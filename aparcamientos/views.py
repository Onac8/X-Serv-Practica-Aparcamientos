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
def form(tipo, info, info2): #formularios, botones, texto y desplegable
    if tipo == "add":
        out = "<form action='/" + info + "' method='POST'>" \
            + "<button type='submit' name='Add' value='" + info2 + "'> Add </button></form>"

    elif tipo == "accesible": #con value = Comentados, indicando que muestre los accesibles
        out = "<form method='POST'><button type='submit' name='boton' value='ACCESIBLES'>Parkings Accesibles</button></form>"

    elif tipo == "accesible2": #con value = Comentados, indicando que vuelva a mostrar todo
        out = "<form method='POST'><button type='submit' name='boton' value='COMENTADOS'>Todos</button><form>"

    elif tipo == "tituloPersonal":
        out = "<form id='formularioTitulo' action='/" + info + "' method='POST'>" \
            + "Nombre de pagina personal<br><input type='text' name='Titulo'>" \
            + "<input type='submit' value='Enviar'></form>"

    elif tipo == "getdata":
        out = "<form method='POST'><button type='submit' name='boton' value='OBTENER'>Obtener Datos</button></form>"

    elif tipo == "nodata":
        out = "No hay aparcamientos. Pulse sobre el botón 'Obtener datos'"

    elif (tipo == "comentados"):
        out = "Aparcamientos mas comentados"

    elif (tipo == "accesible"):
        out = "Aparcamientos accesibles"

    elif (tipo == "no_parks"):
        out = "No hay Aparcamientos en la base de datos. CaRGALOS"

    return out

#---------------------------------------------------------------------------------------


#LISTADOS Y PAGINAS-----------------------------------------------------------------------------------------------
def listado(lista, request, nick): #listado con todos los aparcamientos seleccionados por el user
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


#CREAR PERSONALES------------------------------------------------------------------------------------
def crearPagPersonales(): #crea las paginas personales asociadas a cada usuario registrado
    pagsPersonalesTot = Personal.objects.all()
    usersTot = User.objects.all()
    if len(pagsPersonalesTot) != len(usersTot):
        for user in usersTot:
            try:
                user = Personal.objects.get(usuario=user)
            except Personal.DoesNotExist:
                pagPersonal = Personal(usuario=user)
                pagPersonal.save()

##HOME##############################################################################
####################################################################################
@csrf_exempt
def home(request): #pagina principal
    if request.method == "GET": #Ordenamos por aparcamientos mas comentados
        titulo = form("comentados","","")
        boton = form("accesible","","")
        parkings = Aparcamientos.objects.all() #con all no tenemos excepcion!

        if len(parkings) == 0:
          titulo = ""
          boton = form("getdata", "", "") #boton para bajarse los datos XML
          content = form("nodata")

        else:
          titulo = form("comentados", "", "")
          boton = form("accesible","","")
          parkingsOrdenados = parkings.order_by('-numComentarios')[:5] #solo mostramos los 5 primeros
          content = listado(parkingsOrdenados, request, request.user) #listado de parkings

    elif request.method == 'POST': #aqui tratamos solo el post del boton accesibles
        valor = request.POST ['boton']

        if valor == "ACCESIBLES": #Aparcamientos accesibles
            titulo = form("accesible")
            boton = form("accesible2","","") #pasamos a mostrar boton de "ir a mas comentados"
            parkings = Aparcamientos.objects.filter(accesibilidad=1)
            parkingsAccesibles = parkings.order_by('numComentarios')
            content = listado(parkingsAccesibles, request, request.user) #listado de parkings accesibles

        elif valor == "COMENTADOS": #Aparcamientos mas comentados
            titulo = form("comentados")
            boton = form("accesible","","") #pasamos a mostrar de nuevo boton de "ir a accesibles"
            parkings = Aparcamientos.objects.all()
            parkingsOrdenados = parkings.order_by('-numComentarios')[:5]
            content = listado(parkingsOrdenados,request, request.user) #listado de parkings

        elif valor == "OBTENER": #Post que nos llega al pulsar boton "Obtener Datos"
            parserXML()


    #creamos pagsPersonales cada vez que entremos al home por si hemos añadido
    #User desde el /admin, evitando asi tener que controlar alguna excepcion
    crearPagPersonales()

    #Renderizamos
    template = get_template("home.html")
    c = Context ({'log': logInOut(request),
                  'links': linksHome(), #links todos, about
                  'boton': boton,
                  'titulo': titulo,
                  'content': content,
                  'datos': paginasUsers()}) #Paginas Personales
    return HttpResponse(template.render(c))



#TODOS LOS APARCAMIENTOS----------------------------------------------------------------
@csrf_exempt
def aparcamientosPS(request): #lista de parkings totales (no se especifica que sea de 5 en 5)
    try: #¿Hay parkings en la lista?
        if request.method == "GET":
            parks = Aparcamientos.objects.all()

            content=[]
            for aux in parks:
                if request.user.is_authenticated(): #aparcamiento + boton add --> parte privada
                    content.append ("<a href='aparcamientos/" + str(aux.id) + "'>" + aux.nombre + "</a>" + form("add", request.user.username, str(aux.id)))
                else:
                    content.append ("<a href='aparcamientos/" + str(aux.id) + "'>" + aux.nombre + "</a>")

        elif request.method == 'POST': #Buscador por distrito
            distrito = request.POST['Distrito']
            #print(Distrito)
            parks = Aparcamientos.objects.filter(distrito=distrito)

            content=[]
            for aux in parks:
                if request.user.is_authenticated(): #aparcamiento + boton add --> parte privada
                    content.append ("<a href='aparcamientos/" + str(aux.id) + "'>" + aux.nombre + "</a>" + form("add", request.user.username, str(aux.id)))
                else:
                    content.append ("<a href='aparcamientos/" + str(aux.id) + "'>" + aux.nombre + "</a>")

        #renderizamos
        template = get_template("aparcamientos.html")
        Context = ({'log': logInOut(request),
                      'links': linksOther(),
                      'datos' : paginasUsers(),
                      'content': content})
        return HttpResponse(template.render(Context))


    except Aparcamientos.DoesNotExist: #no hay parkings en la lista
        template = get_template('aparcamiento.html')
        Context = ({'log': logInOut(request),
                    'links': linksOther(),
                    'boton' : form("getdata", "", ""), #boton para bajarse los datos XML
                    'content' : form("nodata","","")}) #nos indica que hay que bajarse los datos
        return HttpResponse(plantilla.render(Context))



#GESTION /USER-----------------------------------------------------------------------------------------------
@csrf_exempt
def gestionUsuario(request, nick): #Pagina a la que nos dirigimos tras hacer /user

    if request.method == 'POST': #entramos por "ADD" o por "CAMBIAR TITULO", añadimos PARKING, formamos user.html
        addPOST(request)
        userObject = User.objects.get(username=nick) #estos usuarios siempre deberian existir no????? objeto de tipo "User"
        content, titulo, formulario = htmlUser(request,userObject) #formamos user.html
        #return redirect(seleccionPersonal,str(request.user))


    if request.method == 'GET': #entramos aqui tras haber clickeado en el enlace lateral
        try: #por si ponemos /usuario_el_que_sea a mano en la barra de direcciones
            userObject = User.objects.get(username=nick)
            content, titulo, formulario = htmlUser(request, userObject) #formamos user.html

        except User.DoesNotExist: #Error tratado
            content = "NO EXISTE EL USUARIO " + str(nick)
            template = get_template('user.html')
            Context = ({'log': logInOut(request),
                        'enlaces': linksOther(),
                        'content': content})
            return HttpResponseNotFound(plantilla.render(Context))


    #Renderizamos user.html
    template = get_template('user.html')
    Context = ({'log': logInOut(request),
                'links': linksOther(),
                'titulo': titulo,
                'content': content,
                'datos' : paginasUsers(), #paginas personales laterales,
                'form': formulario})
    return HttpResponse(template.render(Context))



#--/USER.HTML-----------------------------------------------------------------------------------------------
def htmlUser(request, userObject): #genera un html para /user

    paginaPersonalUnica = Personal.objects.get(creador=userObject)
    aparcamientosTot = Seleccionar.objects.filter(FichaPersonal=paginaPersonalUnica) #Objeto "Personal"
    content = "" #porsiaca! referenciado antes de asignar error posible!!
    for aux in aparcamientosTot:
        aparcamiento = aux.Aparcamiento #dentro de objeto "Personal", especificamos que queremos un objeto "Aparcamiento"
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



#ABOUT-------------------------------------------------------------------------------------------------
@csrf_exempt
def aboutPS(request): #pagina de informacion/ayuda de PS
    links = linksOther()
    log = logInOut(request)

    plantilla = get_template("about.html")
    Context = ({'log': log,
                'links': links})
    return HttpResponse(plantilla.render(Context))



#LOG IN-------------------------------------------------------------------------------------------------
@csrf_exempt
def loginPS(request):
    nick = request.POST['name']
    password = request.POST['pass']
    user = authenticate(username=nick, password=password)

    if user is not None: #correcto, redireccionamos
        login(request, user)
        return redirect(home)

    else: #Nick o pass incorrectos
        content = "Usuario o contraseña incorrectos. <a href ='/'> Prueba de nuevo </a>"

        template = get_template("home.html") #cambia el content de home.html
        c = Context ({'content': content,
                      'links': linksOther()}) #links Inicio, todos, about
        return HttpResponse(template.render(c))



#LOG OUT------------------------------------------------------------------------------------------------
@csrf_exempt
def logoutPS(request): #Lo llamo logoutPS, porque si lo llamo logout se lia
    logout(request)
    return redirect(home)
