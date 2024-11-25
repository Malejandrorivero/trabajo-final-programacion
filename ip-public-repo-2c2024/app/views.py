from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
    return render(request, 'login.html')

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
