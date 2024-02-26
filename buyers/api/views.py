from .serializers import UserSerialzier,UserLoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
class UserRegisterView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=UserSerialzier(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                context={
                        'success':True,
                        'status':status.HTTP_201_CREATED,
                        'msg':'Registration Successful',
                        'data':serializer.data
                    }
                return Response(context)
            context={
                    'success':False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'msg':'Invalid Crediancial',
                    'data':serializer.errors
                }
            return Response(context)
        except Exception as e:
            context={
                    'success':False,
                    'status':status.HTTP_400_BAD_REQUEST,
                    'msg':'Invalid Crediancial',
                    'data':str(e)
                }
            return Response(context)
        
class UserLoginView(APIView):
    def post(self, request, *args,**kwargs):
        serializer=UserLoginSerializer(data=request.data)
        try:
            if serializer.is_valid():
                email=request.POST['email']
                password=request.POST['password']
                user=authenticate(email=email,password=password)

                if user:
                        
                    refresh = RefreshToken.for_user(user)
                    context={
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                    return Response(context)
                return Response({
                        'success':False,
                        'status':status.HTTP_401_UNAUTHORIZED,
                        'msg':'Invalid Credentials',
                        'data':{}
                    })
            return Response({
                            'success':False,
                            'status':status.HTTP_400_BAD_REQUEST,
                            'msg':'Login Failed',
                            'data':serializer.errors
                        })
        except Exception as e:
            context={
                        'success':False,
                        'status':status.HTTP_400_BAD_REQUEST,
                        'msg':'Invalid Crediancial',
                        'data':str(e)
                    }
            return Response(context)
        
 