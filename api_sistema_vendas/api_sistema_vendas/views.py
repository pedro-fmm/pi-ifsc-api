from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def health(request):
    """
    Healthcheck
    """
    response = {"status": "olha só quem ta na pista"}
    return Response(response, status=status.HTTP_200_OK)
