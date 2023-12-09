"""

"""
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status


class ModelViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    pass


def custom_response(status=status.HTTP_200_OK, detail=None, data=None):
    """
    common method to use return a response
    """
    return Response({'status': status, 'detail': detail, 'data': data})


def custom_error_response(status=status.HTTP_400_BAD_REQUEST, detail=None, data='something went wrong'):
    """
    common method to return a error response
    """
    return Response({'data': data, 'detail': detail}, status=status)
