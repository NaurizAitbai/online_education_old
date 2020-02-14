from django.urls import path

from . import views


app_name = 'projects'
urlpatterns = [
    path('', views.list, name='list'),
    path('create', views.create, name='create'),
    path('<int:project_id>/delete', views.delete, name='delete')
]