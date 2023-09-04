from django.urls import path
from .views import index, create_db

urlpatterns = [
    path("", index, name="index"),
    path("create_db", create_db, name="create_db"),
]
