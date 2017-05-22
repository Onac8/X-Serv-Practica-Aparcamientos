# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import *
from django.views.decorators.csrf import csrf_exempt
from aparcamientos.models import *
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth import logout, authenticate, login
from django.db import models
#from urllib.parse import unquote_plus


#Listas con enlaces dependiendo de la pagina a servir------------
def linksHome():
    links = []
    links.append("<a href='/aparcamientos'>TODOS</a>")
    links.append("<a href='/about'>ABOUT</a>")
    return links

def linksOther():
    links = []
    links.append ("<a href='/'>INICIO</a>")
    links.append("<a href='/aparcamientos'>TODOS</a>")
    links.append("<a href='/about'>ABOUT</a>")
    return links
#----------------------------------------------------------------

#FORM LOG IN/OUT-------------------------------------------------
@csrf_exempt
def logInOut(request): #Form para login o enlace para logout.
    if request.user.is_authenticated():
        log = "<span id= 'logIn' class= '.t-center'>Logged in as " + request.user.username + ". <a href='/logout'> Logout </a><br></span>"
    else:
        log = "<form class='.t-left' action='/login' method='POST'>" \
            + "<label>You aren't logged. Please login<br></label>" \
            + "NICK:  <input type='text' name='name'><br>" \
            + "PASS: <input type='password' name='pass'><br> "\
            + "<input type='submit' value='Submit'></form>"
    return log
#----------------------------------------------------------------

#FORMULARIOS, BOTONES Y BUSCADOR-----------------------------------------------------------
@csrf_exempt
def form(tipo, info, info2): #formularios, botones y buscador
    if tipo == "add":
        form = "<form action='/" + info + "' method='POST'>" \
            + "<button type='submit' name='Add' value='" + info2 + "'> Add </button></form>"

    if tipo == "accesible":
        form = "<form method='POST'><button type='submit' name='boton' value='ACCESIBLES'>Parkings Accesibles</button></form>"

    if tipo == "accesible2": #con value = 0, indicando que vuelva a mostrar todo
        form = "<form method='POST'><button type='submit' name='boton' value='COMENTADOS'>Todos</button><form>"

    if tipo == "tituloPersonal":
        form = "<form id='formularioTitulo' action='/" + info + "' method='POST'>" \
            + "Nombre de pagina personal<br><input type='text' name='Titulo'>" \
            + "<input type='submit' value='Enviar'></form>"

    elif tipo == "distrito":
        form = "<form method='POST'>Distrito: <input type='text' name='Distrito'>" \
            + "<input type='submit' value='Filter'></form>"

    return form
#------------------------------------------------------------------------------------------

#TITULOS O CONTENIDOS-----------------------------------------------------------------------
def texto(tipo): #funcion que sirve diferentes tipos de titulos o contenidos
    if (tipo == "comentados"):
        return "Aparcamientos mas comentados"

    elif (tipo == "accesible"):
        return "Aparcamientos accesibles"

    elif (tipo == "no_parks"):
        return "No hay Aparcamientos en la base de datos. CaRGALOS"

    elif (tipo == "about"):
        return "<p>¿Que es Parking Simulator [PS]?<p>"\
        + "<p>En esta página podrás seleccionar aparcamientos de la base de datos de la Comunidad de Madrid.</p>" \
        + "<p>Para ello, simplemente debes loguearte en la página mediante nuestro sencillo formulario. Una vez hecho, "\
        + "dispondrás de una página personal, donde se encontrarán tus aparcamientos seleccionados. Estos los podrás seleccionar" \
        + "sencillamente pulsando el boton 'ADD' que está situado al lado de cada aparcamiento. Se podrá obtener mas informacion " \
        + "de cada aparcamiento pulsando sobre su enlace 'mas info...'." \
        + "<p>Segun entramos en la pagina, podemos apreciar podremos distinguir un banner, un menu que nos llevara a 'TODOS los" \
        + "aparcamientos' o a este recurso 'ABOUT'. La página nos dará la opcion de descargar todos los aparcamientos del XML de " \
        + "la Comunidad de Madrid. </p>" \
        + "<p>Ademas, si estas logueado, se permite comentar cada aparcamiento (indicando por ejemplo que te pareció espacioso, "\
        + "bien posicionado, etc.). Los aparcamientos apareceran en la pagina principal filtrados por 'mas comentados' o 'accesibles'" \
        + "segun seleccionemos con el boton situado en la columna lateral.</p>"\
        + "<p>Ademas, en dicha columna (mas abajo), podremos elegir ver la pagina en formato XML. Y mas abajo, podremos ver las" \
        + "paginas personales de cada usuario, con enlaces hacia ellas </p>" \
        + "<p><br><br> DESIGNED BY: Jonathan Cano Picazo (Alias Onac8)</p>"
#---------------------------------------------------------------------------------------

########################################################################################
#####HOME###############################################################################
@csrf_exempt
def home(request): #pagina principal
    if request.method == "GET": #Ordenamos por aparcamientos mas comentados
        titulo = texto("comentados")
        boton = form("accesible","","")
        parkings = Aparcamientos.objects.all() #con all no tenemos excepcion!
        aparcamientos = parkings.order_by('-nComen')
        content = listado(aparcamientos, request, 0, request.user) #listado de parkings

    elif request.method == 'POST': #aqui tratamos solo el post del boton accesibles
        valor = request.POST ['boton']

        if (valor == "ACCESIBLES"): #Aparcamientos accesibles
            titulo = texto("accesible")
            boton = form("accesible2","","") #pasamos a mostrar boton de "ir a mas comentados"
            parkings = Aparcamientos.objects.filter(accesibilidad=1)
            aparcamientos = parkings.order_by('-nComen')
            content = listado(aparcamientos, request, 0, request.user) #listado de parkings accesibles

        else: #Aparcamientos mas comentados
            titulo = texto("comentados")
            boton = form("accesible","","") #pasamos a mostrar de nuevo boton de "ir a accesibles"
            parkings = Aparcamientos.objects.all()
            aparcamientos = parkings.order_by('-nComen')
            content = listado(aparcamientos,request, 0, request.user) #listado de parkings


    #Paginas Personales
    datos = paginasUsers()

    #Ahora renderizamos
    log = logInOut(request)
    links = linksHome() #links todos, about
    template = get_template("home.html")
    c = Context ({'log': log,
                  'links': links,
                  'boton': boton,
                  'titulo': titulo,
                  'content': content,
                  'datos': datos})
    return HttpResponse(template.render(c))


#TODOS LOS APARCAMIENTOS----------------------------------------------------------------
@csrf_exempt
def aparcamientosPS(request): #lista de parkings totales

    #Si no hay Parkings en la base de datos, los obtendremos mediante el XML
    try:
        if request.method == "GET":
            parks = Aparcamientos.objects.all()

            content=[]
            for aux in parks:
                if request.user.is_authenticated(): #aparcamiento + boton add --> parte privada
                    content.append ("<a href='aparcamientos/" + str(aux.id) + "'>" + aux.nombre + "</a>" + form("add", request.user.username, str(aux.id)))
                else:
                    content.append ("<a href='aparcamientos/" + str(aux.id) + "'>" + aux.nombre + "</a>")

        elif request.method == 'POST': #Buscador por distrito --> PONER DESPLEGABLEEEEE!!!!!
            Distrito = request.POST['name']
            #Distrito = request.body.decode('utf-8').split("=")[1] #con request.POST[name] no se puede????
            #Distrito = unquote_plus(Distrito)
            #parkings = Aparcamientos.objects.filter(distrito=Distrito)
            #for aux in parkings:
                #content.append ("<a href='/aparcamientos/" + str(aux.id) + "'>" + aux.nombre + "</a>")

        #Paginas Personales
        datos = paginasUsers()

        log = logInOut(request)
        links = linksOther()
        filtro = form("distrito", "","") #buscador por distrito

        template = get_template("aparcamientos.html")
        c = Context ({'log': log,
                      'links': links,
                      'filtro': filtro,
                      'datos' : datos,
                      'content': content})
        return HttpResponse(template.render(c))

    except Aparcamientos.DoesNotExist:
        template = get_template("aparcamientos.html")
        c = Context ({'content': texto("no_parks"),
                   'links': links,
                   'log' : log})
        return HttpResponse(template.render(c))
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
def listado(lista, request, flag, nick): #listado con todos los aparcamientos seleccionados por el user
    content = []
    for aux in lista:
        if request.user.is_authenticated(): #parte privada (con boton add)
            content.append("<a class='info' href='" + aux.url + "'> " + aux.nombre + "</a><br>" \
                + "Direccion: " + aux.direccion + "<br>" \
                + "<a class='info' href='/aparcamientos/" + aux.nombre + "'>Mas informacion...</a><br>"+ form("add", request.user.username, str(aux.id)) + "<br>")
        else: #parte publica (sin boton add)
            content.append("<a class='info' href='" + aux.url + "'> " + aux.nombre + "</a><br>" \
                + "Direccion: " + aux.direccion + "<br>" \
                + "<span class='info'><a class='info' href='/aparcamientos/" + aux.nombre + "'> Mas Info</a></span><br>")
    return content
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
def paginasUsers ():
    content = []
    totUsers = User.objects.all()
    for user in totUsers:
        try:
            titulo = Personal.objects.get(creador=user).titulo #cogemos titulo de nuestra bdd
            if titulo == "":
                content.append("<a href='/" + user.username + "'> Pagina de " + user.username + "</a>Nick: " + user.username)
            else:
                content.append("<a href='/" + user.username + "'>" + titulo + "</a>Nick: " + user.username)
        except Personal.DoesNotExist:
            content.append("<a href='/" + user.username + "'> Pagina de " + user.username + "</a>Nick: " + user.username)
    return (content)
#-------------------------------------------------------------------------------------------------

#--GESTION /USER-----------------------------------------------------------------------------------------------
@csrf_exempt
def gestionUsuario(request, nick): #Pagina a la que nos dirigimos tras hacer /user

    if request.method == 'POST': #entramos por "ADD", añadimos PARKING, formamos user.html
        addPOST(request)
        userObject = User.objects.get(username=nick) #estos usuarios siempre deberian existir no?????
        #Necesitamos objeto de tipo User, para luego obtener la pagina_personal_unica a partir de el. NO nos vale con string nick
        content, titulo, formulario = htmlUser(request,userObject) #formamos user.html
        #return redirect(seleccionPersonal,str(request.user))

    if request.method == 'GET': #entramos aqui tras haber clickeado en el enlace lateral
        userObject = User.objects.get(username=nick) #estos usuarios siempre deberian existir no?????

        content, titulo, formulario = htmlUser(request, userObject) #formamos user.html


    datos = paginasUsers() #paginas personales laterales
    #Renderizamos user.html

    log = logInOut(request)
    links = linksOther()

    plantilla = get_template('user.html')
    Context = ({'log': log,
                'links': links,
                'titulo': titulo,
                'content': content,
                'datos' : datos,
                'form': formulario})
    return HttpResponse(plantilla.render(Context))
#-------------------------------------------------------------------------------------------------

#--/USER.HTML-----------------------------------------------------------------------------------------------
def htmlUser(request, userObject): #genera un html para /user

    try: #Existe pagina_personal_unica
        paginaPersonalUnica = Personal.objects.get(creador=userObject)
        #Obtenemos la lista de Aparcamientos seleccionados
        aparcamientosTot = Seleccionar.objects.filter(FichaPersonal=paginaPersonalUnica) #Objeto "Personal"
        content = "" #porsiaca! referenciado antes de asignar error posible!!
        for aux in aparcamientosTot:
            aparcamiento = aux.Aparcamiento #dentro de objeto "Peronal", especificamos que queremos un objeto "Aparcamiento"
            #content.append(listado(aparcamiento,request, 1, userObject))

            seleccion = Seleccionar.objects.get(Aparcamiento=aparcamiento,Usuario=userObject)
            if request.user.is_authenticated():
                content = "<a class='info' href='" + aparcamiento.url + "'> " + aparcamiento.nombre + "</a><br>" \
                    + "Direccion: " + aparcamiento.direccion + "<br>" \
                    + "<a class='info' href='/aparcamientos/" + aparcamiento.nombre + "'> Mas Info</a><br>" \
                    + "<span class='info'><span class='date'> Fecha Seleccion: " + str(seleccion.Fecha) + "</span></span><br>"
            else:
                content = "<a class='info' href='" + aparcamiento.url + "'> " + aparcamiento.nombre + "</a><br>" \
                    + "Direccion: " + aparcamiento.direccion + "<br>" \
                    + "<a class='info' href='/aparcamientos/" + aparcamiento.nombre + "'> Mas Info</a><br>" \
                    + "<span class='info'><span class='date'> Fecha Seleccion: " + str(seleccion.Fecha) + "</span></span>"


        #Usuario que visita es el creador de la pagina personal?
        formulario = ""
        if request.user.username == str(userObject):
            formulario = form("tituloPersonal",request.user.username,"")

        if paginaPersonalUnica.titulo == "":
            titulo = "Pagina de " + str(userObject)
        else:
            titulo = paginaPersonalUnica.titulo

        return(content, titulo, formulario)

    except Personal.DoesNotExist: #No existe paginaPersonalUnica. La CREAMOS!
        paginaPersonalUnica = Personal(creador=userObject, titulo="")
        paginaPersonalUnica.save()
        content = "No hay PARKINGS"
        return (paginaPersonalUnica.titulo,"" , content)
#-------------------------------------------------------------------------------------------------

# #AÑADIR APARCAMIENTO-----------------------------------------------------------------------------------------
# def addPOST(request): #Añade aparcamiento pulsado el boton "add"
#     #Procesa el POST que haremos sobre /(usuario)
#     #Y SI PROBAMOS A HACER LO DE : VALUE = REQUEST.POST [NAME, O LO QUE SEA]
#     keyPost, valuePost = request.body.decode('utf-8').split("=")
#     print(valuePost)
#     #Antes de nada comprobaremos si existe la pagina, si no, la creamos
#     usuario = User.objects.get(username=str(request.user))
#     try:
#         PaginaPersonal.objects.get(usuario=usuario)
#     except PaginaPersonal.DoesNotExist:
#         nuevaPagina = PaginaPersonal(Titulo="", usuario=usuario)
#         nuevaPagina.save()
#     #Comprobamos si se esta haciendo un POST para añadir aparcamiento o para modificar el titulo de nuestra paginaPersonalUnica
#     if keyPost == 'Add':
#         paginaPersonalUnica = PaginaPersonal.objects.get(usuario=usuario)
#         parking = Aparcamientos.objects.get(id=int(valuePost))
#         añadir = True
#         listaParkings = Seleccionar.objects.filter(Usuario=usuario)
#         for i in listaParkings:
#             if i.Aparcamiento.nombre == parking.nombre:
#                 añadir = False
#                 break
#         if añadir == True:
#             adiccion = Seleccionar(Aparcamiento=parking, Usuario=usuario, FichaPersonal=paginaPersonalUnica)
#             adiccion.save()
#     elif keyPost == 'Titulo':
#         pagina = PaginaPersonal.objects.get(usuario=usuario)
#         pagina.Titulo = unquote_plus(valuePost)
#         pagina.save()


#PAGINA PERSONAL DE CADA APARCAMIENTO-------------------------------------------------------------
def infoAparcamiento(request):
    plantilla = get_template('aparcamientos.html')
    return HttpResponse(plantilla.render(Context))
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
@csrf_exempt
def aboutPS(request): #pagina de informacion/ayuda de PS
    links = linksOther()
    log = logInOut(request)
    content = texto("about") #contenido (texto) del about

    plantilla = get_template("about.html")
    Context = ({'content': content,
                'log': log,
                'links': links})
    return HttpResponse(plantilla.render(Context))
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
@csrf_exempt
def loginPS(request):
    nick = request.POST['name']
    password = request.POST['pass']
    user = authenticate(username=nick, password=password)

    if user is not None: #correcto, redireccionamos
        login(request, user)
        return redirect(home)

    else: #Nick o pass incorrectos
        log = logError(request) #formulario de error de sign in
        links = linksHome() #links todos, about
        boton = form("accesible","","")

        ########################################################
        ###FALTA METER
        #CONTENT --> reseteamos y metemos mas comentados.
        #PANEL LATERAL
        #ETC

        template = get_template("home.html")
        c = Context ({'log': log,
                      'links': links,
                      'boton': boton})
        return HttpResponse(template.render(c))
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
@csrf_exempt
def logoutPS(request): #Lo llamo logoutPS, porque si lo llamo logout se lia
    logout(request)
    return redirect(home)

#-------------------------------------------------------------------------------------------------
@csrf_exempt
def logError(request): #Nuevo form para login, dado el error de autentificacion
    log = "<form class='.t-left' action='/login' method='POST'>" \
        + "<label><strong>Wrong Nick or Pass. Try again</strong><br></label>" \
        + "NICK:  <input type='text' name='name'><br>" \
        + "PASS: <input type='password' name='pass'><br> "\
        + "<input type='submit' value='Submit'></form>"
    return log
