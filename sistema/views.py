# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect 
from django.http import HttpResponseRedirect
from sistema.models import *
import datetime
import time
from datetime import timedelta
from django.core.mail import send_mail
from sistema.forms import FormularioContactos, TiempoAsignacionForm, BusAlimentadorForm, DespachoForm
from django.db.models import Max
from django.contrib.auth.decorators import login_required


def buscar(request):
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
    if not q:
        errors.append('Por favor introduce un término de búsqueda.')
    elif len(q) > 14:
        errors.append('Por favor introduce un término de búsqueda menor a 20 caracteres.')
    else:
        usuarios = Usuario.objects.filter(UID__contains=q)
        return render(request, 'resultados.html',  {'usuarios': usuarios, 'query': q})
    return render(request, 'formulario_buscar.html', {'errors'  : errors})


def contactos(request):
    if request.method == 'POST':
        form = FormularioContactos(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                cd['asunto'],
                cd['mensaje'],
                cd.get('email', 'noreply@example.com'),
                ['siteowner@example.com'],)
            return HttpResponseRedirect('/contactos/gracias/')
    else:
        form = FormularioContactos()
    return render(request, 'formulario_contactos.html', {'form': form})


num_solicitud_81, fecha_81, hora_81, tiempo_81, despacho_81 = 0, 0, 0, 0, 0
num_solicitud_82, fecha_82, hora_82, tiempo_82, despacho_82 = 0, 0, 0, 0, 0
num_solicitud_83, fecha_83, hora_83, tiempo_83, despacho_83 = 0, 0, 0, 0, 0
estado_81, estado_82, estado_83 = False, False, False


def sumar_hora(hora1,hora2):
    formato = "%H:%M:%S"
    lista = hora2.split(":")
    hora=int(lista[0])
    minuto=int(lista[1])
    segundo=int(lista[2])
    h1 = datetime.datetime.strptime(hora1, formato)
    dh = timedelta(hours=hora) 
    dm = timedelta(minutes=minuto)          
    ds = timedelta(seconds=segundo) 
    resultado1 =h1 + ds
    resultado2 = resultado1 + dm
    resultado = resultado2 + dh
    resultado=resultado.strftime(formato)
    return str(resultado)

def restar_hora(hora1,hora2):
        formato = "%H:%M:%S"
        h1 = datetime.datetime.strptime(hora1, formato)
        h2 = datetime.datetime.strptime(hora2, formato)
        if h1 > h2:
            resultado = h1 - h2
            return str(resultado)
        else:
            return str("00:00:00")


def solicitudes(request):
    if not request.user.is_authenticated():
        return redirect('homepage')        
        #return render(request, 'homepage.html')
        #return redirect('/login/?next=%s' % request.path)
    global num_solicitud_81, fecha_81, hora_81, tiempo_81, despacho_81
    global num_solicitud_82, fecha_82, hora_82, tiempo_82, despacho_82
    global num_solicitud_83, fecha_83, hora_83, tiempo_83, despacho_83
    global estado_81, estado_82, estado_83
    
    #Calcula el tiempo de espera de las solicitudes que no han sido despachadas
    hora_actual = time.strftime("%H:%M:%S")
    lista_espera = []    
    lista_num_solic = []
    q_solic_espera = TiempoAsignacion.objects.filter(Despachado=0).values('NumSolicitud')
    tam_espera = len(q_solic_espera)
    for i in range(tam_espera):
        i_num_solic = q_solic_espera[i]['NumSolicitud']
        lista_num_solic.append(i_num_solic)
    for i in range(tam_espera):
        t_espera = TiempoAsignacion.objects.filter(NumSolicitud=lista_num_solic[i]).values('Hora')
        ruta_espera = t_espera[0]['Hora']    
        lista_espera.append(ruta_espera)
    for i in range(tam_espera):
        tiempo_espera = restar_hora(hora_actual,str(lista_espera[i]))
        ins_tiempo_espera = TiempoAsignacion.objects.filter(NumSolicitud=lista_num_solic[i]).update(TiempoEspera=str(tiempo_espera))
        
    try:
        q_solicitud_81 = TiempoAsignacion.objects.filter(CodRuta=81).values('NumSolicitud').aggregate(Max('NumSolicitud'))
        num_solicitud_81 = q_solicitud_81['NumSolicitud__max']
        q_fecha_81 = TiempoAsignacion.objects.filter(CodRuta=81, NumSolicitud=num_solicitud_81).values('Fecha')
        fecha_81 = q_fecha_81[0]['Fecha']
        q_hora_81 = TiempoAsignacion.objects.filter(CodRuta=81, NumSolicitud=num_solicitud_81).values('Hora')
        hora_81 = q_hora_81[0]['Hora']
        q_tiempo_81 = TiempoAsignacion.objects.filter(CodRuta=81, NumSolicitud=num_solicitud_81).values('TiempoEspera')
        tiempo_81 = q_tiempo_81[0]['TiempoEspera']
        q_despacho_81 = TiempoAsignacion.objects.filter(CodRuta=81, NumSolicitud=num_solicitud_81).values('Despachado')
        despacho_81 = q_despacho_81[0]['Despachado']
        if despacho_81 == 1:
            estado_81 = True
        elif despacho_81 == 0:
            estado_81 = False                

    except:
        num_solicitud_81, fecha_81, hora_81, tiempo_81, despacho_81 = 0, 0, 0, 0, 0

    try:
        q_solicitud_82 = TiempoAsignacion.objects.filter(CodRuta=82).values('NumSolicitud').aggregate(Max('NumSolicitud'))
        num_solicitud_82 = q_solicitud_82['NumSolicitud__max']
        q_fecha_82 = TiempoAsignacion.objects.filter(CodRuta=82, NumSolicitud=num_solicitud_82).values('Fecha')
        fecha_82 = q_fecha_82[0]['Fecha']
        q_hora_82 = TiempoAsignacion.objects.filter(CodRuta=82, NumSolicitud=num_solicitud_82).values('Hora')
        hora_82 = q_hora_82[0]['Hora']
        q_tiempo_82 = TiempoAsignacion.objects.filter(CodRuta=82, NumSolicitud=num_solicitud_82).values('TiempoEspera')
        tiempo_82 = q_tiempo_82[0]['TiempoEspera']
        q_despacho_82 = TiempoAsignacion.objects.filter(CodRuta=82, NumSolicitud=num_solicitud_82).values('Despachado')
        despacho_82 = q_despacho_82[0]['Despachado']
        if despacho_82 == 1:
            estado_82 = True
        elif despacho_82 == 0:
            estado_82 = False

    except:
        num_solicitud_82, fecha_82, hora_82, tiempo_82, despacho_82 = 0, 0, 0, 0, 0

    try:
        q_solicitud_83 = TiempoAsignacion.objects.filter(CodRuta=83).values('NumSolicitud').aggregate(Max('NumSolicitud'))
        num_solicitud_83 = q_solicitud_83['NumSolicitud__max']
        q_fecha_83 = TiempoAsignacion.objects.filter(CodRuta=83, NumSolicitud=num_solicitud_83).values('Fecha')
        fecha_83 = q_fecha_83[0]['Fecha']
        q_hora_83 = TiempoAsignacion.objects.filter(CodRuta=83, NumSolicitud=num_solicitud_83).values('Hora')
        hora_83 = q_hora_83[0]['Hora']
        q_tiempo_83 = TiempoAsignacion.objects.filter(CodRuta=83, NumSolicitud=num_solicitud_83).values('TiempoEspera')
        tiempo_83 = q_tiempo_83[0]['TiempoEspera']
        q_despacho_83 = TiempoAsignacion.objects.filter(CodRuta=83, NumSolicitud=num_solicitud_83).values('Despachado')
        despacho_83 = q_despacho_83[0]['Despachado']
        if despacho_83 == 1:
            estado_83 = True
        elif despacho_83 == 0:
            estado_83 = False

    except:
        num_solicitud_83, fecha_83, hora_83, tiempo_83, despacho_83 = 0, 0, 0, 0, 0

    #Muestra la lista de las ultimas rutas despachadas
    try:
        solic_despachadas = TiempoAsignacion.objects.filter(Despachado=1).order_by('-NumSolicitud').values('NumSolicitud')[:10]
        num_solic_desp = len(solic_despachadas)
        lista_solic = []
        lista_solic_rut = []
        lista_solic_fec = []
        lista_solic_hora = []
        lista_solic_espera = []
        for i in range(num_solic_desp):
            solicitudes = solic_despachadas[i]['NumSolicitud']
            lista_solic.append(solicitudes)
        for i in range(num_solic_desp):
            cod_solic_ruta = TiempoAsignacion.objects.filter(NumSolicitud=lista_solic[i]).values('CodRuta')
            cod_solic_fecha = TiempoAsignacion.objects.filter(NumSolicitud=lista_solic[i]).values('Fecha')
            cod_solic_hora = TiempoAsignacion.objects.filter(NumSolicitud=lista_solic[i]).values('Hora')
            cod_solic_espera = TiempoAsignacion.objects.filter(NumSolicitud=lista_solic[i]).values('TiempoEspera')
            cod_solic_rutas = cod_solic_ruta[0]['CodRuta']
            cod_solic_fechas = cod_solic_fecha[0]['Fecha']
            cod_solic_horas = cod_solic_hora[0]['Hora']
            cod_solic_esperas = cod_solic_espera[0]['TiempoEspera']
            lista_solic_rut.append(cod_solic_rutas)
            lista_solic_fec.append(cod_solic_fechas)
            lista_solic_hora.append(cod_solic_horas)
            lista_solic_espera.append(cod_solic_esperas)

    except:
        lista_solic, lista_solic_rut, lista_solic_fec, lista_solic_hora, lista_solic_espera = [],[],[],[],[]

    try:
        #Busca los datos de las rutas en tránsito
        buses_transito = BusAlimentador.objects.filter(Estado='En transito').values('NumeroBus')        
        num_buses_tran = len(buses_transito)
        lista_buses=[]
        lista_rutas=[]
        lista_capacidades=[]
        for i in range (num_buses_tran):
            ruta = buses_transito[i]['NumeroBus']
            lista_buses.append(ruta)
        for i in range (num_buses_tran):
            cod_rutas = BusAlimentador.objects.filter(NumeroBus=lista_buses[i]).values('CodRuta')
            cod_capacidades = BusAlimentador.objects.filter(NumeroBus=lista_buses[i]).values('CapacidadBus')
            cod_ruta = cod_rutas[0]['CodRuta']
            cod_capacidad = cod_capacidades[0]['CapacidadBus']
            lista_rutas.append(cod_ruta)
            lista_capacidades.append(cod_capacidad)

    except:
        lista_buses, lista_rutas, lista_capacidades = [],[],[]


    return render(request, 'solicitudes.html',
        {'num_solicitud_81': num_solicitud_81,
         'fecha_81': fecha_81, 'hora_81': hora_81,
         'tiempo_81': tiempo_81, 'despacho_81': despacho_81,
         'num_solicitud_82': num_solicitud_82,
         'fecha_82': fecha_82, 'hora_82': hora_82,
         'tiempo_82': tiempo_82, 'despacho_82': despacho_82,
         'num_solicitud_83': num_solicitud_83,
         'fecha_83': fecha_83, 'hora_83': hora_83,
         'estado_81': estado_81, 'estado_82': estado_82, 'estado_83': estado_83,
         'lista_solic': lista_solic, 'lista_solic_rut': lista_solic_rut, 'lista_solic_fec': lista_solic_fec,
         'lista_solic_hora': lista_solic_hora, 'lista_solic_espera':lista_solic_espera,
         'lista_buses': lista_buses, 'lista_rutas': lista_rutas, 'lista_capacidades': lista_capacidades,         
         'tiempo_83': tiempo_83, 'despacho_83': despacho_83})


def home(request):
    return render(request, 'home.html')


def javascript(request):
    return render(request, 'javascript.html')
num_bus = 0
tipo = None


def despachar(request, cod_ruta):
    if not request.user.is_authenticated():
        return redirect('homepage')

    fecha = time.strftime("%Y-%m-%d")
    hora = time.strftime("%H:%M:%S")

    if cod_ruta == '81':
        if request.method == 'POST':
            form = TiempoAsignacionForm(request.POST)            
            if form.is_valid():                
                num_bus = form.cleaned_data['NumeroBus']                
                solicitud = TiempoAsignacion.objects.get(NumSolicitud=num_solicitud_81)
                solicitud.Despachado = 1                
                solicitud.NumeroBus = num_bus
                solicitud.save()
                #Registra la ruta que está realizando el bus y cambia el estado a "En transito"                 
                bus = TiempoAsignacion.objects.filter(NumSolicitud=num_solicitud_81).values('NumeroBus')
                bus_transito = bus[0]['NumeroBus']
                bus_ruta = BusAlimentador.objects.filter(NumeroBus=bus_transito).update(CodRuta=cod_ruta)                               
                bus_entransito = BusAlimentador.objects.filter(NumeroBus=bus_transito).update(Estado='En transito')
                                              #Ingreso de datos en tabla Despacho
                #Se calcula la carga de pasajeros con los pasajeros en espera
                acceso = Usuario.objects.filter(CodRuta=cod_ruta).values('NumAcceso').aggregate(Max('NumAcceso'))
                ult_acceso = acceso['NumAcceso__max']
                pasaj = Usuario.objects.filter(NumAcceso=ult_acceso).values('PasajerosEspera')
                pasaj_espera = pasaj[0]['PasajerosEspera']
                # Se halla el dia y franja actual
                dia = ListaDias.objects.filter(Fecha=fecha).values('TipoDia')
                tipo_dia = dia[0]['TipoDia']                               
                tiempo_est = HorarioRecorrido.objects.filter(CodRuta=81, TipoDia=tipo_dia, HoraInicio__lte=hora, HoraFin__gte=hora).values('TiempoEstimado')
                tiempo_estimado = tiempo_est[0]['TiempoEstimado']                
                #Se calcula tiempo de llegada esperado
                tiempo_esperado = sumar_hora(hora,str(tiempo_estimado))
                #Se calcula si el bus va a tope o no
                bus_capac = BusAlimentador.objects.filter(NumeroBus=bus_transito).values('CapacidadBus')
                bus_capacidad = bus_capac[0]['CapacidadBus']
                registro_carga = pasaj_espera - bus_capacidad
                if registro_carga > 0:
                    carga_pasajeros = bus_capacidad
                    tope = 1
                    pasaj_espera = pasaj_espera - registro_carga
                    act_pasajeros = Usuario.objects.filter(NumAcceso=ult_acceso).update(PasajerosEspera=pasaj_espera)
                else:
                    carga_pasajeros = pasaj_espera
                    tope = 0
                    pasaj_espera = 0
                    act_pasajeros = Usuario.objects.filter(NumAcceso=ult_acceso).update(PasajerosEspera=pasaj_espera)
                #Se calcula la frecuencia comparando la hora de salida del despacho anterior
                ult_num_desp = Despacho.objects.filter(CodRuta_id=81).aggregate(Max('NumDespacho'))
                ult_num_despacho = ult_num_desp['NumDespacho__max']
                if ult_num_despacho == None:
                    frecuencia = '00:00:00'
                else:
                    ult_desp = Despacho.objects.filter(CodRuta_id=81, NumDespacho=ult_num_despacho).values('HoraDespacho')
                    ult_despacho = ult_desp[0]['HoraDespacho']
                    frecuencia = restar_hora(hora,str(ult_despacho))
                Despacho_81 = Despacho(CodRuta_id=81,NumeroBus_id=bus_transito, FechaDespacho=fecha, HoraDespacho=hora, CargaPasajeros=carga_pasajeros, Frecuencia=frecuencia, HoraLlegadaEsperada=tiempo_esperado, Tope=tope)
                Despacho_81.save()
                num_des = Despacho_81.NumDespacho
                ins_despacho_bus = BusAlimentador.objects.filter(NumeroBus=bus_transito).update(NumDespacho=num_des)
                return HttpResponseRedirect('/login/solicitud/') 
        else:
            form = TiempoAsignacionForm(initial={'NumSolicitud': num_solicitud_81, 'CodRuta':81,})
        return render(request, 'despachar_ruta.html', {'form': form, 'fecha':fecha, 'hora': hora})

    elif cod_ruta == '82':
        if request.method == 'POST':
            form = TiempoAsignacionForm(request.POST)
            if form.is_valid():                
                num_bus = form.cleaned_data['NumeroBus']                
                solicitud = TiempoAsignacion.objects.get(NumSolicitud=num_solicitud_82)
                solicitud.Despachado = 1                
                solicitud.NumeroBus = num_bus
                solicitud.save()
                #Registra la ruta que está realizando el bus y cambia el estado a "En transito"                 
                bus = TiempoAsignacion.objects.filter(NumSolicitud=num_solicitud_82).values('NumeroBus')
                bus_transito = bus[0]['NumeroBus']
                bus_ruta = BusAlimentador.objects.filter(NumeroBus=bus_transito).update(CodRuta=cod_ruta)                               
                bus_entransito = BusAlimentador.objects.filter(NumeroBus=bus_transito).update(Estado='En transito')
                                              #Ingreso de datos en tabla Despacho
                #Se calcula la carga de pasajeros con los pasajeros en espera
                acceso = Usuario.objects.filter(CodRuta=cod_ruta).values('NumAcceso').aggregate(Max('NumAcceso'))
                ult_acceso = acceso['NumAcceso__max']
                pasaj = Usuario.objects.filter(NumAcceso=ult_acceso).values('PasajerosEspera')
                pasaj_espera = pasaj[0]['PasajerosEspera']
                # Se halla el dia y franja actual
                dia = ListaDias.objects.filter(Fecha=fecha).values('TipoDia')
                tipo_dia = dia[0]['TipoDia']                               
                tiempo_est = HorarioRecorrido.objects.filter(CodRuta=cod_ruta, TipoDia=tipo_dia, HoraInicio__lte=hora, HoraFin__gte=hora).values('TiempoEstimado')
                tiempo_estimado = tiempo_est[0]['TiempoEstimado']                
                #Se calcula tiempo de llegada esperado
                tiempo_esperado = sumar_hora(hora,str(tiempo_estimado))
                #Se calcula si el bus va a tope o no
                bus_capac = BusAlimentador.objects.filter(NumeroBus=bus_transito).values('CapacidadBus')
                bus_capacidad = bus_capac[0]['CapacidadBus']
                registro_carga = pasaj_espera - bus_capacidad
                if registro_carga > 0:
                    carga_pasajeros = bus_capacidad
                    tope = 1
                    pasaj_espera = pasaj_espera - registro_carga
                    act_pasajeros = Usuario.objects.filter(NumAcceso=ult_acceso).update(PasajerosEspera=pasaj_espera)
                else:
                    carga_pasajeros = pasaj_espera
                    tope = 0
                    pasaj_espera = 0
                    act_pasajeros = Usuario.objects.filter(NumAcceso=ult_acceso).update(PasajerosEspera=pasaj_espera)
                #Se calcula la frecuencia comparando la hora de salida del despacho anterior (si es el primer despacho del dia
                #registra como frecuencia '00:00:00)
                ult_num_desp = Despacho.objects.filter(CodRuta_id=cod_ruta).aggregate(Max('NumDespacho'))
                ult_num_despacho = ult_num_desp['NumDespacho__max']
                if ult_num_despacho == None:
                    frecuencia = '00:00:00'
                else:
                    ult_desp = Despacho.objects.filter(CodRuta_id=cod_ruta, NumDespacho=ult_num_despacho).values('HoraDespacho')
                    ult_despacho = ult_desp[0]['HoraDespacho']
                    frecuencia = restar_hora(hora,str(ult_despacho))
                Despacho_82 = Despacho(CodRuta_id=cod_ruta,NumeroBus_id=bus_transito, FechaDespacho=fecha, HoraDespacho=hora, CargaPasajeros=carga_pasajeros, Frecuencia=frecuencia, HoraLlegadaEsperada=tiempo_esperado, Tope=tope)
                Despacho_82.save()
                num_des = Despacho_82.NumDespacho
                ins_despacho_bus = BusAlimentador.objects.filter(NumeroBus=bus_transito).update(NumDespacho=num_des)
                return HttpResponseRedirect('/login/solicitud/')            
        else:
            form = TiempoAsignacionForm(initial={'NumSolicitud': num_solicitud_82, 'CodRuta':82,})
        return render(request, 'despachar_ruta.html', {'form': form, 'fecha':fecha, 'hora': hora})

    elif cod_ruta == '83':
        if request.method == 'POST':
            form = TiempoAsignacionForm(request.POST)
            if form.is_valid():                
                num_bus = form.cleaned_data['NumeroBus']                
                solicitud = TiempoAsignacion.objects.get(NumSolicitud=num_solicitud_83)
                solicitud.Despachado = 1                
                solicitud.NumeroBus = num_bus
                solicitud.save()
                #Registra la ruta que está realizando el bus y cambia el estado a "En transito"                 
                bus = TiempoAsignacion.objects.filter(NumSolicitud=num_solicitud_83).values('NumeroBus')
                bus_transito = bus[0]['NumeroBus']
                bus_ruta = BusAlimentador.objects.filter(NumeroBus=bus_transito).update(CodRuta=cod_ruta)                               
                bus_entransito = BusAlimentador.objects.filter(NumeroBus=bus_transito).update(Estado='En transito')
                                              #Ingreso de datos en tabla Despacho
                #Se calcula la carga de pasajeros con los pasajeros en espera
                acceso = Usuario.objects.filter(CodRuta=cod_ruta).values('NumAcceso').aggregate(Max('NumAcceso'))
                ult_acceso = acceso['NumAcceso__max']
                pasaj = Usuario.objects.filter(NumAcceso=ult_acceso).values('PasajerosEspera')
                pasaj_espera = pasaj[0]['PasajerosEspera']
                # Se halla el dia y franja actual
                dia = ListaDias.objects.filter(Fecha=fecha).values('TipoDia')
                tipo_dia = dia[0]['TipoDia']                               
                tiempo_est = HorarioRecorrido.objects.filter(CodRuta=cod_ruta, TipoDia=tipo_dia, HoraInicio__lte=hora, HoraFin__gte=hora).values('TiempoEstimado')
                tiempo_estimado = tiempo_est[0]['TiempoEstimado']                
                #Se calcula tiempo de llegada esperado
                tiempo_esperado = sumar_hora(hora,str(tiempo_estimado))
                #Se calcula si el bus va a tope o no
                bus_capac = BusAlimentador.objects.filter(NumeroBus=bus_transito).values('CapacidadBus')
                bus_capacidad = bus_capac[0]['CapacidadBus']
                registro_carga = pasaj_espera - bus_capacidad
                if registro_carga > 0:
                    carga_pasajeros = bus_capacidad
                    tope = 1
                    pasaj_espera = pasaj_espera - registro_carga
                    act_pasajeros = Usuario.objects.filter(NumAcceso=ult_acceso).update(PasajerosEspera=pasaj_espera)
                else:
                    carga_pasajeros = pasaj_espera
                    tope = 0
                    pasaj_espera = 0
                    act_pasajeros = Usuario.objects.filter(NumAcceso=ult_acceso).update(PasajerosEspera=pasaj_espera)
                #Se calcula la frecuencia comparando la hora de salida del despacho anterior
                ult_num_desp = Despacho.objects.filter(CodRuta_id=cod_ruta).aggregate(Max('NumDespacho'))
                ult_num_despacho = ult_num_desp['NumDespacho__max']
                if ult_num_despacho == None:
                    frecuencia = '00:00:00'
                else:
                    ult_desp = Despacho.objects.filter(CodRuta_id=cod_ruta, NumDespacho=ult_num_despacho).values('HoraDespacho')
                    ult_despacho = ult_desp[0]['HoraDespacho']
                    frecuencia = restar_hora(hora,str(ult_despacho))
                Despacho_83 = Despacho(CodRuta_id=cod_ruta,NumeroBus_id=bus_transito, FechaDespacho=fecha, HoraDespacho=hora, CargaPasajeros=carga_pasajeros, Frecuencia=frecuencia, HoraLlegadaEsperada=tiempo_esperado, Tope=tope)
                Despacho_83.save()
                num_des = Despacho_83.NumDespacho
                ins_despacho_bus = BusAlimentador.objects.filter(NumeroBus=bus_transito).update(NumDespacho=num_des)
                return HttpResponseRedirect('/login/solicitud/')            
        else:
            form = TiempoAsignacionForm(initial={'NumSolicitud': num_solicitud_83, 'CodRuta':83,})
        return render(request, 'despachar_ruta.html', {'form': form, 'fecha':fecha, 'hora': hora})


def llegada(request, num_bus):
    if not request.user.is_authenticated():
        return redirect('homepage')

    fecha = time.strftime("%Y-%m-%d")
    hora = time.strftime("%H:%M:%S")
    sin_ruta = ''

    if request.method == 'POST':
        form = DespachoForm(request.POST)
        if form.is_valid():
            #Se busca el número de despacho en la tabla BusAlimentador
            ult_despacho_bus = BusAlimentador.objects.filter(NumeroBus=num_bus).values('NumDespacho')
            ult_desp_bus = ult_despacho_bus[0]['NumDespacho']                      
            #Se inserta la hora de llegada en tabla Despacho
            bus_ruta = Despacho.objects.filter(NumDespacho=ult_desp_bus, NumeroBus=num_bus).update(HoraLlegada=hora)
            #Se calcula y se inserta el delay entre la hora de llegada esperada y la hora de llegada
            hora_esper = Despacho.objects.filter(NumDespacho=ult_desp_bus, NumeroBus=num_bus).values('HoraLlegadaEsperada')
            hora_esperada = hora_esper[0]['HoraLlegadaEsperada']
            delay = restar_hora(hora,str(hora_esperada))
            ins_delay = Despacho.objects.filter(NumDespacho=ult_desp_bus, NumeroBus=num_bus).update(Delay=delay)
            #Calcula el factor de confiabilidad
            valor_conf = datetime.time(0, 20, 0)
            confiab = 0
            delays_lista = []
            ruta_recor = Despacho.objects.filter(NumDespacho=ult_desp_bus, NumeroBus=num_bus).values('CodRuta_id')
            ruta_recorrida = ruta_recor[0]['CodRuta_id']
            #Verifica si hay suficientes despacho de la misma ruta para evaluar el factor
            num_viajes = Despacho.objects.filter(CodRuta=ruta_recorrida).values('Delay')
            numero_viajes = len(num_viajes)
            if numero_viajes > 6:
                ult_retardos = Despacho.objects.filter(CodRuta=ruta_recorrida).order_by('-NumDespacho').values('Delay')[:5]
                delays_lista = [ult_retardos[0]['Delay'],ult_retardos[1]['Delay'],ult_retardos[2]['Delay'],ult_retardos[3]['Delay'],ult_retardos[4]['Delay']]
                for i in range(0,4):
                    if valor_conf > delays_lista[i]:
                        confiab += 1
                    else:
                        confiab = confiab
                fac_conf = confiab/5.0
            else:
                ult_retardos = Despacho.objects.filter(CodRuta=ruta_recorrida).order_by('-NumDespacho').values('Delay')
                tam = len(ult_retardos)
                for i in range(tam):
                    lista = ult_retardos[0]['Delay']
                    delays_lista.append(lista)

                for i in range(0,numero_viajes):
                    if valor_conf > delays_lista[i]:
                        confiab += 1
                    else:
                        confiab=confiab
                fac_conf = confiab/numero_viajes                
            bus_ruta = Despacho.objects.filter(NumDespacho=ult_desp_bus, NumeroBus=num_bus).update(FactorConfiabilidad=fac_conf)
            #Se cambia el estado del bus a "Disponible y se elimina la ruta que realizo"
            bus__sin_ruta = BusAlimentador.objects.filter(NumeroBus=num_bus).update(CodRuta='')
            bus_sin_despacho = BusAlimentador.objects.filter(NumeroBus=num_bus).update(NumDespacho=0)                            
            bus_disponible = BusAlimentador.objects.filter(NumeroBus=num_bus).update(Estado='DISPONIBLE')



            return HttpResponseRedirect('/login/solicitud/')        
    else:
        form = DespachoForm()
    return render(request, 'llegada_bus.html', {'form': form, 'hora':hora, 'numero_bus': num_bus,})

