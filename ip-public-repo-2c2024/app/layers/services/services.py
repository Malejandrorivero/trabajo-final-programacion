from ..persistence import repositories
from ..utilities import translator
from ..transport import transport
from django.contrib.auth import get_user

def getAllImages(page=1, query=''):
    json_collection, total_pages = repositories.getAllImages(page, query)
    images = [translator.fromRequestIntoCard(obj) for obj in json_collection]
    return images, total_pages


def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)
        favourite_list = repositories.getAllFavourites(user)
        return [translator.fromRepositoryIntoCard(fav) for fav in favourite_list]

def saveFavourite(request):
    fav = translator.fromTemplateIntoCard(request)
    fav.user = get_user(request)
    fav.comment = request.POST.get('comment', '')  # Capturamos el comentario desde el formulario
    return repositories.saveFavourite(fav)

def editComment(fav_id, comment):
    return repositories.editComment(fav_id, comment)

def deleteComment(fav_id):
    return repositories.deleteComment(fav_id)


def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.deleteFavourite(favId)