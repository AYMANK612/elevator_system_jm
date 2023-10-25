from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist  # Import ObjectDoesNotExist from django.core.exceptions
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Elevator, E_Request
from .serializers import ElevatorSerializer, RequestSerializer
# Create your views here.
from rest_framework.decorators import api_view

#API to intilaze elevators 
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
    if 'from_floor' in request.data:
        try:
            requested_floor=int(request.data.get('from_floor'))
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
            optimal_elevator.is_door_open = False if optimal_elevator.is_door_open else optimal_elevator.is_door_open

            print(optimal_elevator.current_floor < requested_floor) 
            if optimal_elevator.current_floor < requested_floor:
                optimal_elevator.is_moving_up=True
            optimal_elevator.current_floor=requested_floor
            optimal_elevator.save()
        
            # Create a request 
            request_instance = E_Request.objects.create(elevator=optimal_elevator, floor=requested_floor)
            request_instance.save()
            
        
            return Response({'message': f'Optimal elevator is {optimal_elevator.name}'}, status=200)
        else:
            return Response({'message': 'No operational elevators available.'}, status=400)
        

#API to Fetch all requests for a given elevator
class RequestViewSet(viewsets.ModelViewSet):
    queryset = Elevator.objects.all()
    serializer_class = RequestSerializer

    def list(self, request):
        elevator_id = request.query_params.get('elevator_id')

        if elevator_id:
            try:
                elevator = Elevator.objects.get(id=elevator_id)
                requests = E_Request.objects.filter(elevator=elevator)
            except ObjectDoesNotExist:
                return Response({'message': f'Elevator with ID {elevator_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
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
    
#API to open or close door 
@api_view(["put"])
def door_toggle(request):
    elevator_id = request.data.get('elevator_id')

    try:
        elevator= Elevator.objects.get(id=elevator_id)
        if elevator.is_door_open == False:
            elevator.is_door_open = not elevator.is_door_open
            elevator.save()
            return Response({'message': f'Door for Elevator with ID {elevator_id} is open now'})
        else:
            elevator.is_door_open = not elevator.is_door_open
            elevator.save()
            return Response({'message': f'Door for Elevator with ID {elevator_id} is closed now'})
           
    except ObjectDoesNotExist:
        return Response({'message': f'Elevator with ID {elevator_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)
    

#API to get the direction an elevator
@api_view(['GET'])
def elevator_direction(request):
    elevator_id = request.query_params.get('elevator_id')

    if not elevator_id:
        return Response({'message': 'Please provide an elevator ID as a query parameter.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        elevator = Elevator.objects.get(pk=elevator_id)
    except Elevator.DoesNotExist:
        return Response({'message': 'Elevator not found.'}, status=status.HTTP_404_NOT_FOUND)

    if not elevator.is_working:
        return Response({'message': 'Elevator is currently not working.'}, status=status.HTTP_400_BAD_REQUEST)

    if elevator.is_moving_up:
        return Response({'direction': 'up'}, status=status.HTTP_200_OK)
    else:
        return Response({'direction': 'down'}, status=status.HTTP_200_OK)
    
    

@api_view(['GET'])
def next_destination(request):
    elevator_id = request.query_params.get('elevator_id')

    if not elevator_id:
        return Response({'message': 'Please provide an elevator ID as a query parameter.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        elevator = Elevator.objects.get(pk=elevator_id)
    except Elevator.DoesNotExist:
        return Response({'message': 'Elevator not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Check first if the elevator is working
    if not elevator.is_working:
        return Response({'message': 'Elevator is not working.'}, status=status.HTTP_400_BAD_REQUEST)

    # Find the latest request for the elevator
    latest_request = E_Request.objects.filter(elevator=elevator).order_by('-timestamp').first()

    if latest_request:
        next_destination = latest_request.floor
        return Response({'next_destination': next_destination}, status=status.HTTP_200_OK)
    else:
        # If there are no requests,return that the elevator has no next destination
        return Response({'message': 'No pending requests for this elevator.'}, status=status.HTTP_200_OK)