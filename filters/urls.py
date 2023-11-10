from django.urls import path
from .views import ImageToBlackAndWhite, ImageBlurFilter, ImageSketchFilter

urlpatterns = [
    path('blackandwhite/', ImageToBlackAndWhite.as_view(), name='image-filter-black-and-white'),
    path('blur/', ImageBlurFilter.as_view(), name='image-filter-blur'),
    path('sketch/', ImageSketchFilter.as_view(), name='image-sketch-filter'),
]
