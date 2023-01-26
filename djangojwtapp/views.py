from rest_framework.views import APIView
from djangojwtapp.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class RegisterView(APIView):
    @staticmethod
    def post(request):
        user = UserSerializer(data=request.data)
        user.is_valid(raise_exception=True)
        user.save()

        return Response(user.data)


class UserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = self.request.user
        return Response(UserSerializer(user).data)
