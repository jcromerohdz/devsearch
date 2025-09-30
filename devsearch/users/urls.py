from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>/', views.user_profile, name='user_profile'),
    path('account/', views.user_account, name='account'),
    path('edit-account/', views.edit_account, name='edit_account'),
    # path('create-project/', views.create_project, name='create_project'),
    # path('update-project/<str:pk>/', views.update_project, name='update_project'),
    # path('delete-project/<str:pk>/', views.delete_project, name='delete_project')
]