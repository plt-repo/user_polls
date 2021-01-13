from rest_framework import serializers

from .models import Poll, QuestionAnswerOption, Question, Answer


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = '__all__'


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswerOption
        fields = ('id', 'text')


class AnswerSerializer(serializers.ModelSerializer):
    selected_answers_options = serializers.ListField(read_only=True)

    class Meta:
        model = Answer
        exclude = ('id', 'user_id', 'question')


class QuestionSerializer(serializers.ModelSerializer):
    answer_options = AnswerOptionSerializer(many=True)
    answer = AnswerSerializer(many=True)

    class Meta:
        model = Question
        exclude = ('poll',)


class PassedPollSerializer(PollSerializer):
    questions = QuestionSerializer(many=True)


class AnswersOnQuestionsSerializer(serializers.Serializer):
    question_id = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    selected_answers = serializers.PrimaryKeyRelatedField(many=True, required=False, default=[],
                                                          queryset=QuestionAnswerOption.objects.all())
    text_answer = serializers.CharField(required=False, allow_null=True)

    def validate(self, attrs):
        question = attrs['question_id']
        selected_answers = attrs.get('selected_answers')
        text_answer = attrs.get('text_answer')

        if selected_answers:
            question_answer_options_ids = question.answer_options.values_list('id', flat=True)
            not_existing_in_question_options_ids = [str(answer.id) for answer in
                                                    selected_answers
                                                    if answer.id not in question_answer_options_ids]

            if not_existing_in_question_options_ids:
                raise serializers.ValidationError(
                    {"selected_answers": "Варианты ответа на вопрос с id ({}) не существуют в вопросе.".format(','.join(
                        not_existing_in_question_options_ids))}
                )

        if selected_answers and text_answer:
            raise serializers.ValidationError(
                {"selected_answers, text_answer": "Эти поля не могут быть переданы вместе."}
            )

        if question.type == 1 and not text_answer:
            raise serializers.ValidationError(
                {"text_answer": "Вы не передали ответ на вопрос."}
            )
        elif question.type in [2, 3] and not selected_answers:
            raise serializers.ValidationError(
                {"selected_answers": "Вы не передали ответ на вопрос."}
            )

        return attrs


class PollPassingSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(min_value=0)
    poll = serializers.PrimaryKeyRelatedField(required=True, queryset=Poll.objects.all())
    answers_on_questions = AnswersOnQuestionsSerializer(many=True)

    def validate_answers_on_questions(self, value):
        if not value:
            raise serializers.ValidationError("Это поле не может быть пустым.")
        return value

    def validate(self, attrs):
        is_answer_exists = Poll.objects.filter(
            id=attrs['poll'].id, questions__answer__user_id=attrs['user_id']).exists()
        if is_answer_exists:
            raise serializers.ValidationError(
                {"detail": "Пользователь уже проходил данный опрос!"}
            )

        poll_questions_ids = Question.objects.filter(poll_id=attrs['poll'].id).values_list('id', flat=True)
        not_existing_in_poll_questions_ids = [str(answer['question_id'].id) for answer in attrs['answers_on_questions']
                                              if answer['question_id'].id not in poll_questions_ids]

        if not_existing_in_poll_questions_ids:
            raise serializers.ValidationError(
                {"answers_on_questions": "Вопросы с id ({}) не существуют в опросе.".format(','.join(
                    not_existing_in_poll_questions_ids))}
            )

        if len(attrs['answers_on_questions']) < len(poll_questions_ids):
            raise serializers.ValidationError(
                {"answers_on_questions": "Вы передали не все ответы на вопросы."}
            )

        return attrs
