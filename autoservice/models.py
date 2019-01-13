from django.db import models
from django.conf import settings
from django.utils.timezone import now
from datetime import datetime, timedelta, date
from .helpers import split_date_ranges, get_time_periods
from decimal import Decimal
from random import choice


class CarBrand(models.Model):
    title = models.CharField("Марка", max_length=32)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Марка автомобиля"
        verbose_name_plural = "Марки автомобилей"


class CarType(models.Model):
    title = models.CharField("Тип", max_length=64)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тип автомобиля"
        verbose_name_plural = "Типы автомобилей"


class Car(models.Model):
    brand = models.ForeignKey('CarBrand', on_delete=models.CASCADE, verbose_name="Марка")
    title = models.CharField("Модель", max_length=32)
    type = models.ForeignKey('CarType', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Тип")

    def __str__(self):
        return f"{self.brand} {self.title}"

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"


class CarGeneration(models.Model):
    car = models.ForeignKey('Car', verbose_name="Автомобиль", on_delete=models.CASCADE)
    title = models.CharField("Название", max_length=32)
    year_start = models.SmallIntegerField("Год начала")
    year_end = models.SmallIntegerField('Год окончания', blank=True, null=True)

    def __str__(self):
        return f"{self.car} {self.get_label()}"

    def get_label(self):
        return f"{self.title} ({self.get_years()})"

    def get_years(self):
        return f"{self.year_start} - {self.year_end or 'н.в.'}"

    class Meta:
        verbose_name = "Поколение"
        verbose_name_plural = "Поколения"


class Client(models.Model):
    first_name = models.CharField("Имя", max_length=32)
    last_name = models.CharField("Фамилия", max_length=32, blank=True, null=True)
    middle_name = models.CharField("Отчество", max_length=32, blank=True, null=True)
    email = models.EmailField("Email", blank=True, null=True)
    phone = models.CharField("Телефон", max_length=11, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    first_name = models.CharField("Имя", max_length=32)
    last_name = models.CharField("Фамилия", max_length=32)
    middle_name = models.CharField("Отчество", max_length=32, blank=True, null=True)
    position = models.ForeignKey('Position', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Должность")

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.position})"

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"


class Position(models.Model):
    title = models.CharField("Позиция", max_length=32)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"


class Schedule(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, verbose_name="Сотрудник")
    date = models.DateField("День")
    start = models.TimeField("Начало")
    end = models.TimeField("Конец")

    class Meta:
        verbose_name = "Рабочий график"
        verbose_name_plural = "Рабочие графики"

    def __str__(self):
        return f"({self.employee}) {self.date} {self.start} - {self.end}"

    def get_date_range(self):
        start = datetime.combine(self.date, self.start)
        end = datetime.combine(self.date, self.end)
        return start, end

    def get_empty_range(self):
        empty_range = [self.get_date_range()]
        works = Request.objects.filter(employee=self.employee, date__contains=self.date)
        for work in works:
            empty_range = split_date_ranges(empty_range, work.get_date_range())
        return empty_range

    def get_empty_range_for(self, need_hours: Decimal):
        need_seconds = int(need_hours * 60 * 60)
        empty_range = self.get_empty_range()
        for date_range in empty_range:
            start, end = date_range
            if (end - start).seconds >= need_seconds:
                yield start, end - timedelta(seconds=need_seconds)

    def is_available_for(self, need_hours: Decimal, date_time: datetime):
        empty_range = self.get_empty_range_for(need_hours)
        for date_range in empty_range:
            start, end = date_range
            if start <= date_time <= end:
                return True
        return False


WORK_TYPE_CATEGORIES = (
    ('diagnostics', 'Диагностика'),
    ('repair', 'Ремонт'),
    ('carcase', 'Кузовной')
)


class WorkTypeName(models.Model):
    title = models.CharField("Название", max_length=64)
    category = models.CharField("Категория", max_length=16, choices=WORK_TYPE_CATEGORIES, default=WORK_TYPE_CATEGORIES[0][0])
    description = models.TextField("Описание", blank=True, null=True)

    def get_start_price(self):
        work_type = self.worktype_set.order_by('price').first()
        return work_type.price if work_type else 0

    def is_price_range(self):
        work_types = self.worktype_set.order_by('price')
        first_price = work_types.first()
        last_price = work_types.last()
        return first_price and last_price and first_price.price != last_price.price

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Вид работы"
        verbose_name_plural = "Виды работ"


class WorkType(models.Model):
    name = models.ForeignKey('WorkTypeName', verbose_name='Название', on_delete=models.CASCADE)
    norm_hour = models.DecimalField("Нормо-час", max_digits=6, decimal_places=2)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    car_type = models.ForeignKey('CarType', on_delete=models.CASCADE, verbose_name="Тип автомобиля")

    def __str__(self):
        return f"{self.name} ({self.car_type})"

    class Meta:
        verbose_name = "Вид работы"
        verbose_name_plural = "Виды работ"


REQUEST_STATUSES = (
    ('await', 'Ожидание'),
    ('confirm', 'Подтвержена'),
    ('work', 'В работе'),
    ('done', 'Выполнена'),
    ('closed', 'Закрыта'),
)


class Request(models.Model):
    type = models.ForeignKey('WorkType', on_delete=models.CASCADE, verbose_name="Вид работы")
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, verbose_name="Сотрудник")
    client = models.ForeignKey('Client', on_delete=models.CASCADE, verbose_name="Клиент")
    car = models.ForeignKey('CarGeneration', on_delete=models.CASCADE, verbose_name="Автомобиль")
    status = models.CharField("Статус", max_length=16, choices=REQUEST_STATUSES, default=REQUEST_STATUSES[0][0])
    date = models.DateTimeField("Дата начала работы", blank=True, null=True)
    create_date = models.DateTimeField("Дата создания", auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField("Последнее обновление", auto_now=True, blank=True, null=True)
    finish_date = models.DateTimeField("Окончание работы", blank=True, null=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return f"{self.type} - {self.date}"

    def get_date_range(self):
        start = self.date.replace(tzinfo=None)
        end = start + timedelta(minutes=int(self.type.norm_hour * 60))
        return start, end


def get_available_dates(work_type: WorkType, start_range: date=None, end_range: date=None):
    start_range = start_range or now().date()
    end_range = end_range or now() + timedelta(days=31)
    schedules = Schedule.objects.filter(date__gte=start_range, date__lt=end_range)
    available_schedules = filter(lambda s: s.get_empty_range_for(work_type.norm_hour), schedules)
    available_days = set(s.date for s in available_schedules)
    return sorted(available_days)


def get_available_times(work_type: WorkType, selected_date: date):
    schedules = Schedule.objects.filter(date=selected_date)
    available_schedules = map(lambda s: s.get_empty_range_for(work_type.norm_hour), schedules)
    return sorted(set(get_time_periods(available_schedules)))


def get_available_employee(work_type: WorkType, selected_date_time: datetime):
    schedules = Schedule.objects.filter(date=selected_date_time.date())
    available_schedules = list(filter(lambda s: s.is_available_for(work_type.norm_hour, selected_date_time), schedules))
    random_schedule = choice(available_schedules)
    if random_schedule:
        return random_schedule.employee
