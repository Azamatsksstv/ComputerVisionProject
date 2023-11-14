import cv2
import numpy as np
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

from .models import EnteredImage, FilteredImage
from .serializers import EnteredImageSerializer, FilteredImageSerializer
from PIL import Image, ImageOps, ImageFilter


class ImageUploadView(APIView):
    def get(self, request):
        entered_images = EnteredImage.objects.all()
        serializer = EnteredImageSerializer(entered_images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        entered_image_serializer = EnteredImageSerializer(data=request.data)
        if entered_image_serializer.is_valid():
            entered_image_serializer.save()
            return Response({'Successfully uploaded'}, status=status.HTTP_201_CREATED)
        return Response(entered_image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageToBlackAndWhite(APIView):
    def post(self, request, *args, **kwargs):
        image_file = request.FILES.get('image_file')

        if not image_file:
            return Response({'error': 'No image file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            entered_image = self.save_original_image(image_file)
            filtered_image = self.apply_black_and_white_filter(entered_image.image_file)
            filtered_image_obj = self.save_filtered_image(filtered_image, entered_image, 'black_and_white')

            entered_image_serializer = EnteredImageSerializer(entered_image)
            filtered_image_serializer = FilteredImageSerializer(filtered_image_obj)

            return Response({
                'entered_image': entered_image_serializer.data,
                'filtered_image': filtered_image_serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def save_original_image(self, image_file):
        entered_image = EnteredImage.objects.create(image_file=image_file)
        return entered_image

    def apply_black_and_white_filter(self, image_file):
        original_image = Image.open(image_file)
        black_and_white_image = ImageOps.grayscale(original_image)

        output_buffer = BytesIO()
        black_and_white_image.save(output_buffer, format='JPEG')
        output_buffer.seek(0)

        black_and_white_file = InMemoryUploadedFile(
            output_buffer,
            'image',
            f'{image_file.name.split(".")[0]}_bw.jpg',
            'image/jpeg',
            output_buffer.tell(),
            None
        )

        return black_and_white_file

    def save_filtered_image(self, filtered_image, entered_image, filter_used):
        filtered_image_obj = FilteredImage.objects.create(
            image_file=filtered_image,
            original_image=entered_image,
            filter_used=filter_used
        )
        return filtered_image_obj


class BlurFilter(APIView):
    def post(self, request, *args, **kwargs):
        image_file = request.FILES.get('image_file')

        if not image_file:
            return Response({'error': 'Image file is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            entered_image = self.save_original_image(image_file)
            filtered_image = self.apply_blur_filter(entered_image.image_file)
            filtered_image_obj = self.save_filtered_image(filtered_image, entered_image, 'blur_filter')

            entered_image_serializer = EnteredImageSerializer(entered_image)
            filtered_image_serializer = FilteredImageSerializer(filtered_image_obj)

            return Response({
                'entered_image': entered_image_serializer.data,
                'filtered_image': filtered_image_serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def save_original_image(self, image_file):
        entered_image = EnteredImage.objects.create(image_file=image_file)
        return entered_image

    def apply_blur_filter(self, image_file):
        original_image = Image.open(image_file)

        blur_effect_img = cv2.GaussianBlur(np.array(original_image), (35, 35), 0)

        blur_image = Image.fromarray(blur_effect_img)

        output_buffer = BytesIO()
        blur_image.save(output_buffer, format='JPEG')
        output_buffer.seek(0)

        filtered_image = InMemoryUploadedFile(
            output_buffer,
            'image',
            f'{image_file.name.split(".")[0]}_blur.jpg',
            'image/jpeg',
            output_buffer.tell(),
            None
        )

        return filtered_image

    def save_filtered_image(self, filtered_image, entered_image, filter_used):
        filtered_image_obj = FilteredImage.objects.create(
            image_file=filtered_image,
            original_image=entered_image,
            filter_used=filter_used
        )
        return filtered_image_obj


class ImageSketchFilter(APIView):
    def post(self, request, *args, **kwargs):
        image_file = request.FILES.get('image_file')

        if not image_file:
            return Response({'error': 'Image file is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            entered_image = self.save_original_image(image_file)
            filtered_image = self.apply_sketch_filter(entered_image.image_file)
            filtered_image_obj = self.save_filtered_image(filtered_image, entered_image)

            entered_image_serializer = EnteredImageSerializer(entered_image)
            filtered_image_serializer = FilteredImageSerializer(filtered_image_obj)

            return Response({
                'entered_image': entered_image_serializer.data,
                'filtered_image': filtered_image_serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def save_original_image(self, image_file):
        entered_image = EnteredImage.objects.create(image_file=image_file)
        return entered_image

    def apply_sketch_filter(self, image_file):
        original_image = Image.open(image_file)
        sketch_image = original_image.filter(ImageFilter.CONTOUR)

        output_buffer = BytesIO()
        sketch_image.save(output_buffer, format='JPEG')
        output_buffer.seek(0)

        filtered_image = InMemoryUploadedFile(
            output_buffer,
            'image',
            f'{image_file.name.split(".")[0]}_sketch.jpg',
            'image/jpeg',
            output_buffer.tell(),
            None
        )

        return filtered_image

    def save_filtered_image(self, filtered_image, entered_image):
        filtered_image_obj = FilteredImage.objects.create(
            image_file=filtered_image,
            original_image=entered_image,
            filter_used='sketch_filter'
        )
        return filtered_image_obj


class EmbossFilter(APIView):
    def post(self, request, *args, **kwargs):
        image_file = request.FILES.get('image_file')

        if not image_file:
            return Response({'error': 'Image file is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            entered_image = self.save_original_image(image_file)
            filtered_image = self.apply_emboss_filter(entered_image.image_file)
            filtered_image_obj = self.save_filtered_image(filtered_image, entered_image)

            entered_image_serializer = EnteredImageSerializer(entered_image)
            filtered_image_serializer = FilteredImageSerializer(filtered_image_obj)

            return Response({
                'entered_image': entered_image_serializer.data,
                'filtered_image': filtered_image_serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def save_original_image(self, image_file):
        entered_image = EnteredImage.objects.create(image_file=image_file)
        return entered_image

    def apply_emboss_filter(self, image_file):
        original_image = Image.open(image_file)

        original_image_np = np.array(original_image)

        emboss_kernel = np.array([[0, -1, -1], [1, 0, -1], [1, 1, 0]])

        emboss_effect_img = cv2.filter2D(original_image_np, -1, emboss_kernel)

        emboss_image = Image.fromarray(emboss_effect_img)

        output_buffer = BytesIO()
        emboss_image.save(output_buffer, format='JPEG')
        output_buffer.seek(0)

        filtered_image = InMemoryUploadedFile(
            output_buffer,
            'image',
            f'{image_file.name.split(".")[0]}_emboss.jpg',
            'image/jpeg',
            output_buffer.tell(),
            None
        )

        return filtered_image

    def save_filtered_image(self, filtered_image, entered_image):
        filtered_image_obj = FilteredImage.objects.create(
            image_file=filtered_image,
            original_image=entered_image,
            filter_used='emboss_filter'
        )
        return filtered_image_obj


class SharpenFilter(APIView):
    def post(self, request, *args, **kwargs):
        image_file = request.FILES.get('image_file')

        if not image_file:
            return Response({'error': 'Image file is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            entered_image = self.save_original_image(image_file)
            filtered_image = self.apply_sharpen_filter(entered_image.image_file)
            filtered_image_obj = self.save_filtered_image(filtered_image, entered_image, 'sharpen_filter')

            entered_image_serializer = EnteredImageSerializer(entered_image)
            filtered_image_serializer = FilteredImageSerializer(filtered_image_obj)

            return Response({
                'entered_image': entered_image_serializer.data,
                'filtered_image': filtered_image_serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def save_original_image(self, image_file):
        entered_image = EnteredImage.objects.create(image_file=image_file)
        return entered_image

    def apply_sharpen_filter(self, image_file):
        original_image = Image.open(image_file)

        sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])

        original_image_np = np.array(original_image)

        sharpen_effect_img = cv2.filter2D(original_image_np, -1, sharpen_kernel)

        sharpen_image = Image.fromarray(sharpen_effect_img)

        output_buffer = BytesIO()
        sharpen_image.save(output_buffer, format='JPEG')
        output_buffer.seek(0)

        filtered_image = InMemoryUploadedFile(
            output_buffer,
            'image',
            f'{image_file.name.split(".")[0]}_sharpen.jpg',
            'image/jpeg',
            output_buffer.tell(),
            None
        )

        return filtered_image

    def save_filtered_image(self, filtered_image, entered_image, filter_used):
        filtered_image_obj = FilteredImage.objects.create(
            image_file=filtered_image,
            original_image=entered_image,
            filter_used=filter_used
        )
        return filtered_image_obj


class SepiaFilter(APIView):
    def post(self, request, *args, **kwargs):
        image_file = request.FILES.get('image_file')

        if not image_file:
            return Response({'error': 'Image file is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            entered_image = self.save_original_image(image_file)
            filtered_image = self.apply_sepia_filter(entered_image.image_file)
            filtered_image_obj = self.save_filtered_image(filtered_image, entered_image, 'sepia_filter')

            entered_image_serializer = EnteredImageSerializer(entered_image)
            filtered_image_serializer = FilteredImageSerializer(filtered_image_obj)

            return Response({
                'entered_image': entered_image_serializer.data,
                'filtered_image': filtered_image_serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def save_original_image(self, image_file):
        entered_image = EnteredImage.objects.create(image_file=image_file)
        return entered_image

    def apply_sepia_filter(self, image_file):
        original_image = Image.open(image_file)

        sepia_kernel = np.array([[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]])

        original_image_np = np.array(original_image)

        sepia_effect_img = cv2.filter2D(original_image_np, -1, sepia_kernel)

        sepia_image = Image.fromarray(sepia_effect_img)

        output_buffer = BytesIO()
        sepia_image.save(output_buffer, format='JPEG')
        output_buffer.seek(0)

        filtered_image = InMemoryUploadedFile(
            output_buffer,
            'image',
            f'{image_file.name.split(".")[0]}_sepia.jpg',
            'image/jpeg',
            output_buffer.tell(),
            None
        )

        return filtered_image

    def save_filtered_image(self, filtered_image, entered_image, filter_used):
        filtered_image_obj = FilteredImage.objects.create(
            image_file=filtered_image,
            original_image=entered_image,
            filter_used=filter_used
        )
        return filtered_image_obj
