from rest_framework import serializers
from .models import Loan

# Made Serializer for Loan Model
class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ('user', 'amount', 'term', 'installment','date','status')



