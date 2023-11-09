from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import EnteredImageSerializer


class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        entered_image_serializer = EnteredImageSerializer(data=request.data)
        if entered_image_serializer.is_valid():
            entered_image_serializer.save()
            return Response({'Successfully uploaded'}, status=status.HTTP_201_CREATED)
        return Response(entered_image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
