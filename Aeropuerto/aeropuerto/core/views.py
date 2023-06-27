from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Usuario, Pasajero
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count
import json
from django.http import JsonResponse
from django import forms

class PasajeroForm(forms.ModelForm):
    chofer_id = forms.CharField(widget=forms.HiddenInput())  # Agrega el campo chofer_id al formulario

    class Meta:
        model = Pasajero
        fields = ['nombre', 'direccion', 'telefono', 'chofer_id']  # Incluye el campo chofer_id en los campos del formulario

def index_view(request):
    return render(request, 'core/index.html')

def reserve_view(request):
    usuarios = Usuario.objects.all()  # Obtener todos los usuarios de la base de datos
    context = {
        'usuarios': usuarios
    }
    return render(request, 'core/reserve.html', context)

def home2_view(request):
    return render(request, 'core/home2.html')

def home_view(request):
    return render(request, 'core/home.html')

def succesfully_view(request):
    return render(request, 'core/succesfully.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'core/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        patente = request.POST['patente']
        nombre_chofer = request.POST['nombre_chofer']
        telefono_chofer = request.POST['telefono_chofer']

        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)
        # Crear instancia de Usuario y asociarla al usuario
        usuario = Usuario(user=user, email=email,  patente=patente, nombre_chofer=nombre_chofer, telefono_chofer=telefono_chofer)
        usuario.save()

        messages.success(request, 'Usuario registrado correctamente.')
        return redirect('succesfully')

    return render(request, 'core/register.html')

def form_pasajeros(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        telefono = request.POST['telefono']
        destino = request.POST['destino']
        chofer_id = request.POST.get('chofer_id')

        # Verificar que el ID del chofer esté presente en la solicitud o en la sesión
        if chofer_id:
            # Obtener el chofer correspondiente
            chofer = Usuario.objects.get(id=chofer_id)

            # Guardar los datos del pasajero en la base de datos y asociarlos al chofer
            pasajero = Pasajero(nombre=nombre, telefono=telefono, destino=destino, chofer=chofer)
            pasajero.save()

            return redirect('pasajeros_view')
        else:
            # Manejar el caso en el que no se haya proporcionado un ID de chofer
            messages.error(request, "ID de chofer no proporcionado")
            return redirect('form_pasajeros')

    return render(request, 'core/form_pasajeros.html')

def pasajeros_view(request):
    chofer_id = request.session.get('chofer_id')  # Obtener el ID del chofer desde la sesión

    pasajeros = Pasajero.objects.filter(chofer_id=chofer_id)

    return render(request, 'core/pasajeros.html', {'pasajeros': pasajeros})


def pasajero_view(request):
    if request.method == 'POST':
        form = PasajeroForm(request.POST)
        if form.is_valid():
            # Guardar los datos del pasajero y asociarlo al chofer correspondiente
            chofer_id = form.cleaned_data['chofer_id']
            chofer = Usuario.objects.get(id=chofer_id)
            pasajero = form.save(commit=False)
            pasajero.chofer = chofer
            pasajero.save()
            return redirect('pasajeros_view')
    else:
        form = PasajeroForm(initial={'chofer_id': request.session.get('chofer_id')})  # Pasar el ID del chofer inicialmente al formulario

    return render(request, 'core/form_pasajero.html', {'form': form})
    

def change_language_view(request):
  # Obtener el idioma seleccionado desde la solicitud
  language = request.POST.get('language')

  # Guardar el idioma seleccionado en la sesión o en una cookie, según tus necesidades
  # Por ejemplo, puedes guardar el idioma en la sesión:
  request.session['language'] = language

  # Retornar una respuesta JSON indicando que el cambio de idioma fue exitoso
  return JsonResponse({'success': True})







