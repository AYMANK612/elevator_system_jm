from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist  # Import ObjectDoesNotExist from django.core.exceptions
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Elevator, E_Request
from .serializers import ElevatorSerializer, RequestSerializer
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
    
#API to request an elevator at any floor
@api_view(["post"])
def request_elevator(request):
    if 'floor' in request.data:
        try:
            requested_floor=int(request.data.get('floor'))
        except ValueError:
            return Response({'message': 'Invalid input. Please provide a valid floor number.'}, status=400)
        
        elevators=Elevator.objects.filter(is_working=True).order_by('current_floor')
        optimal_elevator=None
        min_distance = float('inf')
        
        #get the most optimal elevator 
        for elevator in elevators:
            distance_to_floor=abs(elevator.current_floor-requested_floor)
            if distance_to_floor < min_distance:
                optimal_elevator=elevator
                min_distance=distance_to_floor
        if optimal_elevator:
            optimal_elevator.current_floor=requested_floor
            optimal_elevator.save()
        if optimal_elevator.current_floor < requested_floor:
            optimal_elevator.is_moving_up=True
        
        if optimal_elevator:
            # Create a request and associate it with the optimal elevator
            request_instance = E_Request.objects.create(elevator=optimal_elevator, floor=requested_floor)
            request_instance.save()
            
            # Update the elevator's state
            optimal_elevator.current_floor = requested_floor
            optimal_elevator.is_moving_up = optimal_elevator.current_floor < requested_floor
            optimal_elevator.save()
            return Response({'message': f'Optimal elevator is {optimal_elevator.name}'}, status=200)
        else:
            return Response({'message': 'No operational elevators available.'}, status=400)
        

#API to Fetch all requests for a given elevator
class RequestViewSet(viewsets.ModelViewSet):
    serializer_class = RequestSerializer

    def list(self, request):
        elevator_id = request.query_params.get('elevator_id')
        
        # Check if elevator_id is provided in the query parameters
        if elevator_id:
            try:
                requests = E_Request.objects.filter(elevator=elevator_id)
            except ObjectDoesNotExist:
                return Response({'message': f'Elevator with ID {elevator_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # If elevator_id is not provided, return all requests
            requests = E_Request.objects.all()

        serializer = RequestSerializer(requests, many=True)
        return Response(serializer.data)

#API to Mark a elevator as not working or in maintenance 
@api_view(["put"])
def maintainance_toggle(request):
    elevator_id = request.data.get('elevator_id')

    try:
        elevator= Elevator.objects.get(id=elevator_id)
        if elevator.is_working == True:
            elevator.is_working = not elevator.is_working
            elevator.save()
            return Response({'message': f'Elevator with ID {elevator_id} maintenance status marked as not working'})
        else:
            elevator.is_working = not elevator.is_working
            elevator.save()
            return Response({'message': f'Elevator with ID {elevator_id} maintenance status marked as working'})
           
    except ObjectDoesNotExist:
        return Response({'message': f'Elevator with ID {elevator_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
#API to Mark a elevator as not working or in maintenance 
