from django.urls import path
from . import views

urlpatterns = [
    # Autenticação 
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Projetos
    path('projects/new/', views.project_create, name='project_create'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project_delete'),

    # Membros
    path('projects/<int:pk>/members/add/', views.project_add_member, name='project_add_member'),
    path('projects/<int:pk>/members/<int:user_pk>/remove/', views.project_remove_member, name='project_remove_member'),

    # Tarefas
    path('projects/<int:project_pk>/tasks/new/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('tasks/<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('tasks/<int:pk>/status/<str:new_status>/', views.task_change_status, name='task_change_status'),

    # Comentários
    path('comments/<int:pk>/delete/', views.comment_delete, name='comment_delete'),

    # Notificações
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/clear/', views.notification_clear, name='notification_clear'),
    
    # Petfil 
    path('profile/', views.profile, name='profile'),
    
]