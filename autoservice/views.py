from django.views.generic import TemplateView, CreateView, FormView
from django.http import JsonResponse
from django.conf import settings
from .models import (
    WorkType, WorkTypeName, CarBrand, Car, CarGeneration, Request, get_available_dates, get_available_times
)
from .helpers import AjaxListView
from .forms import RequestForm, RequestCheckForm
from datetime import datetime


class IndexView(TemplateView):
    template_name = 'index.html'


class SearchCarBrandView(AjaxListView):
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.pk,
            'label': obj.title
        }

    def get_data(self, request):
        types = CarBrand.objects.all()
        return map(self.serialize, types)


class SearchCarView(AjaxListView):
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.pk,
            'label': obj.title
        }

    def get_data(self, request):
        brand_id = request.GET.get('brand')
        types = Car.objects.filter(brand_id=brand_id)
        return map(self.serialize, types)


class SearchCarGenerationView(AjaxListView):
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.pk,
            'label': obj.get_years()
        }

    def get_data(self, request):
        car_id = request.GET.get('car')
        generations = CarGeneration.objects.filter(car_id=car_id)
        return map(self.serialize, generations)


class SearchWorkTypeView(AjaxListView):
    @staticmethod
    def serialize(obj: WorkType):
        return {
            'id': obj.pk,
            'label': str(obj.name),
            'price': obj.price,
        }

    def get_data(self, request):
        car_id = request.GET.get('car')
        car = Car.objects.get(id=car_id)
        types = WorkType.objects.filter(car_type=car.type)
        return map(self.serialize, types)


class SearchDateView(AjaxListView):
    @staticmethod
    def serialize(obj):
        return {
            'id': obj.strftime(settings.DATE_INPUT_FORMAT),
            'label': obj.strftime('%d %B %Y')
        }

    def get_data(self, request):
        work = WorkType.objects.get(id=request.GET.get('work'))
        available_days = get_available_dates(work)
        return map(self.serialize, sorted(available_days))


class SearchTimeView(AjaxListView):
    @staticmethod
    def serialize(obj):
        return {
            'id': obj,
            'label': obj
        }

    def get_data(self, request):
        day = request.GET.get('date')
        selected_date = datetime.strptime(day, settings.DATE_INPUT_FORMAT).date()
        work = WorkType.objects.get(id=request.GET.get('work'))
        available_schedules = get_available_times(work, selected_date)
        return map(self.serialize, available_schedules)


class CreateRequestForm(CreateView):
    form_class = RequestForm
    model = Request
    http_method_names = ['post']

    def form_invalid(self, form):
        errors = {e: [i for i in form.errors[e]] for e in form.errors}
        return self.render_to_response(errors, False)

    def form_valid(self, form):
        self.object = form.save()
        return self.render_to_response(self.object.id, True)

    def render_to_response(self, context, status=False, **response_kwargs):
        return JsonResponse({
            'status': status,
            'data': context,
        })


class WorkInfoView(AjaxListView):
    @staticmethod
    def serialize(obj: WorkTypeName):
        return {
            'label': obj.title,
            'price': obj.get_start_price(),
            'is_range': obj.is_price_range(),
        }

    def get_data(self, request):
        category = request.GET.get('category')
        types = WorkTypeName.objects.filter(category=category)
        return map(self.serialize, types)


class CheckRequestStatusView(FormView):
    form_class = RequestCheckForm
    http_method_names = ['post']

    def form_valid(self, form):
        try:
            work = Request.objects.get(id=form.cleaned_data['id'], client__phone=form.cleaned_data['phone'])
            return self.render_to_response({
                'id': work.id,
                'status': work.get_status_display(),
                'finish_date': work.finish_date.strftime(settings.DATETIME_INPUT_FORMAT) if work.finish_date else None,
            }, status=True)
        except Request.DoesNotExist:
            return self.render_to_response({}, status=True)

    def form_invalid(self, form):
        errors = {e: [i for i in form.errors[e]] for e in form.errors}
        return self.render_to_response(errors, False)

    def render_to_response(self, context, status=False, **response_kwargs):
        return JsonResponse({
            'status': status,
            'data': context,
        })
