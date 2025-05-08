# accounts/serializers.py

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        # authenticate usa USERNAME_FIELD = 'email'
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Credenciales inválidas")
        if not user.is_active:
            raise serializers.ValidationError("Usuario desactivado")
        data['user'] = user
        return data

class UserSerializer(serializers.ModelSerializer):
    # mostramos los nombres de grupo en vez de solo la PK
    groups = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Group.objects.all(),
        required=False
    )

    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
            'groups',
        )
        read_only_fields = ('id',)

    def create(self, validated_data):
        groups_data = validated_data.pop('groups', [])
        password    = validated_data.pop('password', None)
        email       = validated_data.get('email')

        # asigna el username igual al email (o cualquier otro único)
        user = User(
            username=email,
            email=email,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()

        user.groups.set(groups_data)
        return user

    def update(self, instance, validated_data):
        # extraemos y quitamos de los datos
        groups_data = validated_data.pop('groups', None)
        password    = validated_data.pop('password', None)

        # actualizamos campos normales
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # contraseña
        if password:
            instance.set_password(password)

        instance.save()

        # re-asignamos grupos si vienen en la request
        if groups_data is not None:
            instance.groups.set(groups_data)

        return instance