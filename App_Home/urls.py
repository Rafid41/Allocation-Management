# tasks\urls.py
from django.urls import path
from App_Home import views


app_name = "App_Home"


urlpatterns = [
    path("", views.home, name="home_page"),
    # path('', views.TaskListView.as_view(), name='task_list'),
    # path('task_detail_view/<pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    # path('create_task/',views.CreateNewTaskView.as_view(), name='create_task'),
    # path('update_task/<pk>/',views.TaskUpdateView.as_view(), name='update_task'),
    # path('task_delete/<pk>/', views.TaskDeleteView.as_view(), name='task_delete'),
    # path('add_image/<pk>/', views.add_image_to_task, name='add_image_to_task'),
    # path('delete_image/<pk>/', views.DeleteImageView.as_view(), name='delete_image'),
]
