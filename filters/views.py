from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

from .models import EnteredImage, FilteredImage
from .serializers import EnteredImageSerializer, FilteredImageSerializer
from PIL import Image, ImageOps, ImageFilter


class ImageUploadView(APIView):
    def post(self, request):
        entered_image_serializer = EnteredImageSerializer(data=request.data)
        if entered_image_serializer.is_valid():
            entered_image_serializer.save()
            return Response({'Successfully uploaded'}, status=status.HTTP_201_CREATED)
        return Response(entered_image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageToBlackAndWhite(APIView):
    def post(self, request, *args, **kwargs):
        # Получаем изображение из запроса
        image_file = request.FILES.get('image_file')

        if not image_file:
            return Response({'error': 'No image file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Открываем изображение
            original_image = Image.open(image_file)

            # Преобразуем в черно-белое
            black_and_white_image = ImageOps.grayscale(original_image)

            # Сохраняем черно-белое изображение в памяти
            output_buffer = BytesIO()
            black_and_white_image.save(output_buffer, format='JPEG')
            output_buffer.seek(0)

            # Создаем объект InMemoryUploadedFile для черно-белого изображения
            black_and_white_file = InMemoryUploadedFile(
                output_buffer,
                'image',
                f'{image_file.name.split(".")[0]}_bw.jpg',
                'image/jpeg',
                output_buffer.tell(),
                None
            )

            # Сохраняем оригинальное изображение в базу данных
            entered_image = EnteredImage.objects.create(image_file=image_file)

            # Сохраняем черно-белое изображение в базу данных
            filtered_image = FilteredImage.objects.create(original_image=entered_image,
                                                          image_file=black_and_white_file,
                                                          filter_used='black_and_white')

            # Возвращаем сериализованные данные о сохраненных изображениях
            entered_image_serializer = EnteredImageSerializer(entered_image)
            filtered_image_serializer = FilteredImageSerializer(filtered_image)
            return Response({
                'entered_image': entered_image_serializer.data,
                'filtered_image': filtered_image_serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ImageBlurFilter(APIView):
    def post(self, request, *args, **kwargs):
        # Получаем изображение из запроса
        image_file = request.FILES.get('image_file')

        if not image_file:
            return Response({'error': 'Image file is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Открываем изображение
            original_image = Image.open(image_file)

            # Применяем эффект размытия
            blur_radius = 5
            blurred_image = original_image.filter(ImageFilter.GaussianBlur(blur_radius))

            # Сохраняем размытое изображение в памяти
            output_buffer = BytesIO()
            blurred_image.save(output_buffer, format='JPEG')
            output_buffer.seek(0)

            # Создаем объект InMemoryUploadedFile для размытого изображения
            filtered_image = InMemoryUploadedFile(
                output_buffer,
                'image',
                f'{image_file.name.split(".")[0]}_blurred.jpg',
                'image/jpeg',
                output_buffer.tell(),
                None
            )

            # Сохраняем оригинальное изображение в базу данных
            entered_image = EnteredImage.objects.create(image_file=image_file)

            # Сохраняем размытое изображение в базу данных
            filtered_image_obj = FilteredImage.objects.create(
                image_file=filtered_image,
                original_image=entered_image,
                filter_used='blurred_image'
            )

            # Возвращаем сериализованные данные о сохраненных изображениях
            entered_image_serializer = EnteredImageSerializer(entered_image)
            filtered_image_serializer = FilteredImageSerializer(filtered_image_obj)
            return Response({
                'entered_image': entered_image_serializer.data,
                'filtered_image': filtered_image_serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ImageSketchFilter(APIView):
    def post(self, request, *args, **kwargs):
        # Получаем изображение из запроса
        image_file = request.FILES.get('image_file')

        if not image_file:
            return Response({'error': 'Image file is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Открываем изображение
            original_image = Image.open(image_file)

            # Применяем эффект "Sketch"
            sketch_image = original_image.filter(ImageFilter.CONTOUR)

            # Сохраняем изображение в памяти
            output_buffer = BytesIO()
            sketch_image.save(output_buffer, format='JPEG')
            output_buffer.seek(0)

            # Создаем объект InMemoryUploadedFile для результирующего изображения
            filtered_image = InMemoryUploadedFile(
                output_buffer,
                'image',
                f'{image_file.name.split(".")[0]}_sketch.jpg',
                'image/jpeg',
                output_buffer.tell(),
                None
            )

            # Сохраняем оригинальное изображение в базу данных
            entered_image = EnteredImage.objects.create(image_file=image_file)

            # Сохраняем результат "Sketch" в базу данных
            filtered_image_obj = FilteredImage.objects.create(
                image_file=filtered_image,
                original_image=entered_image,
                filter_used='sketch_filter'
            )

            # Возвращаем сериализованные данные о сохраненных изображениях
            entered_image_serializer = EnteredImageSerializer(entered_image)
            filtered_image_serializer = FilteredImageSerializer(filtered_image_obj)
            return Response({
                'entered_image': entered_image_serializer.data,
                'filtered_image': filtered_image_serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)