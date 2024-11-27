from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .forms import UserRegisterForm
from django.shortcuts import render
from django.utils.encoding import smart_str



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Enviar correo electrónico con codificación UTF-8
            subject = smart_str('Registro exitoso', encoding='utf-8')
            message = smart_str(f'Tus credenciales de acceso son:\n\nUsuario: {user.username}\nClave: {form.cleaned_data["password"]}', encoding='utf-8')
            
            send_mail(
                subject,
                message,
                'tu_correo@gmail.com',
                [user.email],
                fail_silently=False,
            )
            
            messages.success(request, 'Tu cuenta ha sido creada exitosamente. Revisa tu correo electrónico para más detalles.')
            return render(request, 'registration/register.html', {'form': form, 'show_message': True})
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})



def index_page(request):
    return render(request, 'index.html')

def home(request):
    page = request.GET.get('page', 1)
    query = request.GET.get('query', '')

    images, total_pages = services.getAllImages(page, query)
    pages = range(1, total_pages + 1)
    favourite_list = []

    if request.user.is_authenticated:
        favourite_list = services.getAllFavourites(request)

    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list, 'total_pages': total_pages, 'current_page': int(page), 'query': query, 'pages': pages })

def search(request):
    query = request.POST.get('query', '')
    return redirect(f'/home?query={query}&page=1')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos. Inténtalo de nuevo.')
            return redirect('login')
    return render(request, 'registration/login.html')

@login_required
def getAllFavouritesByUser(request):
    favourite_list = services.getAllFavourites(request)
    return render(request, 'favourites.html', { 'favourite_list': favourite_list })

@login_required
def saveFavourite(request):
    services.saveFavourite(request)
    return redirect('home')

@login_required
def deleteFavourite(request):
    services.deleteFavourite(request)
    return redirect('favoritos')

@login_required
def editComment(request):
    fav_id = request.POST.get('id')
    comment = request.POST.get('comment')
    services.editComment(fav_id, comment)
    return redirect('favoritos')

@login_required
def deleteComment(request):
    fav_id = request.POST.get('id')
    services.deleteComment(fav_id)
    return redirect('favoritos')

@login_required
def exit(request):
    logout(request)
    return redirect('index-page')
