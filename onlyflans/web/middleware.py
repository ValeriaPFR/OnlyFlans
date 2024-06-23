#Limpieza automática del cache del servidor, esto para que se cierre adecuadamente la sesion. 
# Implementado luego de advertir que al cerrar sesion con logout, al ir a la vista de Welcome, seguía mostrando el nombre del usuario y la vista protegida
#from django.core.cache import cache
#--1
# from django.utils.deprecation import MiddlewareMixin
# class ClearCacheOnLogoutMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         if not request.user.is_authenticated:
#             cache.clear()

#--2
from django.contrib.sessions.models import Session

class ClearCacheOnLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path == '/logout/' and request.user.is_authenticated:
            # Aquí limpias la caché relacionada a la sesión del usuario
            Session.objects.filter(session_key=request.session.session_key).delete()
        return response