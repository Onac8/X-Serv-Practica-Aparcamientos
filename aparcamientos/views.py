from django.shortcuts import render
from django.http import *
from django.views.decorators.csrf import csrf_exempt
from aparcamientos.models import *
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth import logout, authenticate, login
#from django.db import models
#from urllib.parse import unquote_plus


@csrf_exempt
def home(request):
    if request.method == "GET":
        log = logInOut(request)
        template = get_template("index.html")
        c = Context ({'log': log})
        return HttpResponse(template.render(c))

    #OTRA COSAAAAAAAAAAAAAAAAAAAAAAA
    #elif request.method == 'POST':

#Listas con enlaces dependiendo de la pagina a servir------------
def linksHome():
    links = []
    links.append("<a href='/aparcamientos'>TODOS</a>")
    links.append("<a href='/about'>ABOUT</a>")
    return links

def linksOther():
    links = []
    links.append ("<a href='/'> INICIO </a>")
    links.append("<a href='/aparcamientos'>TODOS</a>")
    links.append("<a href='/about'>ABOUT</a>")
    return links
#----------------------------------------------------------------


@csrf_exempt
def loginPS(request):
    nick = request.POST['name']
    password = request.POST['pass']
    user = authenticate(username=nick, password=password)

    if user is not None: #correcto, redireccionamos
        login(request, user)
        return redirect(home)

    else: #Nick o pass incorrectos
        log = logError(request) #formulario
        links = linksHome() #links todos, about
        template = get_template("index.html")
        c = Context ({'log': log})
        return HttpResponse(template.render(c))

@csrf_exempt
def logError(request): #Nuevo form para login, dado el error de autentificacion
    log = "<form class='.t-left' action='/login' method='POST'>" \
        + "<label><strong>Wrong Nick or Pass. Try again</strong><br></label>" \
        + "NICK:  <input type='text' name='name'><br>" \
        + "PASS: <input type='password' name='pass'><br> "\
        + "<input type='submit' value='Submit'></form>"
    return log


@csrf_exempt
def logInOut(request): #Form para login o enlace para logout.
    if request.user.is_authenticated():
        log = "<span id= 'logError' class= '.t-center'>Logged in as " + request.user.username + ". <a href='/logout'> Logout </a><br></span>"
    else:
        log = "<form class='.t-left' action='/login' method='POST'>" \
            + "<label>You aren't logged. Please login<br></label>" \
            + "NICK:  <input type='text' name='name'><br>" \
            + "PASS: <input type='password' name='pass'><br> "\
            + "<input type='submit' value='Submit'></form>"
    return log


@csrf_exempt
def logoutPS(request): #Lo llamo salir, porque si lo llamo logout se lia
    logout(request)
    return redirect(home)


# @csrf_exempt
# #Podemos entrar a esta view clickeando en uno de los enlaces anteriores o
# #poniendo directamente el recurso (/loquesea)
# def resource(request, nombreRecurso):
#     if request.method == "GET":
#         if request.user.is_authenticated():
#             htmlAnswer = "Logged in as " + request.user.username \
#                 + ". <a href='/logout'> Logout </a><br>"
#         else:
#             htmlAnswer = "You are not logged in. " \
#             + "<a href='/admin/'> Login </a><br> "
#         try:
#             pagina = Pages.objects.get(nombre=nombreRecurso)
#             htmlAnswer = htmlAnswer + pagina.pagina
#             return HttpResponse(htmlAnswer)
#         except Pages.DoesNotExist:
#             return HttpResponseNotFound(htmlAnswer + "Page Not Found")
#     elif request.method == 'PUT':
#         if request.user.is_authenticated:
#             try:
#                 pagina = Pages.objects.get(name=nombreRecurso)
#                 pagina.page = request.body.decode('utf-8')
#                 pagina.save()
#                 return(HttpResponse("Updated resource: /" + nombreRecurso))
#             except Pages.DoesNotExist:
#                 return HttpResponseNotFound("ERROR! Resource doesn't exist!")
#         else:
#             return HttpResponseBadRequest("ERROR! YOU ARE NOT LOGGED IN. YOU CAN'T PUT")
