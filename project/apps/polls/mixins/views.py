from ..serializers import PollSerializer, PassedPollSerializer
from ..models import Poll


class PollsListViewMixin:
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class PassedPollsByUserIdListViewMixin:
    queryset = Poll.objects.none()  # just a stub, override in view get method
    serializer_class = PassedPollSerializer
