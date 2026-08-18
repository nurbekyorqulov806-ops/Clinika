from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    path('', views.doctor_list_view, name='list'),
    path('<int:pk>/', views.doctor_detail_view, name='detail'),
]
