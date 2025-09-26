from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('todo/create/', views.todo_create, name='todo_create'),
    path('todo/update/<int:pk>/', views.todo_update, name='todo_update'),
    path('todo/delete/<int:pk>/', views.todo_delete, name='todo_delete'),
    path('todo/toggle/<int:pk>/', views.todo_toggle_complete, name='todo_toggle'),
]