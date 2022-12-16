from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializer import UsersSerializer
from .models import User
from .permissions import EmployeePermission, EmployeeRestrictPermission


class UserView(APIView):
    
    authentication_classes = [JWTAuthentication]    
    permission_classes = [IsAuthenticated, EmployeeRestrictPermission]
    
    def get(self, request):
        
        users = User.objects.all()
        serializer = UsersSerializer(users, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = UsersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)

class UserDetailView(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, EmployeePermission]
    
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        
        self.check_object_permissions(request, user)
        
        serializer = UsersSerializer(user)
        
        return Response(serializer.data)
        