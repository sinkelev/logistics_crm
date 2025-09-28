from rest_framework import viewsets
from .models import Route
from .serializers import RouteSerializer

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related("vehicle", "driver").prefetch_related("routecargo_set__cargo")
    serializer_class = RouteSerializer