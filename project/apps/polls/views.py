from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema

from .models import Poll
from .mixins.views import PollsListViewMixin, PassedPollsByUserIdListViewMixin
from .serializers import PollPassingSerializer
from .handlers.pool_passing import PollPassingHandler


class PollsListView(PollsListViewMixin, ListAPIView):
    @swagger_auto_schema(
        operation_description="Список опросов."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PollsPassingCreateView(APIView):
    @swagger_auto_schema(
        request_body=PollPassingSerializer,
        operation_description="Прохождение опроса. Поля answers_on_questions__text_answer и "
                              "answers_on_questions__selected_answers отвечают за прием ответа от пользователя, "
                              "ответ передается в нужное поле в зависимости от типа вопроса. Если тип вопроса 1(Ответ "
                              "текстом) то ответ нужно передавать в поле answers_on_questions__text_answer, "
                              "в остальных случаях в поле answers_on_questions__selected_answers. "
    )
    def post(self, request, poll_id: int):
        request.data['poll'] = poll_id
        serializer = PollPassingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(PollPassingHandler().save_user_poll_questions_answers(serializer.data),
                        status=status.HTTP_201_CREATED)


class PassedPollsByUserIdListView(PassedPollsByUserIdListViewMixin, ListAPIView):
    @swagger_auto_schema(
        operation_description="Пройденные опросы по id пользователя"
    )
    def get(self, request, *args, **kwargs):
        self.queryset = Poll.objects.filter(questions__answer__user_id=kwargs['user_id']).distinct()
        return super().get(request, *args, **kwargs)
