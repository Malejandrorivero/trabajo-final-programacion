from app.models import Favourite
import requests

import requests

import requests

def getAllImages(page=1, query=''):
    url = f"https://rickandmortyapi.com/api/character/?page={page}&name={query}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        total_pages = data['info']['pages']
        return results, total_pages
    else:
        return [], 0



def saveFavourite(image):
    try:
        fav = Favourite.objects.create(
            url=image.url,
            name=image.name,
            status=image.status,
            last_location=image.last_location,
            first_seen=image.first_seen,
            user=image.user,
            comment=image.comment  # Guardamos el comentario
        )
        return fav
    except Exception as e:
        print(f"Error al guardar el favorito: {e}")
        return None

def editComment(fav_id, comment):
    try:
        favourite = Favourite.objects.get(id=fav_id)
        favourite.comment = comment
        favourite.save()
        return True
    except Favourite.DoesNotExist:
        print(f"El favorito con ID {fav_id} no existe.")
        return False
    except Exception as e:
        print(f"Error al actualizar el comentario: {e}")
        return False

def deleteComment(fav_id):
    try:
        favourite = Favourite.objects.get(id=fav_id)
        favourite.comment = ""
        favourite.save()
        return True
    except Favourite.DoesNotExist:
        print(f"El favorito con ID {fav_id} no existe.")
        return False
    except Exception as e:
        print(f"Error al eliminar el comentario: {e}")
        return False

def getAllFavourites(user):
    favouriteList = Favourite.objects.filter(user=user).values('id', 'url', 'name', 'status', 'last_location', 'first_seen', 'comment')
    return list(favouriteList)

def deleteFavourite(id):
    try:
        favourite = Favourite.objects.get(id=id)
        favourite.delete()
        return True
    except Favourite.DoesNotExist:
        print(f"El favorito con ID {id} no existe.")
        return False
    except Exception as e:
        print(f"Error al eliminar el favorito: {e}")
        return False
