from django.urls import path
from .views import (ImageUploadView, ImageToBlackAndWhite, BlurFilter,
                    ImageSketchFilter, EmbossFilter, SharpenFilter, SepiaFilter)

urlpatterns = [
    path('image-upload/', ImageUploadView.as_view(), name='image-upload'),
    path('blackandwhite/', ImageToBlackAndWhite.as_view(), name='image-filter-black-and-white'),
    path('blur/', BlurFilter.as_view(), name='image-filter-blur'),
    path('sketch/', ImageSketchFilter.as_view(), name='image-sketch-filter'),
    path('emboss/', EmbossFilter.as_view(), name='image-emboss'),
    path('sharpen/', SharpenFilter.as_view(), name='image-sharpen'),
    path('sepia/', SepiaFilter.as_view(), name='image-sepia')

]
