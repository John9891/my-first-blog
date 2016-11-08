from django.contrib import admin
from sistema.models import Origen, RutaAlimentadora, TipoDia, ListaDias, HorarioRecorrido, Usuario, TiempoAsignacion, BusAlimentador, Operador, Despacho

class OrigenAdmin(admin.ModelAdmin):
    list_display = ('CodOrigen', 'NombreOrigen')
    search_fields = ('NombreOrigen',)


class RutaAlimentadoraAdmin(admin.ModelAdmin):
    list_display = ('CodRuta','NombreRuta','CodOrigen','Area','UltimoDespacho',)
    search_fields = ('NombreRuta',)
    list_filter = ('CodOrigen', 'UltimoDespacho',)


class TipoDiaAdmin(admin.ModelAdmin):
    list_display = ('TipoDia', 'NombreTipoDia',)


class ListaDiasAdmin(admin.ModelAdmin):
    list_display = ('CodDia', 'Fecha', 'TipoDia',)
    list_filter = ('TipoDia',)


class HorarioRecorridoAdmin(admin.ModelAdmin):
    list_display = ('CodFranja', 'CodRuta', 'HoraInicio', 'HoraFin', 'TiempoEstimado', 'TipoDia', 'Franja',)
    list_filter = ('CodRuta', 'HoraInicio', 'HoraFin', 'TiempoEstimado', 'Franja',)


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('NumAcceso', 'UID', 'FechaAcceso', 'HoraAcceso', 'CodRuta', 'PasajerosEspera', 'DensidadPasajeros',)


class TiempoAsignacionAdmin(admin.ModelAdmin):
    list_display = ('NumSolicitud', 'CodRuta', 'Fecha', 'Hora', 'TiempoEspera', 'NumeroBus', 'Despachado',)
    list_filter = ('CodRuta', 'Fecha', 'TiempoEspera',)


class BusAlimentadorAdmin(admin.ModelAdmin):
    list_display = ('NumeroBus', 'CodRuta', 'Estado', 'CapacidadBus', 'NumDespacho',)
    list_filter = ('CodRuta', 'Estado', 'CapacidadBus',)

class DespachoAdmin(admin.ModelAdmin):
    list_display = ('NumDespacho', 'CodRuta', 'NumeroBus', 'FechaDespacho', 'HoraDespacho', 'HoraLlegada', 'Delay', 'FactorConfiabilidad', 'CargaPasajeros', 'Frecuencia', 'HoraLlegadaEsperada', 'Tope')
    list_filter = ('CodRuta', 'NumeroBus', 'Delay')

admin.site.register(Origen, OrigenAdmin)
admin.site.register(RutaAlimentadora, RutaAlimentadoraAdmin)
admin.site.register(TipoDia,TipoDiaAdmin)
admin.site.register(ListaDias,ListaDiasAdmin)
admin.site.register(HorarioRecorrido,HorarioRecorridoAdmin)
admin.site.register(Usuario,UsuarioAdmin)
admin.site.register(TiempoAsignacion,TiempoAsignacionAdmin)
admin.site.register(BusAlimentador, BusAlimentadorAdmin)
admin.site.register(Despacho, DespachoAdmin)
#admin.site.register(BusesDisponibles)
#admin.site.register(HorarioOperador)
admin.site.register(Operador)


