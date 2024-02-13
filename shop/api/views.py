from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer,CartSerializer,OrderSerializer
from rest_framework.views import APIView
from shop.models import Product,Category,CartItem,Order,Wallet,AdminWallet
from accounts.models import CustomUser
from rest_framework.response import Response
import razorpay
from django.conf import settings

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
    
    def post(self, request, *args, **kwargs):
        category_id=request.query_params.get('category_id')
        try:
            category=Category.objects.get(id=category_id)
            data=request.data
            pro_name=data['product_name']
            pro_image=data['product_image']
            price=data['price']
            qty=data['quantity']
            desc=data['description']

            product=Product.objects.create(product_name=pro_name,product_image=pro_image,price=price,quantity=qty,description=desc,category=category)

            context = {
                        'success': True,
                        'status': status.HTTP_201_CREATED,
                        'msg':'Product created successfully',
                        'data': ProductSerializer(product).data
                    }

            return Response(context)
        except Category.DoesNotExist:
            return Response({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'data': 'Category not found'
            })
        except Exception as e:
            return Response({
                'success': False,
                'data': str(e)
            })

    def put(self, request, *args, **kwargs):
        product_id=request.query_params.get('product_id')     
        category_id=request.query_params.get('category_id')     
        category=Category.objects.get(id=category_id)
        product=Product.objects.get(id=product_id)
        data=request.data
        pro_name=data['product_name']
        pro_image=data['product_image']
        price=data['price']
        qty=data['quantity']
        desc=data['description']

        product.product_name=pro_name
        product.product_image=pro_image
        product.price=price
        product.quantity=qty
        product.description=desc
        product.category=category
        product.save()

        context={
                'success':True,
                'status':status.HTTP_205_RESET_CONTENT,
                'msg':'Product update successfully',
                'data':ProductSerializer(product).data
            }
        return Response(context)
    
    def patch(self, request, *args, **kwargs):
        product_id=request.query_params.get('product_id')     
        category_id=request.query_params.get('category_id')     
        category=Category.objects.get(id=category_id)
        product=Product.objects.get(id=product_id)
        data = request.data
        pro_name = data.get('product_name', product.product_name)
        pro_image = data.get('product_image', product.product_image)
        price = data.get('price', product.price)
        qty = data.get('quantity', product.quantity)
        desc = data.get('description', product.description)

       
        product.product_name = pro_name
        product.product_image = pro_image
        product.price = price
        product.quantity = qty
        product.description = desc
        product.save()

        context={
                'success':True,
                'status':status.HTTP_205_RESET_CONTENT,
                'msg':'Product update successfully',
                'data':ProductSerializer(product).data
            }
        return Response(context)
    
    def delete(self, request, *args, **kwargs):
        product_id=request.query_params.get('product_id')
        try:
            product=Product.objects.get(id=product_id)
            product.delete()
            context={
                    'success':True,
                    'status':status.HTTP_204_NO_CONTENT,
                    'msg':'Product deleted successfully',
                    'data':{}
                }
            return Response(context)
        except Product.DoesNotExist:
            return Response({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'data': 'Product not found'
            })
        except Exception as e:
            return Response({
                'success': False,
                'data': str(e)
            })
        

class CartView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def post(self, request, *args, **kwargs):
        product_id=request.query_params.get('product_id')
        try:
            product=Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'data': 'Product not found'
            })
        cartitem,created=CartItem.objects.get_or_create(product=product,user=request.user)
        if product.quantity > 0:
            product.quantity-=1
            product.save()
            if not created:
                cartitem.quantity+=1
                cartitem.save()
            context={
                    'success':True,
                    'status':status.HTTP_201_CREATED,
                    'data':CartSerializer(cartitem).data
                }
            return Response(context)
        else:
            return Response({
                'success': False,
                'status': status.HTTP_400_BAD_REQUEST,
                'data': 'Product out of stock'
            })
    
    def delete(self, request, *args, **kwargs):
        product_id=request.query_params.get('product_id')
        try:
            product=Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'data': 'Product not found'
            })
        cartitem=CartItem.objects.get(product=product,user=request.user)

        if cartitem.quantity>=1 and cartitem.quantity is not None:
            product.quantity+=cartitem.quantity
            product.save()
        cartitem.delete()
        context={
                    'success':True,
                    'status':status.HTTP_204_NO_CONTENT,
                    'data':'Item remove successfully'
                    }
        return Response(context)
    
class UpdateQuantityView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        product_id = request.query_params.get('product_id')
        action = request.query_params.get('action')
        print(action, '==========1')

        try:
            product = Product.objects.get(id=product_id)
            cartitem = CartItem.objects.get(product=product, user=request.user)
        except Product.DoesNotExist:
            context = {
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Product not found'
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        except CartItem.DoesNotExist:
            context = {
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'CartItem not found'
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
       
   
        if action == 'increase':
            if product.quantity > 0 :
                cartitem.quantity += 1
                product.quantity -= 1
                product.save()
                cartitem.save()
                context = {
                    'success': True,
                    'status': status.HTTP_200_OK,
                    'data': CartSerializer(cartitem).data
                }
                return Response(context)
            else:
                context = {
                    'success': True,
                    'status': status.HTTP_400_BAD_REQUEST,
                    'data': 'Product out of stock'
                }
                return Response(context)
        elif action == 'decrease':
            if cartitem.quantity > 1:
                cartitem.quantity -= 1
                product.quantity += 1
                product.save()
                cartitem.save()
                context = {
                    'success': True,
                    'status': status.HTTP_200_OK,
                    'data': CartSerializer(cartitem).data
                }
                return Response(context)
            else:
                product.quantity += 1
                product.save()
               
                cartitem.delete()
                context = {
                    'success': True,
                    'status': status.HTTP_204_NO_CONTENT,
                    'data': 'CartItem deleted successfully'
                }
                return Response(context)

        else:
            print(f'Invalid action: {action}')
            context = {
                'success': False,
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Invalid action'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class CreateOrderView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def post(self, request, *args, **kwargs):
        product_id=request.query_params.get('product_id')
        product=Product.objects.get(id=product_id)
        user=CustomUser.objects.get(id=request.user.id)
        cartitem=CartItem.objects.filter(user=user)

        if not cartitem.exists():
            return Response({'msg':'Cart is empty'},status=status.HTTP_400_BAD_REQUEST)
        first_name=request.data.get('first_name')
        last_name=request.data.get('last_name')
        address=request.data.get('address')
        pincode=request.data.get('pincode')
        contact=request.data.get('contact')
        city=request.data.get('city')
        email=request.data.get('email')  
        order_data={
            'user':user.id,
            'product':product.id,
            'city':city,
            'pincode':pincode,
            'first_name':first_name,
            'last_name':last_name,
            'address':address,
            'email':email,
            'contact':contact
        }
        serializer=OrderSerializer(data=order_data)
        if serializer.is_valid():
            order=serializer.save()
            price=int(sum(item.subtotal() for item in cartitem))
            client=razorpay.Client(auth=(settings.KEY,settings.SECRET))
            payment=client.order.create({'amount': price*100, "currency": "INR", 'payment_capture': 1})
        
            order.razorpay_order_id=payment['id']
            
            cartitem.delete()
            order.save()
            context = {'success':True,
                'status':status.HTTP_201_CREATED,
                'payment': payment, 'total_price': price}
            return Response(context)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    def delete(self, request, *args, **kwargs):
        order_id=request.query_params.get('order_id')
        try:
            order=Order.objects.get(razorpay_order_id=order_id)
            order.delete()
            return Response({'message': f'Order {order_id} cancelled successfully.'}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'error': f'Order {order_id} not found.'}, status=status.HTTP_404_NOT_FOUND)
        

class PaymentSuccessView(APIView):
    def put(self, request, *args, **kwargs):
        order_id=request.query_params.get('order_id')
        try:
            user=CustomUser.objects.get(id=request.user.id)
            order = Order.objects.get(razorpay_order_id=order_id)
            admin=CustomUser.objects.get(email='admin@gmail.com')
           
        except Order.DoesNotExist:
            return Response({'error': 'Order not found or does not belong to the user'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
        
        order_amount=int(request.data.get('order_amount'))/100

        if order.is_paid:
            return Response({'error': 'Order is already paid'}, status=status.HTTP_400_BAD_REQUEST)
        buyerwallet=Wallet.objects.get(user=user)
        adminwallet,created=AdminWallet.objects.get_or_create(user=admin)
        if buyerwallet.balance>=order_amount:
            buyerwallet.balance-=order_amount
            adminwallet.balance+=order_amount
            order.is_paid =True     
            order.save()
            buyerwallet.save()
            adminwallet.save()
            serializer = OrderSerializer(order)
        else:
            order.is_paid=False
            order.save()
            return Response({'error':'Insufficent Balance'},status=status.HTTP_400_BAD_REQUEST)    

        return Response(serializer.data, status=status.HTTP_200_OK)


