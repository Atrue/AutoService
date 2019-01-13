from django.contrib import admin
from .models import Employee, Client, Request, WorkTypeName, WorkType, Position, Schedule, CarType, CarBrand, Car, CarGeneration


class WorkTypeInline(admin.TabularInline):
    model = WorkType
    min_num = 1
    extra = 0


class WorkTypeNameAdmin(admin.ModelAdmin):
    inlines = (WorkTypeInline, )


class CarGenerationInline(admin.TabularInline):
    model = CarGeneration
    min_num = 1
    extra = 0


class CarAdmin(admin.ModelAdmin):
    inlines = (CarGenerationInline, )


admin.site.register(Employee)
admin.site.register(Client)
admin.site.register(WorkTypeName, WorkTypeNameAdmin)
admin.site.register(Request)
admin.site.register(Position)
admin.site.register(Schedule)
admin.site.register(CarType)
admin.site.register(CarBrand)
admin.site.register(Car, CarAdmin)
