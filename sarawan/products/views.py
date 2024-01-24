
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from .models import Cart, CartItem, Category, Product
from .permission import IsOwnerOrReadOnly
from .serializers import CartSerializer, CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        # Возвращаем только корзину текущего пользователя
        return Cart.objects.filter(user=self.request.user)

    def get_object(self):
        # Возвращаем корзину текущего пользователя
        return Cart.objects.get(user=self.request.user)

    def create(self, request, *args, **kwargs):
        cart = Cart.objects.create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        cart = self.get_object()
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        if product_id and quantity:
            product = Product.objects.get(pk=product_id)
            cart_item = CartItem.objects.get_or_create(cart=cart,
                                                       product=product)

            cart_item.quantity = quantity
            cart_item.save()

            return Response({'detail': 'Product quantity'
                             'updated successfully'})

        return Response({'detail': 'Invalid data provided'},
                        status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        cart = self.get_object()
        product_id = request.data.get('product_id')

        if product_id:
            try:
                product = Product.objects.get(pk=product_id)
                cart_item = CartItem.objects.get(cart=cart, product=product)
                cart_item.delete()
                return Response({'detail': 'Product removed'
                                 'from cart successfully'})
            except CartItem.DoesNotExist:
                return Response({'detail': 'Product not found in the cart'},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            cart.clear_cart()
            serializer = CartSerializer(cart)
            return Response(serializer.data)
