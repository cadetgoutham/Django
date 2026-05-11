from django.urls import path
from .views import delete_task, home, toggle_task

urlpatterns = [
    path('', home, name='home'),
    path('delete/<int:pk>/', delete_task, name='delete_task'),
    path('toggle/<int:pk>/', toggle_task, name='toggle_task'),
]