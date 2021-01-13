from django.urls import path
from django.conf.urls import url
from rest_framework.permissions import AllowAny

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from .views import PollsListView, PollsPassingCreateView, PassedPollsByUserIdListView

schema_view = get_schema_view(
    openapi.Info(
        title="User Polls App",
        default_version='v1',
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('list/', PollsListView.as_view(), name='polls_list_url'),
    path('list/<int:poll_id>/passing-by-user-id/', PollsPassingCreateView.as_view(), name='polls_passing_create_url'),
    path('list/passed-by-user-id/<int:user_id>/', PassedPollsByUserIdListView.as_view(),
         name='passed_polls_by_user_id_list_url'),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
