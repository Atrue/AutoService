from django.views.generic import View
from django.http import JsonResponse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta


def get_time_periods(schedule_ranges):
    for date_ranges in schedule_ranges:
        for date_range in date_ranges:
            for time in divide_time_periods(date_range):
                yield time


def split_date_ranges(ranges, slice_times):
    slice_start, slice_end = slice_times
    for times in ranges:
        start, end = times
        split_start = start < slice_start < end
        split_end = start < slice_end < end
        if split_start:
            yield (start, slice_start)
        if split_end:
            yield (slice_end, end)
        if not split_start and not split_end:
            yield (start, end)


def divide_time_periods(ranges, delta_minute=15, date_format=settings.TIME_INPUT_FORMAT):
    start, end = ranges
    while start <= end:
        yield start.strftime(date_format)
        start = start + timedelta(minutes=delta_minute)


class AjaxListView(View):
    http_method_names = ['get']

    def get(self, request):
        try:
            result = list(self.get_data(request))
            return JsonResponse({'result': result, 'status': True})
        except ObjectDoesNotExist:
            return JsonResponse({'status': False, 'message': 'Объекта с таким запросом не существует'})

    def get_data(self, request):
        return []
