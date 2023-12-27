from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer


# class CustomTokenObtainPairView(TokenObtainPairView):
#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)
#         refresh = response.data.get('refresh')
#         access = response.data.get('access')
#         user_id = self.request.user.id

#         if refresh and access:
#             # Revoke all refresh tokens for the user
#             OutstandingToken.objects.filter(user=self.request.user, token=refresh).delete()

#             # Generate a new refresh token
#             new_refresh_token = RefreshToken.for_user(self.request.user)
#             response.data['refresh'] = str(new_refresh_token)
#             response.data['user_id'] = user_id

#         return response
    
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh = response.data.get('refresh')
        access = response.data.get('access')
        user_id = self.user.id  # Adapte isso de acordo com seu modelo de usuário

        if refresh and access:
            refresh_token = RefreshToken(refresh)
            refresh_token.blacklist()
            refresh_token = RefreshToken.for_user(self.user)
            response.data['refresh'] = str(refresh_token)
            response.data['user_id'] = user_id

        return response
    
class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)