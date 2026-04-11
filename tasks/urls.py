from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    path('manager/', views.manager_tasks, name='manager_tasks'),
    path('employee/', views.employee_tasks, name='employee_tasks'),
    path('add/', views.add_task, name='add_task'),
    path('update-task/<int:task_id>/', views.update_task, name='update_task'),
    path('update/<int:task_id>/', views.update_task_status, name='update_task_status'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path("logout/", views.log_out, name="log_out"),
]