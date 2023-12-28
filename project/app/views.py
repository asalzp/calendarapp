import logging
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import View
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


class FrontendAppView(View):
    """
    Serves the compiled frontend entry point (only works if you have run `yarn
    run build`).
    """
    def get(self, request):
            print (os.path.join(settings.BASE_DIR, 'build', 'index.html'))
            try:
                with open(os.path.join(settings.BASE_DIR, 'build', 'index.html')) as f:
                    return HttpResponse(f.read())
            except FileNotFoundError:
                logging.exception('Production build of app not found')
                return HttpResponse(
                    """
                    This URL is only used when you have built the production
                    version of the app. Visit http://localhost:3000/ instead, or
                    run `yarn run build` to test the production version.
                    """,
                    status=501,
                )

# class ReactView(APIView):
#     serializer_class=DataSerializer
#     def get(self, request):
#         output = [{"userInput": output.userInput, "date": output.date} for output in UserData.objects.all()]
#         return Response(output)
    
#     def post(self, request):
#         serializer = DataSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data)
        
