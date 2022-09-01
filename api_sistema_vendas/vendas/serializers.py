from rest_framework import serializers
from .models import Venda, VendaItem

class VendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venda
        fields = '__all__'


class VendaItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendaItem
        fields = '__all__'

