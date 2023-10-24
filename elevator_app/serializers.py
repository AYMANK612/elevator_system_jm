from rest_framework import serializers
from elevator_app.models import Elevator ,E_Request

class ElevatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elevator
        fields = '__all__'

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = E_Request
        fields = '__all__'