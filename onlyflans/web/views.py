from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from .models import Flan, Contact, Client
from .forms import ClientForm, ContactFormForm
from django.core.cache import cache

#Index=Home
def index(request):
    flanes_publicos = Flan.objects.filter(is_private=False)
    return render(request, 'index.html', {'lista_flanes': flanes_publicos}) # Flanes publicos-Index

#About=Acerca de OnlyFlans
def about(request):
    return render(request, 'about.html', {})

#Lista de Flanes
def flan_list(request):
    all_flan = Flan.objects.all() 
    context = {'Flan':all_flan}
    return render(request,'flan.html',context=context)

#Welcome=Vista Protegida
@login_required
def welcome(request):
    username = request.session.get('username', request.user.name if request.user.is_authenticated else None)
    
    private_flan = Flan.objects.filter(is_private=True)
    context = {
        'flan_list': private_flan,
        'username': username,
        'user': request.user  # Asegura que el objeto de usuario esté disponible en el contexto
    }
    return render(request, 'welcome.html', context)

#Autenticacion de Usuarios
@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        # Procesamiento para solicitudes AJAX (peticiones asíncronas)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'Credenciales inválidas.'}, status=400)
        
        else:
            # Procesamiento para solicitudes normales (no AJAX)
            form = AuthenticationForm(request, request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect('welcome')  # Redireccionar a la página deseada después del login
                    else:
                        return HttpResponse('Tu cuenta está desactivada.')
                else:
                    messages.error(request, 'Credenciales inválidas. Inténtalo de nuevo.')
            else:
                messages.error(request, 'Credenciales inválidas. Inténtalo de nuevo.')
            
            return redirect('index')  # Redireccionar a la página de inicio en caso de credenciales inválidas
    
    # Si el método de solicitud no es POST (por ejemplo, GET), renderizar el formulario de inicio de sesión
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    if request.method == 'POST':
        request.session.flush()
        logout(request)
        messages.success(request, '¡Has cerrado sesión exitosamente!')
        cache.clear()
        return redirect('logout_page')
    else:
        return render(request, 'registration/logout.html')
    
def logout_page(request):
        return render(request, 'registration/logout.html')

#Formulario de Registro de Clientes=Usuarios
def add_user_to_client_group(user):
    group, created = Group.objects.get_or_create(name='clientes_onlyflans')
    user.groups.add(group)

def registration(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if Client.objects.filter(email=email).exists():
                form.add_error('email', 'El correo electrónico ya está en uso.')
            else:
                client = form.save(commit=False)
                client.set_password(form.cleaned_data['password'])
                client.save()

                # Agregar al grupo 'clientes_onlyflans'
                add_user_to_client_group(client)

                # Autenticar y loguear al usuario recién registrado
                user = authenticate(request, email=email, password=form.cleaned_data['password'])
                if user is not None:
                    login(request, user)
                    return redirect('welcome')  # Redirigir a la página de bienvenida después del registro

    else:
        form = ClientForm()

    return render(request, 'registration_form.html', {'form': form})

def new_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            # Guardamos al cliente
            client = form.save(commit=False)
            client.set_password(password)
            client.save()

            # Autenticamos y logueamos al usuario recién registrado
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('welcome.html')  # Redirige a la página de bienvenida después del login

    else:
        form = ClientForm()

    login_form = AuthenticationForm()  # Formulario de login para la vista
    return render(request, 'new_client.html', {'form': form, 'login_form': login_form})

#Listado de  Clientes=costumers
def clients(request):
    customers_list = Client.objects.all()
    return render(request, 'registration/clients.html', {'customers_list': customers_list})

def save_customer(request):
    if request.method == 'POST':
        name = request.POST['name']
        lastname = request.POST['lastname']
        birth_date = request.POST['birth_date']
        email = request.POST['email']
        address = request.POST['address']
        
        customers = Client(name=name, lastname=lastname, birth_date=birth_date, email=email, address=address)
        customers.save()

    return redirect("registration/clients")

def edit_customer(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    
    if request.method == 'POST':
        client.name = request.POST['name']
        client.lastname = request.POST['lastname']
        client.birth_date = request.POST['birth_date']
        client.email = request.POST['email']
        client.address = request.POST['address']
        client.save()
        return redirect("clients")
    
    context = {
        'client': client,
    }
    return render(request, "registration/save_customer.html", context)

def delete_customer(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        client.delete()
        return redirect("clients")
    
    context = {
        'client': client,
    }
    return render(request, "registration/delete_customer.html", context)

#Contacto-envio de mensajes
def contact(request):
    if request.method == 'POST':
        form = ContactFormForm(request.POST)
        if form.is_valid():  
            form.save()
            messages.success(request, '¡Tu mensaje ha sido enviado exitosamente!')
            return redirect('success')
    else:
        form = ContactFormForm()
    return render(request, 'contact.html', {'form': form})

def success(request):
    return render(request, 'success.html')