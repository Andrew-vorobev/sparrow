from django.contrib import admin

from .models import *


class VacancyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'published_at')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'content')


class TypeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Stats)
admin.site.register(Image)
