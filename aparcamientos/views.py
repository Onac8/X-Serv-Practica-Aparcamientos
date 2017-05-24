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
from urllib2 import urlopen
import xml.etree.ElementTree as ET


#Listas con enlaces dependiendo de la pagina a servir------------
@csrf_exempt
def linksHome():
    links = []
    links.append("<a href='/aparcamientos'>TODOS</a>")
    links.append("<a href='/about'>ABOUT</a>")
    return links

@csrf_exempt
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

    elif tipo == "getdata":
        out = "<form method='POST'><button type='submit' name='boton' value='OBTENER'>Obtener Datos</button></form>"

    elif tipo == "nodata":
        out = []
        out.append ("No hay aparcamientos. Pulse sobre el botón 'Obtener datos'")

    elif tipo == "comentados":
        out = "Aparcamientos mas comentados"

    elif tipo == "parkAccesibles":
        out = "Aparcamientos accesibles"

    elif tipo == "comentario":
        out = "<form method='POST'> Comentario <br><input type='text' id='Comentarios'  name='Comentario'  ><input type='submit' value='Comentar'></form>"

    elif tipo == "xml":
        out = "<a href='" + info + "/xml'>" + info + "</a>"

    elif tipo == "titulo":
        out = "<form name='myForm' action='/" + info + "' onsubmit='return validateForm()' method='post'>" \
            + "Name: <input type='text' name='Titulo'> <input type='submit' value='Submit'></form>"

    elif tipo == "css":
        out = "<form id='formularioCss' action='/" + info + "' method='POST'>" \
            + "Color <br><input type='color' name='Color' value='#ff0000'><br><br>" \
            + "Tipo de letra<br><input type='radio' name='Size' value='Normal' checked> Short<br>" \
            +  "<input type='radio' name='Size' value='Grande'> Medium<br>" \
            + "<input type='submit' value='Enviar'></form>"

    return out

#---------------------------------------------------------------------------------------


#LISTADOS Y PAGINAS-----------------------------------------------------------------------------------------------
@csrf_exempt
def listado(lista, request, nick): #listado con todos los aparcamientos seleccionados por el user
    content = []
    for aux in lista:
        if request.user.is_authenticated(): #parte privada (con boton add)
            content.append("<a class='info' href='" + aux.url + "'> " + aux.nombre + "</a><br>" \
                + "Direccion: " + aux.direccion + "<br>" \
                + "<a class='info' href='/aparcamientos/" + str(aux.id) + "'>Mas informacion...</a><br>"+ form("add", request.user.username, str(aux.id)) + "<br>")
        else: #parte publica (sin boton add)
            content.append("<a class='info' href='" + aux.url + "'> " + aux.nombre + "</a><br>" \
                + "Direccion: " + aux.direccion + "<br>" \
                + "<span class='info'><a class='info' href='/aparcamientos/" + str(aux.id) + "'> Mas Info</a></span><br>")
    return content
#-------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
@csrf_exempt
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
@csrf_exempt
def crearPagPersonales(): #crea las paginas personales asociadas a cada usuario registrado
    pagsPersonalesTot = Personal.objects.all()
    usersTot = User.objects.all()
    if len(pagsPersonalesTot) != len(usersTot):
        for user in usersTot:
            try:
                aux = Personal.objects.get(creador=user)
            except Personal.DoesNotExist:
                pagPersonal = Personal(creador=user)
                pagPersonal.save()

##HOME##############################################################################
####################################################################################
@csrf_exempt
def home(request): #pagina principal
    if request.method == "GET": #Ordenamos por aparcamientos mas comentados
        titulo = form("comentados","","") #aparcamientos mas comentados
        boton = form("accesible","","")
        parkings = Aparcamientos.objects.all() #con all no tenemos excepcion!

        if len(parkings) == 0:
            titulo = ""
            boton = form("getdata", "", "") #boton para bajarse los datos XML
            content = form("nodata","","")

        else:
            parkingsOrdenados = Aparcamientos.objects.filter(numComentarios__gt = 0)
            parkingsOrdenados = parkingsOrdenados.order_by('-numComentarios')[:5] #solo mostramos los 5 primeros
            content = listado(parkingsOrdenados, request, request.user) #listado de parkings

    elif request.method == 'POST': #aqui tratamos solo el post del boton accesibles
        valor = request.POST ['boton']

        if valor == "ACCESIBLES": #Aparcamientos accesibles
            titulo = form("parkAccesibles","","") #aparcamientos accesibles
            boton = form("accesible2","","") #pasamos a mostrar boton de "ir a mas comentados"
            parkings = Aparcamientos.objects.filter(accesibilidad=1)
            parkingsAccesibles = parkings.order_by('numComentarios')
            content = listado(parkingsAccesibles, request, request.user) #listado de parkings accesibles

        elif valor == "COMENTADOS": #Aparcamientos mas comentados
            titulo = form("comentados", "", "")
            boton = form("accesible","","") #pasamos a mostrar de nuevo boton de "ir a accesibles"
            parkings = Aparcamientos.objects.all()
            parkingsOrdenados = parkings.order_by('-numComentarios')[:5]
            content = listado(parkingsOrdenados,request, request.user) #listado de parkings

        elif valor == "OBTENER": #Post que nos llega al pulsar boton "Obtener Datos"
            parserXML()
            return redirect(home)


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

    if request.method == 'GET': #entramos aqui tras haber clickeado en el enlace lateral
        try: #por si ponemos /usuario_el_que_sea a mano en la barra de direcciones
            userObject = User.objects.get(username=nick)
            paginaPersonalUnica = Personal.objects.get(creador=userObject)

            #Formulario para cambiar titulo/css? --> Solo si usuario que request es el creador de la pagPersonal
            formulario = ""
            formularioCss = ""
            if request.user.username == str(userObject):
                formularioCss = form("css", request.user.username, "")
                formulario = form("titulo", nick, "")

            #Titulo de pagina personal
            if paginaPersonalUnica.titulo == "":
                titulo = "Pagina de " + str(userObject) # "Pagina de "nick""
            else:
                titulo = paginaPersonalUnica.titulo # "Nombre de la pagina personal chulo"



            aparcamientosTot = Seleccionar.objects.filter(fichaPersonal=paginaPersonalUnica) #Objeto "Personal"
            content = [] #porsiaca! referenciado antes de asignar error posible!!
            for aux in aparcamientosTot:
                aparcamiento = aux.aparcamiento #dentro de objeto "Personal", especificamos que queremos un objeto "Aparcamiento"

                seleccion = Seleccionar.objects.get(aparcamiento=aparcamiento,usuario=userObject)
                if request.user.is_authenticated():
                    content.append ("<a class='info' href='" + aparcamiento.url + "'> " + aparcamiento.nombre + "</a><br>" \
                        + "Direccion: " + aparcamiento.direccion + "<br>" \
                        + "<a class='info' href='/aparcamientos/" + str(aparcamiento.id) + "'> Mas Info</a><br>" \
                        + "<span class='info'><span class='date'> Fecha Seleccion: " + str(seleccion.fecha) + "</span></span><br><br>")
                else:
                    content.append("<a class='info' href='" + aparcamiento.url + "'> " + aparcamiento.nombre + "</a><br>" \
                        + "Direccion: " + aparcamiento.direccion + "<br>" \
                        + "<a class='info' href='/aparcamientos/" + str(aparcamiento.id) + "'> Mas Info</a><br>" \
                        + "<span class='info'><span class='date'> Fecha Seleccion: " + str(seleccion.fecha) + "</span></span><br><br>")

        except User.DoesNotExist: #Error tratado
            content = []
            content.append ("No existe el usuario " + str(nick) + ". Intento de ruptura.")
            template = get_template('user.html')
            Context = ({'log': logInOut(request),
                        'links': linksOther(),
                        'content': content})
            return HttpResponseNotFound(template.render(Context))

    #-------------------------------------------------------------------------------------------------------
    elif request.method == 'POST': #entramos por "ADD" o por "CAMBIAR TITULO", añadimos PARKING, formamos user.html

        if 'Add' in request.POST:
            paginaPersonalUnica = Personal.objects.get(creador=request.user)
            parking = Aparcamientos.objects.get(id=int(request.POST['Add']))
            add = True
            listaParkings = Seleccionar.objects.filter(usuario=request.user)
            for i in listaParkings:
                if i.aparcamiento.nombre == parking.nombre:
                    add = False
                    break
            if add == True:
                addParking = Seleccionar(aparcamiento=parking, usuario=request.user, fichaPersonal=paginaPersonalUnica)
                addParking.save()

        elif 'Titulo' in request.POST: #cambiamos titulo de la pagina personal
            pagina = Personal.objects.get(creador=request.user)
            pagina.titulo = request.POST['Titulo']
            pagina.save()

        elif 'Color' in request.POST: #CSS dinamico
            color = request.POST['Color']
            letra = request.POST['Size']

            usuario = User.objects.get(username=request.user)
            css = Personal.objects.get(creador=usuario)
            css.color = color
            css.letra = letra
            css.save()


        return redirect (gestionUsuario, str(request.user))


    #-------------------------------------------------------------------------------------------------------
    #Renderizamos user.html
    template = get_template('user.html')
    Context = ({'log': logInOut(request),
                'links': linksOther(),
                'titulo': titulo,
                'content': content,
                'datos' : paginasUsers(), #paginas personales laterales,
                'xml' : form("xml", nick, ""),
                'formcss' : formularioCss,
                'form': formulario}) #para javascript
    return HttpResponse(template.render(Context))




#PAGINA PERSONAL DE CADA APARCAMIENTO-------------------------------------------------------------
@csrf_exempt
def infoAparcamiento(request, id):

    if request.method == "GET":
        try:
            aparcamiento = Aparcamientos.objects.get(id=id)
        except Aparcamientos.DoesNotExist:
            template = get_template("infoAparcamiento.html")
            content = "No existe dicho aparcamiento. Intento de ruptura."
            Context = ({'login': logInOut(request),
                        'enlaces': linksOther(),
                        'content': content})
            return HttpResponseNotFound(template.render(Content))

    elif request.method == "POST": #añadimos comentario y sumamos contador
        comentario = request.POST['Comentario']

        aparcamiento = Aparcamientos.objects.get(id=id)
        aparcamiento.numComentarios = aparcamiento.numComentarios + 1
        aparcamiento.save()

        nuevo = Comentario(aparcamiento=aparcamiento, texto=comentario)
        nuevo.save()


    #CAJA para comentar SI o NO------------
    if request.user.is_authenticated():
        formulario = form("comentario", "", "")
    else:
        formulario = ""
    #--------------------------------------

    #Preparamos los valores del context para renderizar-----------------------
    aparcamiento = Aparcamientos.objects.get(id=id)

    content=[]
    try:
        comentariosTot = Comentario.objects.filter(aparcamiento=aparcamiento)
        for aux in comentariosTot:
            content.append(aux.texto)
    except Comentario.DoesNotExist:
        content.append  ("No hay comentarios.")

    #Renderizamos aparcamientosInfo.html
    template = get_template('infoAparcamiento.html')
    Context = ({'log': logInOut(request),
                'links': linksOther(),
                'content': content,
                'datos' : paginasUsers(), #paginas personales laterales,
                'form': formulario,
                'aparcamiento': aparcamiento})
    return HttpResponse(template.render(Context))


#PARSER_XML---------------------------------------------------------------------------------
@csrf_exempt
def parserXML():
    xmlFile = urlopen("http://datos.munimadrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=202584-0-aparcamientos-residentes&mgmtid=e84276ac109d3410VgnVCM2000000c205a0aRCRD&preview=full")
    arbol = ET.parse(xmlFile)
    raiz = arbol.getroot()

    for elem in arbol.iter(): #recorremos el arbol --> hago pass a los elementos que no me interesan, aunque esta bien tratarlos
        if "ID-ENTIDAD" in elem.attrib.values():
            pass
        elif "NOMBRE" in elem.attrib.values():
            nuevoAparcamiento = Aparcamientos(nombre=elem.text)
            nuevoAparcamiento.numComentarios = 0
        elif "DESCRIPCION" in elem.attrib.values():
            nuevoAparcamiento.descripcion = elem.text
        elif "ACCESIBILIDAD" in elem.attrib.values():
            nuevoAparcamiento.accesibilidad = elem.text
        elif "CONTENT-URL" in elem.attrib.values():
            nuevoAparcamiento.url = elem.text
        elif "NOMBRE-VIA" in elem.attrib.values(): #nombre de la calle
            nombreCalle = elem.text
            nombreCalle = "C/" + nombreCalle
            nuevoAparcamiento.direccion = elem.text
        elif "CLASE-VIAL" in elem.attrib.values(): #calle, avenida, paseo
            tipoCalle = elem.text #lo ignoramos un poco
        elif "TIPO-NUM" in elem.attrib.values():
            pass
        elif "NUM" in elem.attrib.values():
            pass
        elif "ORIENTACION" in elem.attrib.values():
            pass
        elif "LOCALIDAD" in elem.attrib.values():
            pass
        elif "PROVINCIA" in elem.attrib.values():
            pass
        elif "CODIGO-POSTAL" in elem.attrib.values():
            pass
        elif "BARRIO" in elem.attrib.values():
            nuevoAparcamiento.barrio = elem.text
        elif "DISTRITO" in elem.attrib.values():
            nuevoAparcamiento.distrito = elem.text
        elif "COORDENADA-X" in elem.attrib.values():
            pass
        elif "COORDENADA-Y" in elem.attrib.values():
            pass
        elif "LATITUD" in elem.attrib.values():
            nuevoAparcamiento.latitud = elem.text
        elif "LONGITUD" in elem.attrib.values():
            nuevoAparcamiento.longitud = elem.text
        elif "TELEFONO" in elem.attrib.values():
            nuevoAparcamiento.telefono = elem.text
        elif "EMAIL" in elem.attrib.values():
            nuevoAparcamiento.email = elem.text
        elif "TIPO" in elem.attrib.values():
            nuevoAparcamiento.save()
        else:
            pass



#CSS DINAMICO------------------------------------------------------------------------------------------
def userCss(request):
    if request.user.is_authenticated(): #necesitamos saber si esta logueado, si lo esta tiene pagPersonal
        usuario = User.objects.get(username=request.user)
        tipo = Personal.objects.get(creador=usuario) #para cambiar color y letra

        #if tipo.color == "" or tipo.letra == "":
        color = "#192666"
        tamano = "5mm"
    else:
        color = "#192666"
        tamano = "5mm"

    plantillaCSS = get_template('personal.css')
    Context = ({'color': Color,
                'tamaño': tamano})
    return HttpResponse(plantillaCSS.render(Context),content_type="text/css")



#XML USER----------------------------------------------------------------------------------------------
def userXml(request, nick): #enviamos datos a nuestro fichero xml (por comodidad) -- ahorro de espacio aqui
    template = get_template('userdd.xml')
    usuario = User.objects.get(username=nick)
    parkingsTot = Seleccionar.objects.filter(usuario=usuario)

    context = ({'nick': nick,
                'parks': parkingsTot})
    return HttpResponse(template.render(context), content_type="text/xml")



#HTML5 (AUDIOS)----------------------------------------------------------------------------------------
def multimediaPS(request):
    plantilla = get_template("multimedia.html")
    Context = ({'log': logInOut(request),
                'links': linksOther()})
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
        content=[]
        content.append( "Usuario o contraseña incorrectos. <a href ='/'> Prueba de nuevo </a>")

        template = get_template("home.html") #cambia el content de home.html
        c = Context ({'content': content,
                      'links': linksOther()}) #links Inicio, todos, about
        return HttpResponse(template.render(c))



#LOG OUT------------------------------------------------------------------------------------------------
@csrf_exempt
def logoutPS(request): #Lo llamo logoutPS, porque si lo llamo logout se lia
    logout(request)
    return redirect(home)
