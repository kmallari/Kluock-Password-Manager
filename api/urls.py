from django.urls import path
from .views import CredentialsApiView, SingleSiteCredentials, SingleCredentials

urlpatterns = [
    path("", CredentialsApiView.as_view()),
    path("site/<str:site>/", SingleSiteCredentials.as_view()),
    path("id/<str:id>/", SingleCredentials.as_view())
]
