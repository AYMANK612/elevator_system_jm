from django.urls import path, include
from rest_framework.routers import DefaultRouter
from elevator_app.views import intialize_elevators
#router = DefaultRouter()


urlpatterns = [
    #path('', include(router.urls)),
    path('initialize/', intialize_elevators, name='initialize_elevators'),
    
]