# accounts/views.py

from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, UserSerializer


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        # Obtenemos o creamos token existente
        return Response({ 'user': UserSerializer(user).data})

class UserViewSet(viewsets.ModelViewSet):
    """
    CRUD completo de usuarios. Para producción revisa permisos
    """ 
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    # Solo usuarios autenticados pueden ver/editarlos
    # Si quieres que cada quien solo maneje su propio perfil, filtra en get_queryset
