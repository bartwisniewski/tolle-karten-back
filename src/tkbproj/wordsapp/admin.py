from django.contrib import admin

from .models import GeneratorTask, Result, Student, Word


class InputFilter(admin.SimpleListFilter):
    template = "admin/input_filter.html"

    def lookups(self, request, model_admin):
        # Dummy, required to show the filter.
        return ((),)

    def choices(self, changelist):
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice["query_parts"] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice


class InputContainsFilter(InputFilter):
    separator = ", "

    def queryset(self, request, queryset):
        if self.value() is not None:
            field_query = self.parameter_name + "__icontains"
            return queryset.filter(**{field_query: self.value()})


class WordFilter(InputContainsFilter):
    parameter_name = "word"
    title = "word"


class TagFilter(InputContainsFilter):
    parameter_name = "tags"
    title = "tag"


class WordAdmin(admin.ModelAdmin):
    list_display = ["article", "word", "tags", "level", "polish"]
    list_filter = [WordFilter, TagFilter, "level"]


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
