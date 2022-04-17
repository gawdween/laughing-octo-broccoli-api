
from django.contrib.auth import login
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import permissions
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from api.models import User, CustomerTransaction, CustomerProfile
from api.serializers import UserSerializer, RegisterSerializer, StaffUserSerializer, CustomerTransactionSerializer
from api.permissions import IsOwnerOrReadOnly




# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


class CreateStaffUserAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": StaffUserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class CustomerTransactionList(generics.ListCreateAPIView):
    queryset = CustomerTransaction.objects.all()
    serializer_class = CustomerTransactionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = (TokenAuthentication,)
    
    def perform_create(self, serializer):
        user = User.objects.get(user=self.request.user)
        serializer.save(owner=user)
        

    

class CustomerTransactionDetail(generics.RetrieveAPIView):
    queryset = CustomerTransaction.objects.all()
    serializer_class = CustomerTransactionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class OwnTransactions(generics.ListAPIView):
    """
    List all transactions by a customer
    """
    model = CustomerTransaction
    queryset = CustomerTransaction.objects
    serializer_class = CustomerTransactionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        owner = self.request.user
        product_owner = CustomerProfile.objects.get(user=owner)
        return self.queryset.filter(owner=product_owner).order_by('-timestamp')