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
        order_by = request.query_params.get("order_by")
        page = int(request.query_params.get("page"))
        start = 10 * (page - 1)
        end = 10 * page
        if order_by == "last_used":
            credentials = Credentials.objects.all().order_by("-updated_at")[start:end]
        else:
            credentials = Credentials.objects.all().order_by("website")[start:end]
        size = Credentials.objects.all().count()
        serializer = CredentialsSerializer(credentials, many=True)
        data = {"data": serializer.data, "size": size}

        if len(serializer.data) == 0:
            return Response(
                {"error": "No more credentials found."},
                status=status.HTTP_404_NOT_FOUND,
            )

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
            "-updated_at", "-created_at"
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
