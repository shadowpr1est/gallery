from django.shortcuts import render
from django.core.cache import cache
from django.http import Http404
from images.api.api import PexelsAPI


def index(request):
    search = request.GET.get('search')
    section = request.GET.get('section', 'all').lower()
    ai = request.GET.get('ai') == 'on'
    api = PexelsAPI()
    images = api.get_photo('Animal')

    if search:
        if ai:
            images = api.generated_photo(search)
        else:
            images = api.get_photo(search)

    elif section == 'ai_generated':
        images = api.get_cached_generated_images()

    return render(request, 'images/index.html', {
        'images': images,
        'search_value': search or '',
        'ai_checked': ai,
        'active_section': section,
    })

def img_detail(request, image_id):
    image = cache.get(f"image:{image_id}")
    if not image:
        raise Http404("Изображение не найдено")

    return render(request, 'images/image_detail.html', {'image': image})

