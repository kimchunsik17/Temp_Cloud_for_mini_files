from django.urls import path
from . import views

app_name = 'cloud_storage'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('upload/', views.upload_view, name='upload'),
    path('download/', views.download_view, name='download'),
]
