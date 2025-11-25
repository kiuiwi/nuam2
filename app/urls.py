from django.urls import path
from . import views

urlpatterns = [

    # HOME
    path('', views.inicio, name='inicio'),

    # USUARIO + PERSONA
    path('registros/', views.lista_registros, name='lista_registros'),
    path('registros/nuevo/', views.crear_registro, name='crear_registro'),
    path('registros/<int:usuario_id>/editar/', views.editar_registro, name='editar_registro'),
    path('registros/<int:usuario_id>/eliminar/', views.eliminar_registro, name='eliminar_registro'),

    # DOCUMENTOS
    path('documentos/', views.lista_documentos, name='lista_documentos'),
    path('documentos/nuevo/', views.crear_documento, name='crear_documento'),
    path('documentos/<int:documento_id>/editar/', views.editar_documento, name='editar_documento'),
    path('documentos/<int:documento_id>/eliminar/', views.eliminar_documento, name='eliminar_documento'),

    # LOGS
    path('logs/', views.lista_logs, name='lista_logs'),





    # AUTENTICACIÓN
    path('login/', views.login_view, name='login'),
    path('menu_usuario/', views.menu_usuario, name='menu_usuario'),
    path('menu_admin/', views.menu_admin, name='menu_admin'),
    path('logout/', views.logout_view, name='logout'),
]
