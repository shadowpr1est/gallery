from django.http import HttpResponse
from django.shortcuts import render

from images.api.api import PexelsAPI


def index(request):
    search = request.GET.get('search','Animal')
    if not search:
        search = 'Animal'

    images = PexelsAPI().get_photo(search)
    return render(
        request,
        'images/index.html',
        context={
            'images': images
        }
    )

# def image_detail(request):
#     id = request.GET.get('id',)
#     return render(
#         request,
#         '',
#         context={
#
#         }
#     )
