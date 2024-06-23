#Rutas específicas de la aplicación
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views


urlpatterns = [
    #Home
    path('', views.index, name='index'),
    #About=Acerca de OlyFlans
    path('about/', views.about, name='about'),
    #Contacto
    path('contact/', views.contact, name='contact'),
    path('success/', views.success, name='success'),
    #Autenticación de usuarios=clientes
    #Login
    path('login/', views.user_login, name='registration/login_client'),
    path('login/welcome/', views.welcome, name='welcome'),
    path('login/', views.user_login, name='login'),
    #Logout: 
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('logout/', LogoutView.as_view(next_page='logout'), name='logout'),
    path('logout/', views.user_logout, name='logout'), 
    path('logout_page/', views.logout_page, name='logout_page'),
    path('login/?next=/accounts/logout/', views.user_logout, name='user_logout'), 
    
    #Formulario de Registro de clientes
    path('registration/', views.registration, name='registration'),
    path('registration/new_client/', views.new_client, name='new_client'),
    
    #Seccion en desarrollo, en fase de pruebas
    path('client/', views.Client, name='client'), #modificar vista a template con tabla de clientes
    path('customers', views.Client, name='customers'), #Funciona
    path('customers/save', views.save_customer, name='save_customer'), #Funciona
    path('customers/edit/<int:client_id>/', views.edit_customer, name='edit_customer'), #Faltan detalles
    path('customers/delete<int:client_id>/', views.delete_customer, name='delete_customer'), #Faltan detalles
]

