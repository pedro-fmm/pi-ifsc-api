from rest_framework import serializers
from models import Categoria, Genero, FaixaEtaria, Plataforma, Preco, Produto

class PlataformaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plataforma
        fields = '__all__'


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = '__all__'

    
class FaixaEtariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaixaEtaria
        fields = '__all__'


class PrecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preco
        fields = '__all__'


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'