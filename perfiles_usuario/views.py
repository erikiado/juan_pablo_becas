from rest_framework import parsers, renderers, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import is_member
from .utils import ADMINISTRADOR_GROUP, CAPTURISTA_GROUP


class ObtainAuthToken(APIView):
    """ View to Obtain an authentication Token

        View for a user to provide credentials and obtain an authentication Token.
        This view is a refactor of:
        https://github.com/tomchristie/django-rest-framework/blob/master/rest_framework/authtoken/views.py#L21

        This view incorporates validation that only certain group users can obtain
        authentication through the API.

        The view creates or retrieves a Token for a user and returns it in JSON format.
    """
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if is_member(user, [ADMINISTRADOR_GROUP, CAPTURISTA_GROUP]):
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})

        return Response(status=status.HTTP_400_BAD_REQUEST)
