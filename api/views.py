from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from base.models import Credentials
from .serializers import CredentialsSerializer
from nanoid import generate
from time import time
from django.shortcuts import get_object_or_404


class CredentialsApiView(APIView):
    def get(self, request, *args, **kwargs):
        credentials = Credentials.objects.all()
        serializer = CredentialsSerializer(credentials, many=True)
        data = {"data": serializer.data, "size": len(serializer.data)}

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        data["id"] = generate(size=8)
        data["created_at"] = int(time() * 1000)
        serializer = CredentialsSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"error": serializer._errors}, status=status.HTTP_400_BAD_REQUEST
            )


class SingleSiteCredentials(APIView):
    def get(self, request, *args, **kwargs):
        website = kwargs["site"]
        credentials = Credentials.objects.filter(website=website).order_by(
            "-created_at"
        )
        serializer = CredentialsSerializer(credentials, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SingleCredentials(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs["id"]
        credentials = get_object_or_404(Credentials, id=id)

        serializer = CredentialsSerializer(credentials, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        id = kwargs["id"]
        credentials = get_object_or_404(Credentials, id=id)
        data = request.data
        serializer = CredentialsSerializer(credentials, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"error": serializer._errors}, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, *args, **kwargs):
        id = kwargs["id"]
        credentials = get_object_or_404(Credentials, id=id)
        serializer = CredentialsSerializer(credentials, many=False)
        data = serializer.data
        credentials.delete()
        return Response(data, status=status.HTTP_200_OK)
