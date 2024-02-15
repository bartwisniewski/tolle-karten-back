from django.contrib import admin

from .models import GeneratorTask, Result, Student, Word


class WordAdmin(admin.ModelAdmin):
    pass


class ResultAdmin(admin.ModelAdmin):
    pass


class StudentAdmin(admin.ModelAdmin):
    pass


class GeneratorTaskAdmin(admin.ModelAdmin):
    pass


admin.site.register(Word, WordAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(GeneratorTask, GeneratorTaskAdmin)
