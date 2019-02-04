from django.test import TestCase
from autoservice.models import Employee, Schedule
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta


class ScheduleTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='user')
        employee = Employee.objects.create(first_name='Иван', last_name='Иванов', user=user)
        Schedule.objects.create(employee=employee, date=date(2018, 1, 1), start='08:00', end='10:00')

    def test_empty_ranges(self):
        employee = Employee.objects.get(first_name="Иван")
        schedule = Schedule.objects.get(employee=employee)
        start = datetime.combine(schedule.date, schedule.start)
        end = datetime.combine(schedule.date, schedule.end)
        # массив из одного промежутка времени - время начала и время окончания рабочего дня
        should_range = [(start, end)]
        # у сотрудника должен быть один свободный промежуток времени - should_range
        self.assertEqual(schedule.get_empty_range(), should_range)
        should_hour_range = [(start, end - timedelta(hours=1))]
        # у сотрудника должен быть один свободный промежуток времени на работу, длительностью 1 час - c 8 до 9
        self.assertEqual(list(schedule.get_empty_range_for(1)), should_hour_range)
        # у сотрудника не должно быть свободных промежутков времени на работу длительнотью 3 часа
        self.assertEqual(list(schedule.get_empty_range_for(3)), [])
