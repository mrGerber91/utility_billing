from rest_framework import viewsets
from .models import Rates, Usage
from .serializers import RatesSerializer, UsageSerializer

class RatesViewSet(viewsets.ModelViewSet):
    queryset = Rates.objects.all()
    serializer_class = RatesSerializer

class UsageViewSet(viewsets.ModelViewSet):
    queryset = Usage.objects.all()
    serializer_class = UsageSerializer
