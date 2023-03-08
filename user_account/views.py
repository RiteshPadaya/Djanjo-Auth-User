from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from .serializer import UserSerializer
from rest_framework.response import Response 
from rest_framework import permissions
from rest_framework import status
import traceback
User=get_user_model()

# Create your views here.
class RegisterView(APIView):
    permission_classes=(permissions.AllowAny,)
    def post(self,request):

        try:
            data=request.data

            name=data["name"]
            email=data["email"]
            email=email.lower()
            phone=data["phone"]
            password=data["password"]
            re_password=data["re_password"]


           
            if password == re_password:
                if len(password)>=8:
                    if not  User.objects.filter(email=email).exists():
                        User.objects.create_user(name=name,email=email,phone=phone, password=password)
                        return Response({"sucess":"User created sucessfully"},status=status.HTTP_201_CREATED)

                    else:
                        return Response({'error':'email already exists'},status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"error":"Password must be at least 8 characters long"},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error":"Password did not matched"},status=status.HTTP_400_BAD_REQUEST)

        
        except :
            return Response({"error":"Some error occured "},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def patch(self, request):
        try:

            id=request.query_params.get('id')
            
            data=request.data
            previous_data=User.objects.get(id=id)
            
            
            
            ser=UserSerializer(previous_data, data=data,partial=True)
            if ser.is_valid():
                ser.save()
                return Response({"sucess":ser.data},status=status.HTTP_201_CREATED)
            return Response({"error": ser.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            traceback.print_exc()
            return Response({
                "error": "Somthing wrong happened while updating a User "+str(e) 
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UserView(APIView):

    def get(self, request, *args, **kwargs):
        users=User.objects.all()
        ser=UserSerializer(users,many=True)
        return Response({"users":ser.data})
        