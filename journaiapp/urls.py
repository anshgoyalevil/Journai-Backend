from django.urls import path, re_path
from journaiapp import views

urlpatterns = [
    re_path(r'^api/newtrip$', views.new_trip),
]
