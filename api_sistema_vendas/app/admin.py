from django import forms
from django.contrib import admin
from .models import Empresa, Fornecedor, Cliente, Funcionario, Cargo, Usuario, Plataforma, FaixaEtaria, Genero, Categoria, Preco, Produto, Venda, VendaItem
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from app.models import Usuario

class UsuarioRegistrarForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação da senha', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ('email', 'username', 'primeiro_nome', 'ultimo_nome')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("As senhas são diferentes")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UsuarioAtualizarForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Usuario
        fields = ('email', 'password', 'username', 'primeiro_nome', 'ultimo_nome', 'is_active', 'is_admin')


class UsuarioAdmin(BaseUserAdmin):
    form = UsuarioAtualizarForm
    add_form = UsuarioRegistrarForm

    list_display = ('email', 'username', 'primeiro_nome', 'ultimo_nome', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'primeiro_nome', 'ultimo_nome',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'primeiro_nome', 'ultimo_nome', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Funcionario)
admin.site.register(Empresa)
admin.site.register(Fornecedor)
admin.site.register(Cliente)
admin.site.register(Cargo)
admin.site.register(Plataforma)
admin.site.register(FaixaEtaria)
admin.site.register(Genero)
admin.site.register(Categoria)
admin.site.register(Preco)
admin.site.register(Produto)
admin.site.register(Venda)
admin.site.register(VendaItem)