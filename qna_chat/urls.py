from django.urls import path
from .views import index, create_db, check_task_status

urlpatterns = [
    path("", index, name="index"),
    path("create_db", create_db, name="create_db"),
    path("check_task_status", check_task_status, name="check_task_status"),
]
