from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth import login , logout
from django.core.mail import send_mail
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from knox.models import AuthToken
from knox.views import LoginView , LogoutView  
from knox.auth import TokenAuthentication
from .serializers import *

User = get_user_model()


class SignUpAPI(generics.GenericAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]
    authentication_classes = (TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if request.data['avatar'] :
            user.avatar = request.data['avatar']
            user.save()
        if request.data['lang'] :
            user.language = request.data['lang']
            user.save()
        return Response({
            "users": UserSerializer(user, context=self.get_serializer_context()).data
            })

class SignInAPI(LoginView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token_ttl = self.get_token_ttl()
        instance, token = AuthToken.objects.create(user, token_ttl)
        data = self.get_post_response_data(token, instance , user=user)
        login(request=request , user=user)
        return Response(data)
        
    def get_post_response_data(self,token, instance , user):
        serializer_data = UserSerializer(user).data,
        data = {
            'user':serializer_data,
            'expiry': self.format_expiry_datetime(instance.expiry),
            'token': token
        }
        return data


class Logout(LogoutView):
    def post(self, request, format=None):
        logout(request=request)
        super().post(request=request, format=format)
        return Response({
            'status':status.HTTP_205_RESET_CONTENT,
            'msg':_("logout successfully")})

@api_view(['PUT' , 'PATCH'])
def update_user_name(request):
    data = request.data
    try:
        user = User.objects.get(id = data['user_id'])
        user.first_name = data['fname'] if (data['fname']) else user
        user.last_name = data['lname'] if (data['lname']) else user
        user.save()
        serialized_data = UserSerializer(user)
        return Response(serialized_data.data)
    except:
        raise Exception('Failed to update user name')


@api_view(['PATCH'])
def password_reset(request):
    data = request.data
    try:
        user = User.objects.get(id=data['user_id']) 
        pass_reset_data = PasswordReset.objects.filter(user = data['user_id'])
        if  data['new_password'] == data['conf_new_password'] and user.check_password(data['new_password']):
            user.set_password(data['new_password'])
        else:
            return Response({'msg':'password miss match'})
        return Response(data={'msg':_('password modified successfully')})
    except:
        return Response(data={'msg' : _('error while processing the request')})

def send_password_reset_code_mail_to_user(request):
    # here a mail containing the the pass word reset code
    # to the user mail with a given email
    user_id = request.data['user']
    user = User.objects.get(pk=user_id)
    send_mail(subject='welcome mail' , 
              message='your password reset code is' , 
              from_email="Allianzcm@Gmail.com" , 
              recipient_list=[
        user.email
    ])
    pass