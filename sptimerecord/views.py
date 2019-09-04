from rest_framework import viewsets

from .models import TimeRecord
from .serializer import TimeRecordSerializer


class TimeRecordViews(viewsets.ModelViewSet):
    queryset = TimeRecord.objects.all()
    serializer_class = TimeRecordSerializer
