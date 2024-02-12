from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer
from rest_framework.views import APIView
from shop.models import Product,Category
from rest_framework.response import Response

class ProductView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def get(self, request, *args, **kwargs):
        
        product=Product.objects.all()
        serializer=ProductSerializer(product,many=True)
        context={
            'success':True,
            'status':status.HTTP_200_OK,
            'data':serializer.data
        }
        return Response(context)

    