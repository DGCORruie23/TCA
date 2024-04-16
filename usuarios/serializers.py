from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from usuarios.models import Usuario

class UserGetSerializer(ModelSerializer):
	class Meta:
		model = Usuario
		fields = [
			'nickname',
			'password',
			]
		
class UserGetSerializerC(ModelSerializer):
	class Meta:
		model = Usuario
		fields = [
			'nickname',
			'nombre',
			'apellido',
			'password',
			'estado',
			'tipo',
			]