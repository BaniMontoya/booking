# api/admin.py
from django.contrib import admin
from api.models import Stock_En_booking, booking, Categoria,Producto,SubCategoria

admin.site.register(Stock_En_booking)
admin.site.register(booking)
admin.site.register(Categoria)
admin.site.register(SubCategoria)
admin.site.register(Producto)