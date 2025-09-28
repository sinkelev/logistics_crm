from rest_framework import viewsets
from .models import Expense
from .serializers import ExpenseSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.select_related("route", "vehicle", "employee")
    serializer_class = ExpenseSerializer