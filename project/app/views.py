from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from .serializer import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .openai_integration import generate_openai_prompt
from .google_calendar import *

@api_view(['POST'])
def integrate_google_calendar(request):
    trigger_signin()
    return Response("welcome")

@api_view(['POST'])
def handle_user_input(request, input_data):
    event = generate_openai_prompt(input_data)
    response = create_event(event)
    return response

class ReactView(APIView):
    serializer_class=DataSerializer
    def get(self, request):
        output = [{"userInput": output.userInput, "date": output.date} for output in UserData.objects.all()]
        return Response(output)
    
    def post(self, request):
        serializer = DataSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
