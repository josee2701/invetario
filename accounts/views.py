# accounts/views.py

from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer, UserSerializer


class RegisterAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {'user': UserSerializer(user).data},
            status=status.HTTP_201_CREATED
        )


class LoginAPIView(APIView):
    permission_classes     = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)

        access_token = refresh.access_token

        access_token['groups'] = [g.name for g in user.groups.all()]

        access  = str(access_token)
        refresh = str(refresh)

        return Response({
            'user':          UserSerializer(user).data,
            'access_token':  access,
            'refresh_token': refresh,
        }, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    """
    CRUD completo de usuarios. Para producción revisa permisos
    """ 
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    # Solo usuarios autenticados pueden ver/editarlos
    # Si quieres que cada quien solo maneje su propio perfil, filtra en get_queryset
