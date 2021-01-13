from ..models import Answer


class PollPassingHandler:
    def save_user_poll_questions_answers(self, validated_data: dict) -> str:
        for question in validated_data['answers_on_questions']:
            answer_create_data = {
                'question_id': question['question_id'],
                'user_id': validated_data['user_id'],
            }
            text_answer = question.get('text_answer')
            if text_answer:
                answer_create_data['text_answer'] = text_answer

            answer = Answer.objects.create(**answer_create_data)
            # if user choose one or more answers
            selected_answers = question.get('selected_answers')
            if selected_answers:
                for selected_answer_id in selected_answers:
                    answer.selected_question_answer_options.create(user_id=validated_data['user_id'],
                                                               answer_option_id=selected_answer_id)

        return 'Спасибо за прохождение опроса!'
