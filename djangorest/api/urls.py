from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView, LoginView
from .views import DetailsView

urlpatterns = [
    url(r'^bucketlists/$',CreateView.as_view(),name="create"),
    url(r'^bucketlists/(?P<pk>[0-9]+)/$', DetailsView.as_view(), name="details"),
    url(r'^auth/login/$', LoginView.as_view(), name="auth-login"),

]

urlpatterns=format_suffix_patterns(urlpatterns)
