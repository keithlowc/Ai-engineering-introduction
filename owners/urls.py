from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('owners/', views.owner_list, name='owner_list'),
    path('owners/create/', views.owner_create, name='owner_create'),
    path('owners/<int:pk>/', views.owner_detail, name='owner_detail'),
    path('owners/<int:pk>/update/', views.owner_update, name='owner_update'),
    path('owners/<int:pk>/delete/', views.owner_delete, name='owner_delete'),
    path('owners/<int:owner_pk>/interaction/create/', views.interaction_create, name='interaction_create'),
]
