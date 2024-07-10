from rest_framework import serializers

class SchemeSerializer(serializers.Serializer):
    scheme_name = serializers.CharField(max_length=100)
    tenure = serializers.IntegerField()
    amount = serializers.IntegerField()
    scheme_type = serializers.CharField(max_length=20)
    rate_of_interest = serializers.IntegerField()
    created_by=serializers.CharField()
    create_post = serializers.BooleanField(default=False)