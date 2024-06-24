# capa de vista/presentación
# si se necesita algún dato (lista, valor, etc), esta capa SIEMPRE se comunica con services_nasa_image_gallery.py

from django.shortcuts import redirect, render
from .layers.services import services_nasa_image_gallery
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# función que invoca al template del índice de la aplicación.
def index_page(request):
    return render(request, 'index.html')

# auxiliar: retorna 2 listados -> uno de las imágenes de la API y otro de los favoritos del usuario.
def getAllImagesAndFavouriteList(request,input):
    images = services_nasa_image_gallery.getAllImages(input)
    favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request)

    return images, favourite_list

# función principal de la galería.
def home(request):
    # llama a la función auxiliar getAllImagesAndFavouriteList() y obtiene 2 listados: uno de las imágenes de la API y otro de favoritos por usuario*.
    # (*) este último, solo si se desarrolló el opcional de favoritos; caso contrario, será un listado vacío [].

    # Si estamos en la página home, borro la última palabra buscada de la sesión.
    request.session['last_word_searched'] = ""

    images,favourite_list = getAllImagesAndFavouriteList(request,None)
    
    return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list} )


# función utilizada en el buscador.
def search(request):
    search_msg = request.GET.get('query', request.POST.get('query', ''))
    request.session['last_word_searched'] = search_msg  # Guardar query en la sesión
    # si el usuario no ingresó texto alguno, debe refrescar la página; caso contrario, debe filtrar aquellas imágenes que posean el texto de búsqueda.
    if (search_msg == ''):
        images, favourite_list = getAllImagesAndFavouriteList(request,None)
        return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list} )
    # si el usuario no ingresó texto alguno, debe refrescar la página; caso contrario, debe filtrar aquellas imágenes que posean el texto de búsqueda.
    else:
        images, favourite_list = getAllImagesAndFavouriteList(request,search_msg)
       
        return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list} )

def stringExists(text,object) :
    if text in object.title.lower() :
        return True
    return False

# las siguientes funciones se utilizan para implementar la sección de favoritos: traer los favoritos de un usuario, guardarlos, eliminarlos y desloguearse de la app.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request)
    return render(request, 'favourites.html', {'favourite_list': favourite_list})


@login_required
def saveFavourite(request):
    # Llamo a la función de la capa de servicios para guardar la tarjeta en la base de datos de favoritos.

    services_nasa_image_gallery.saveFavourite(request)

    # Obtengo de la sesión la última palabra de búsqueda que se hizo para mantenerme en la misma página.

    query = request.session.get('last_word_searched', '')

    if query:
        # Redirige a la ruta '/buscar' con el valor de 'query'
        return redirect(f'/buscar?query={query}')
    else:
        return redirect("home")


@login_required
def deleteFavourite(request):
    services_nasa_image_gallery.deleteFavourite(request)
    return redirect(f'/favourites')


@login_required
def exit(request):
    pass
