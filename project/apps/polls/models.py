from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices


class Poll(models.Model):
    name = models.CharField(max_length=500, verbose_name=_('Название'))
    start_date = models.DateTimeField(verbose_name=_('Дата старта'))
    end_date = models.DateTimeField(verbose_name=_('Дата окончания'))
    description = models.TextField(verbose_name=_('Описание'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Опрос')
        verbose_name_plural = _('Опросы')


class Question(models.Model):
    TYPES = Choices(
        (1, _('Ответ текстом')),
        (2, _('Ответ с выбором одного варианта')),
        (3, _('Ответ с выбором нескольких вариантов')),
    )

    poll = models.ForeignKey(Poll, models.CASCADE, related_name='questions', verbose_name=_('Опрос'))
    type = models.IntegerField(choices=TYPES, verbose_name=_('Тип вопроса'))
    text = models.TextField(verbose_name=_('Текст вопроса'))

    class Meta:
        verbose_name = _('Вопрос')
        verbose_name_plural = _('Вопросы')


class QuestionAnswerOption(models.Model):
    question = models.ForeignKey(Question, models.CASCADE, related_name='answer_options', verbose_name=_('Вопрос'))
    text = models.TextField(verbose_name=_('Описание варианта ответа'))

    class Meta:
        verbose_name = _('Вариант ответа')
        verbose_name_plural = _('Варианты ответов')


class Answer(models.Model):
    question = models.ForeignKey(Question, models.CASCADE, related_name='answer', verbose_name=_('Вопрос'))
    text_answer = models.TextField(null=True, blank=True, verbose_name=_('Текстовый ответ'))
    user_id = models.IntegerField(verbose_name=_('Идентификатор пользователя'))

    @property
    def selected_answers_options(self):
        selected_question_answer_options = self.selected_question_answer_options.filter(
            user_id=self.user_id, answer_option__question_id=self.question_id).values('answer_option_id')
        # values list does not work, so i get id from values dict
        return [selected_question_answer_option['answer_option_id'] for
                selected_question_answer_option in selected_question_answer_options]

    class Meta:
        verbose_name = _('Ответ')
        verbose_name_plural = _('Ответы')


class SelectedQuestionAnswerOption(models.Model):
    user_id = models.IntegerField(verbose_name=_('Идентификатор пользователя'))
    answer_option = models.ForeignKey(QuestionAnswerOption, models.CASCADE, related_name='+',
                                      verbose_name=_('Вариант ответа'))
    answer = models.ForeignKey(Answer, models.CASCADE, related_name='selected_question_answer_options',
                               verbose_name=_('Выбранные пользователем варианты ответа'))

    class Meta:
        verbose_name = _('Выбранный пользователем вариант ответа')
        verbose_name_plural = _('Выбранные пользователем варианты ответа')
