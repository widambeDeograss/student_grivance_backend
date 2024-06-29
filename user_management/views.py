from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, ChangePasswordSerializer
from django.contrib.auth import authenticate, login, update_session_auth_hash
from .token import get_user_token
from .models import User
from rest_framework.generics import UpdateAPIView


class RegisterUser(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        data = request.data
        serializer = UserSerializer(data=data)
        if not serializer.is_valid():
            errors = serializer.errors
            print(errors)
            return Response({'save': False, 'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            email = data['email']
            user = User.objects.filter(email=email)
            if user:
                message = {'status': False, 'message': 'email already exists'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            message = {'save': True}
            return Response(message)

        message = {'save': False, 'errors': serializer.errors}
        return Response(message)
# {
# "first_name":"Ditso",
# "last_name":"Ditso",
# "email":"ditsohealth@dit.co.tz",
# "password":"ditsohealth123",
# "username":"DitsoHealth",
# "phone_number":"078676726",
# "role":4,
# }


class LoginView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        email = request.data.get('email')
        password = request.data.get('password')
        print('Data: ', email, password)
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            user_id = User.objects.get(email=email)
            user_info = UserSerializer(instance=user_id, many=False).data
            response = {
                'token': get_user_token(user_id),
                'user': user_info
            }

            return Response(response)
        else:
            response = {
                'msg': 'Invalid username or password',
            }

            return Response(response)
#
# {
#     "username":"johnlukundo",
#     "password":"12345"
# }


class UserInformation(APIView):

    @staticmethod
    def get(request):
        query_type = request.GET.get("querytype")
        if query_type == 'single':
            try:
                user_id = request.GET.get('user_id')
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'message': 'User Does Not Exist'})
            return Response(UserSerializer(instance=user, many=False).data)

        elif query_type == 'all':
            queryset = User.objects.all()
            return Response(UserSerializer(instance=queryset, many=True).data)

        else:
            return Response({'message': 'Wrong Request!'})


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': True,
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserChangeRoles(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        id = request.data['id']
        role = request.data['role']

        try:
            user = User.objects.get(id=id)

            if user:
                user.role = role
                user.save()
            return Response({'save': True, "user": UserSerializer(instance=user, many=False).data})
        except User.DoesNotExist:
            return Response({'save': False, 'message': 'User doest exist'})


class UpdateUserView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        email = request.data.get('email')
        fname = request.data.get('first_name')
        lname = request.data.get('last_name')
        phone_number = request.data.get('phone_number')
        username = request.data.get('username')

        if phone_number:
            try:
                query = User.objects.get(email=email)
                query.first_name = fname
                query.last_name = lname
                query.phone_number = phone_number
                query.username = username
                query.save()
                return Response({'save': True, "user": UserSerializer(instance=query, many=False).data})
            except User.DoesNotExist:
                return Response({'message': 'User does not exist or you cannot change the email'}, status=400)
        else:
            return Response({'message': 'Phone number is required'}, status=400)


class LoggedInUser(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        user = request.user

        if user:
            loggedin = User.objects.get(email=user.email)
            return Response(UserSerializer(instance=loggedin, many=False).data)
        else:
            message = {
                "loggedIn": False,
                "msg": "Loggin session expired"
            }
            return Response(message)


class UpdateUserProfilePictureView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        email = request.data.get('email')
        profile = request.data.get('profile')

        if not profile:
            return Response({'message': 'Profile picture is required'}, status=400)

        try:
            user = User.objects.get(email=email)
            user.update_profile_picture(profile)
            return Response({'save': True, "user": UserSerializer(instance=user, many=False).data})
        except User.DoesNotExist:
            return Response({'message': 'User does not exist or you cannot change the email'}, status=400)


