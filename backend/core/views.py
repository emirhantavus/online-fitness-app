from django.shortcuts import render , get_object_or_404
from .serializers import (bannerSerializer , VideoSerializer ,VideoSerializerDetail,
                          VideoInstructionSerializer ,ContactSerializer)
from .models import (Banners , ExerciseVideo ,VideoInstruction,Contact)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
import requests

class BannersList(ModelViewSet):
    permission_classes =[AllowAny]
    pagination_class = None
    queryset = Banners.objects.all().order_by('id')
    serializer_class = bannerSerializer
    
    
class VideoViewSet(ModelViewSet):
    queryset = ExerciseVideo.objects.all()
    serializer_class = VideoSerializer
    lookup_field = 'slug'

    
class VideoDetailViewSet(APIView):
    def get(self, request, slug):
        video = get_object_or_404(ExerciseVideo, slug=slug)
        serializer = VideoSerializerDetail(video)
        return Response(serializer.data)
  
class ContactView(APIView):
    permission_classes = [AllowAny,]
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class NutritionAPIView(APIView):
    permission_classes= [AllowAny]
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query')
        if not query:
            return Response({"error": "Query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        api_url = f'https://api.api-ninjas.com/v1/nutrition?query={query}'
        response = requests.get(api_url, headers={'X-Api-Key': '5MCogr99STvi4rEr0OJVQQ==UfPF2PcAfbOKe7yM'})

        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        else:
            return Response({"error": "Error fetching nutrition data"}, status=response.status_code)