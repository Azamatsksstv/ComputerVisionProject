from rest_framework import serializers

from filters.models import EnteredImage, FilteredImage


class EnteredImageSerializer(serializers.ModelSerializer):
    # image = serializers.ImageField()

    class Meta:
        model = EnteredImage
        fields = '__all__'


class FilteredImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = FilteredImage
        fields = '__all__'
