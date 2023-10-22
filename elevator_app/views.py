from django.shortcuts import render
from rest_framework.response import Response
from .models import Elevator
# Create your views here.
from rest_framework.decorators import api_view

@api_view(["post"])
def intialize_elevators(request):
    if 'number_of_elevators' in request.data:
        try:
            n = int(request.data.get('number_of_elevators'))
            if n < 1:
                return Response({'message': 'There needs to be atleast one elevator '}, status=400)

            # Create 'n' elevator instances
            for i in range(1, n + 1):
                elevator_name = f'Elevator {i}'
                Elevator.objects.create(name=elevator_name)

            return Response({'message': f'Successfully initialized {n} elevators.'}, status=201)
        except ValueError:
            return Response({'message': 'Invalid input. Please provide a valid number of elevators.'}, status=400)