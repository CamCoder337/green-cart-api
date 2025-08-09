"""
API views for cart management in GreenCart.
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Cart, CartItem
from .serializers import (
    CartSerializer,
    CartItemSerializer,
    AddToCartSerializer,
    UpdateCartItemSerializer
)
from products.models import Product


class CartViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for cart management (consumer only)."""
    
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return only the current user's cart."""
        return Cart.objects.filter(consumer=self.request.user)
    
    def get_object(self):
        """Get or create cart for current user."""
        cart, created = Cart.objects.get_or_create(consumer=self.request.user)
        return cart
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current user's cart."""
        cart, created = Cart.objects.get_or_create(consumer=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def clear(self, request):
        """Clear current user's cart."""
        cart, created = Cart.objects.get_or_create(consumer=request.user)
        cart.clear()
        return Response({'message': 'Cart cleared successfully.'})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_to_cart(request):
    """Add product to cart."""
    serializer = AddToCartSerializer(
        data=request.data,
        context={'request': request}
    )
    
    if serializer.is_valid():
        cart_item = serializer.save()
        item_serializer = CartItemSerializer(cart_item)
        return Response({
            'message': 'Product added to cart successfully.',
            'cart_item': item_serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_cart_item(request, item_id):
    """Update cart item quantity."""
    try:
        cart = Cart.objects.get(consumer=request.user)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    except Cart.DoesNotExist:
        return Response(
            {'error': 'Cart not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = UpdateCartItemSerializer(
        data=request.data,
        context={'cart_item': cart_item}
    )
    
    if serializer.is_valid():
        updated_item = serializer.save()
        
        if updated_item is None:
            return Response({'message': 'Item removed from cart.'})
        
        item_serializer = CartItemSerializer(updated_item)
        return Response({
            'message': 'Cart item updated successfully.',
            'cart_item': item_serializer.data
        })
    
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def remove_from_cart(request, item_id):
    """Remove item from cart."""
    try:
        cart = Cart.objects.get(consumer=request.user)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        cart_item.delete()
        
        return Response({'message': 'Item removed from cart successfully.'})
    
    except Cart.DoesNotExist:
        return Response(
            {'error': 'Cart not found.'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_product_to_cart(request, product_id):
    """Add specific product to cart by product ID."""
    try:
        product = Product.objects.get(id=product_id, is_active=True)
    except Product.DoesNotExist:
        return Response(
            {'error': 'Product not found or not active.'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Get quantity from request, default to 1
    quantity = request.data.get('quantity', 1)
    
    # Validate quantity
    try:
        quantity = int(quantity)
        if quantity <= 0:
            return Response(
                {'error': 'Quantity must be positive.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    except (ValueError, TypeError):
        return Response(
            {'error': 'Invalid quantity.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check stock
    if product.quantity_available < quantity:
        return Response(
            {'error': f'Not enough stock. Only {product.quantity_available} available.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Get or create cart
    cart, created = Cart.objects.get_or_create(consumer=request.user)
    
    # Add product to cart
    cart_item = cart.add_product(product, quantity)
    
    item_serializer = CartItemSerializer(cart_item)
    return Response({
        'message': 'Product added to cart successfully.',
        'cart_item': item_serializer.data
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def cart_summary(request):
    """Get cart summary with totals."""
    cart, created = Cart.objects.get_or_create(consumer=request.user)
    
    summary = {
        'total_items': cart.total_items,
        'total_amount': cart.total_amount,
        'items_count': cart.items_count,
        'is_empty': cart.items_count == 0,
        'has_unavailable_items': any(not item.is_available() for item in cart.items.all())
    }
    
    return Response(summary)