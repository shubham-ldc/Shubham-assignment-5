from rest_framework import serializers

class UserSignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=100)
    contact_number = serializers.CharField(max_length=100)
    date_of_birth = serializers.DateField(format="%d-%m-%Y", input_formats=["%d-%m-%Y"])
    email = serializers.EmailField(max_length=100, allow_null=False)

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(max_length=100)