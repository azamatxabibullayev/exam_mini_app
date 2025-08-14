from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("test/<int:pk>/intro/", views.test_intro, name="test_intro"),
    path("test/<int:pk>/take/", views.take_test, name="take_test"),
    path("results/", views.my_results, name="my_results"),
    path("results/<int:pk>/", views.result_detail, name="result_detail"),
]
