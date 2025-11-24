from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

from .serializer import StatusSerializer, ErrorSerializer
from .models import ErrorReport


@api_view(['GET'])
def get_server_status(request):
    data = {'status': 'running', 'date': datetime.now()}
    serializer = StatusSerializer(data)
    return Response(serializer.data)


@api_view(['GET'])
def get_errors(request):
    errors = ErrorReport.objects.all()
    serializer = ErrorSerializer(errors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_error_from_code(request, code):
    try:
        e = ErrorReport.objects.get(code=code)
    except ErrorReport.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ErrorSerializer(e)
    return Response(serializer.data)


@api_view(['POST'])
def create_error(request):
    serializer = ErrorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def object_update(request, id):
    try:
        obj = ErrorReport.objects.get(id=id)
    except ErrorReport.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ErrorSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
