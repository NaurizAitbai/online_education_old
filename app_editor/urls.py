from django.urls import path

from . import views


app_name = 'editor'
urlpatterns = [
    path('<int:project_id>', views.editor, name='editor'),
]