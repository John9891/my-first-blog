# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Origen(models.Model):
    CodOrigen = models.IntegerField(primary_key=True)
    NombreOrigen = models.CharField(max_length=45)

    class Meta:
        db_table = 'Origen'
        ordering = ['CodOrigen']
        verbose_name_plural = 'Origen'

    def __unicode__(self):
        return '%i' '%s' % (self.CodOrigen, self.NombreOrigen)


class RutaAlimentadora(models.Model):
    CodRuta = models.IntegerField(primary_key=True)
    NombreRuta = models.CharField(max_length=45)
    CodOrigen = models.ForeignKey(Origen)
    Area = models.DecimalField(max_digits=5, decimal_places=2)
    UltimoDespacho = models.TimeField(blank=True, null=True)

    class Meta:
        db_table = 'RutaAlimentadora'
        ordering = ['CodRuta']
        verbose_name_plural = 'RutaAlimentadora'

    def __unicode__(self):
        return '%i' % (self.CodRuta,)


class TipoDia(models.Model):
    TipoDia = models.IntegerField(primary_key=True)
    NombreTipoDia = models.CharField(max_length=45)

    class Meta:
        db_table = 'TipoDia'
        ordering = ['TipoDia']
        verbose_name_plural = 'TipoDia'

    def __unicode__(self):
        return '%i' % (self.TipoDia,)


class ListaDias(models.Model):
    CodDia = models.AutoField(primary_key=True)
    Fecha = models.DateField()
    TipoDia = models.ForeignKey(TipoDia)

    class Meta:
        db_table = 'ListaDias'
        ordering = ['CodDia']
        verbose_name_plural = 'ListaDias'

    def __unicode__(self):
        return '%i' % (self.CodDia,)


class HorarioRecorrido(models.Model):
    CodFranja = models.IntegerField(primary_key=True)
    CodRuta = models.ForeignKey(RutaAlimentadora)
    HoraInicio = models.TimeField()
    HoraFin = models.TimeField()
    TiempoEstimado = models.TimeField()
    TipoDia = models.ForeignKey(TipoDia)
    Franja = models.CharField(max_length=45)

    class Meta:
        db_table = 'HorarioRecorrido'
        ordering = ['CodFranja']
        verbose_name_plural = 'HorarioRecorrido'

    def __unicode__(self):
        return '%i' % (self.CodFranja,)


class Usuario(models.Model):
    NumAcceso = models.AutoField(primary_key=True)
    UID = models.CharField(max_length=45)
    FechaAcceso = models.DateField()
    HoraAcceso = models.TimeField()
    CodRuta = models.ForeignKey(RutaAlimentadora)
    PasajerosEspera = models.IntegerField()
    DensidadPasajeros = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'Usuario'
        ordering = ['NumAcceso']
        verbose_name_plural = 'Usuario'

    def __unicode__(self):
        return '%i' % (self.NumAcceso,)


class BusAlimentador(models.Model):
    NumeroBus = models.IntegerField(primary_key=True)
    CodRuta = models.ForeignKey(RutaAlimentadora, blank=True, null=True)
    Estado = models.CharField(max_length=45, blank=True, null=True)
    CapacidadBus = models.IntegerField()
    NumDespacho = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'BusAlimentador'
        ordering = ['NumeroBus']
        verbose_name_plural = 'BusAlimentador'

    def __unicode__(self):
        #return '%i' '%i' '%s' '%i' '%i' % (self.NumeroBus, self.CodRuta, self.Estado, self.CapacidadBus, self.NumDespacho,)
        return '%i' % (self.NumeroBus,)

class TiempoAsignacion(models.Model):
    NumSolicitud = models.AutoField(primary_key=True)
    CodRuta = models.ForeignKey(RutaAlimentadora, blank=True, null=True)
    Fecha = models.DateField()
    Hora = models.TimeField()
    TiempoEspera = models.TimeField(blank=True, null=True)
    NumeroBus = models.ForeignKey(BusAlimentador, blank=True, null=True)
    Despachado = models.IntegerField(default=0)

    class Meta:
        db_table = 'TiempoAsignacion'
        ordering = ['NumSolicitud']
        verbose_name_plural = 'TiempoAsignacion'

    def __unicode__(self):
        return '%s' '%s' '%s' '%s' '%s' % (self.NumSolicitud, self.CodRuta, self.Fecha, self.Hora, self.TiempoEspera)


#class BusesDisponibles(models.Model):
#    IdDisponibilidad = models.AutoField(primary_key=True)
#    Disponibilidad = models.IntegerField()
#    Fecha = models.DateField()
#    Hora = models.TimeField()
#    TiempoEspera = models.TimeField(blank=True, null=True)
#    CodOrigen = models.ForeignKey(Origen)

#    class Meta:
#        db_table = 'BusesDisponibles'
#        verbose_name_plural = 'BusesDisponibles'

#    def __unicode__(self):
#        return '%i' % (self.IdDisponibilidad,)


class HorarioOperador(models.Model):
    TipoHorario = models.IntegerField(primary_key=True)
    Jornada = models.CharField(max_length=45)
    TipoDia = models.CharField(max_length=45)

    class Meta:
        db_table = 'HorarioOperador'
        verbose_name_plural='HorarioOperador'

    def __unicode__(self):
        return '%i' % (self.TipoHorario,)


class Operador(models.Model):
    DocOperador = models.IntegerField(primary_key=True)
    Nombres = models.CharField(max_length=45)
    Apellidos = models.CharField(max_length=45)
    Perfil = models.CharField(max_length=45)
    CodOrigen = models.ForeignKey(Origen)
    Clave = models.CharField(max_length=45)
    TipoHorario = models.ForeignKey(HorarioOperador)

    class Meta:
        db_table = 'Operador'
        verbose_name_plural = 'Operadores'

    def __unicode__(self):
        return '%i' % (self.DocOperador,)


class Despacho(models.Model):
    NumDespacho = models.AutoField(primary_key=True)
    CodRuta = models.ForeignKey (RutaAlimentadora)
    NumeroBus = models.ForeignKey(BusAlimentador)
    FechaDespacho = models.DateField()
    HoraDespacho = models.TimeField()
    HoraLlegada = models.TimeField(blank=True, null=True)
    Delay = models.TimeField(blank=True, null=True)
    FactorConfiabilidad = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    CargaPasajeros = models.IntegerField()
    Frecuencia = models.TimeField()
    HoraLlegadaEsperada = models.TimeField(max_length=45)
    Tope = models.IntegerField()

    class Meta:
        db_table = 'Despacho'
        verbose_name_plural = 'Despacho'

    def __unicode__(self):
        return '%i' % (self.NumDespacho,)
