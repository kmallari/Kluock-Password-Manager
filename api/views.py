from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Credentials
from .serializers import CredentialsSerializer


@api_view(["GET"])
def getData(request):
    # person = {"name": "Kevin", "age": 23}
    credentials = Credentials.objects.all()
    serializer = CredentialsSerializer(credentials, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def addCredentials(request):
    serializer = CredentialsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)
