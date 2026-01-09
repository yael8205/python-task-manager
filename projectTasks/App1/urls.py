from django.urls import path
from . import views

urlpatterns = [
    path("", views.register_view, name='register'),
    path("workerhome/", views.workerhome, name='workerhome'),
    path("managerhome/", views.managerhome, name='managerhome'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('claim-task/<int:task_id>/', views.claim_task, name='claim_task'),
    path('profile/', views.profile_setup, name='profile_setup'),
    path('complete-task/<int:task_id>/', views.complete_task, name='complete_task'),
    path('add-task/', views.add_task, name='add_task'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('edit-task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('logout/', views.logout_view, name='logout'),
]