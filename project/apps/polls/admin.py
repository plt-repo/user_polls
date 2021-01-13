from django.contrib import admin

from .models import Poll, Question, QuestionAnswerOption


# Inline classes
class AnswerOptionInlineAdmin(admin.StackedInline):
    model = QuestionAnswerOption
    fields = ['text']
    extra = 0
    classes = ['collapse']


class QuestionInlineAdmin(admin.StackedInline):
    model = Question
    extra = 0
    classes = ['collapse']


# Register your models here.
@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'description']
    inlines = [QuestionInlineAdmin]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # obj is not None, so this is an edit
            return ['start_date']  # Return a list or tuple of readonly fields' names
        else:  # This is an addition
            return []


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'text']
    list_filter = ['poll']

    inlines = [AnswerOptionInlineAdmin]
