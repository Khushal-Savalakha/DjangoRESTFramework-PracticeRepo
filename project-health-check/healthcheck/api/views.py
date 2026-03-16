# Create your views here.
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from .serializer import ServerHealthLogSerializer, AgentAuthSerializer
from healthcheck.models import ServerHealthLog
from services.renderer import get_response
from rest_framework_simplejwt.tokens import RefreshToken
from services.utils import extract_serializer_errors


class ServerHealthLogViewset(ModelViewSet):
    queryset = ServerHealthLog.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ServerHealthLogSerializer

    def get_queryset(self):
        print("IT IS COMING FROM HERE !!!")
        return super().get_queryset()

    @action(
        methods=["POST"],
        detail=False,
        url_path="system-health",
        url_name="system-health",
        permission_classes=[IsAuthenticated],
    )
    def create_system_health_log(self, request):
        try:
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()

            return get_response(
                is_success=True,
                message="System Health Log Added successfully",
                status_code=status.HTTP_200_OK,
                data=serializer.data,
            )

        except Exception as e:
            return get_response(
                is_success=True,
                message="Something Went Wrong!",
                status_code=status.HTTP_400_BAD_REQUEST,
                data=serializer.data,
                errors=str(e),
            )


class AgentAuthViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = AgentAuthSerializer

    @action(
        methods=["POST"],
        detail=False,
        url_path="token",
        url_name="agent-token",
    )
    def get_agent_token(self, request):
        try:
            email = request.data.get("email")
            password = request.data.get("password")
            user = AgentAuthSerializer.validate(self, data=request.data)
            if user:
                refresh = RefreshToken.for_user(user)
                return get_response(
                    is_success=True,
                    message="login successfully",
                    status_code=status.HTTP_200_OK,
                    data={
                        "access": str(refresh.access_token),
                    },
                )
        except Exception as e:
            return get_response(
                is_success=False,
                message="Invalid Credentials",
                status_code=status.HTTP_400_BAD_REQUEST,
                errors=extract_serializer_errors(e),
            )
