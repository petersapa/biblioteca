from django.contrib import admin
from .models import *

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('nom', 'cognom')
    search_fields = ('nom', 'cognom')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)

@admin.register(Llibre)
class LlibreAdmin(admin.ModelAdmin):
    list_display = ('titol', 'descripcio', 'isbn', 'autor', 'categoria', 'prestat')
    list_filter = ('prestat', 'categoria')
    search_fields = ('titol', 'isbn')

@admin.register(Alumne)
class AlumneAdmin(admin.ModelAdmin):
    list_display = ('usuari', '__str__', 'idalu', 'curs')
    search_fields = ('usuari__username', 'idalu')

@admin.register(Prestec)
class PrestecAdmin(admin.ModelAdmin):
    list_display = ('llibre', 'alumne', 'data_prestec', 'data_devolucio')
    list_filter = ('data_prestec', 'data_devolucio')