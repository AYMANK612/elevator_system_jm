from django.urls import path, include
from rest_framework.routers import DefaultRouter
from elevator_app.views import intialize_elevators,request_elevator,RequestViewSet, maintainance_toggle,door_toggle,elevator_direction,next_destination
#router = DefaultRouter()


urlpatterns = [
    #path('', include(router.urls)),
    path('initialize/', intialize_elevators, name='initialize_elevators'),
    path('request/', request_elevator, name='request_elevator'),
    path('getall_requests/', RequestViewSet.as_view({'get': 'list'}), name='getall_requests'),
    path('getall_requests/<int:elevator_id>/', RequestViewSet.as_view({'get': 'retrieve'}), name='request-detail'),
    path('maintanaince_toggle/', maintainance_toggle,name='maintanaince_toggle'),
    path('door_toggle/',door_toggle,name='door_toggle'),
    path('direction/',elevator_direction,name='direction'),
    path('destination/',next_destination,name='next_destination')
]