from django.conf import settings
from rest_framework import views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class AppleAppSiteAssociationView(views.APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        return Response(settings.APPLE_APP_SITE_ASSOCIATION)
