from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('create/', views.create, name='create'),
    path('edit/<str:movies_id>', views.edit, name='edit'),
    path('delete/<str:movies_id>', views.delete, name='delete'),
]
