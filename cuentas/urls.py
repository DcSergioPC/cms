from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views  # Apéndice


urlpatterns = [
    path('signup/', views.UserCreateAndLoginView.as_view(), name='signup'),    # cambiar
    path('login/', LoginView.as_view(
        redirect_authenticated_user=True,
        template_name='cuentas/login.html'
    ), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('user_detail/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('user_update/<int:pk>/', views.UserUpdate.as_view(), name='user_update'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(),
         name='password_change_done'),
    path('user_delete/<int:pk>/', views.UserDelete.as_view(), name='user_delete'),
    path('logout_confirm/', views.LogoutConfirmView.as_view(), name='logout_confirm'),
    path('usuarios_list/', views.UsuariosList, name='usuarios_list'),
    path('usuarios/edit/<int:user_id>/', views.edit_user_role, name='edit_user_role'),
    
]
