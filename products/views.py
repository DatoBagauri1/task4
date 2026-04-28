
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from rest_framework import status
from .serializers import ProductSerializer

# @api_view(['GET', 'POST'])
# def products(request):
#     if request.method == "GET":
#         products = Product.objects.all()
#         product_list = []

#         for product in products:
#             product_data = {
#                 'id': product.id,
#                 'name': product.name,
#                 'description': product.description,
#                 'price': product.price,
#                 'currency': product.currency,
#             }
#             product_list.append(product_data)

#         return Response({'products': product_list})
#     elif request.method == "POST":
#         data = request.data
#         serializer = ProductSerializer(data=data)
#         if serializer.is_valid():
#             new_product = Product.objects.create(
#                 name=data.get("name"),
#                 description=data.get("description"),
#                 price=data.get("price"),
#                 currency=data.get("currency"),
#             )

#             return Response({"new product": {
#                 'id': new_product.id,
#                 'name': new_product.name,
#                 'description': new_product.description,
#                 'price': new_product.price,
#                 'currency': new_product.currency,
#             }}, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def products(request):
    if request.method == "GET":
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        data = request.data
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            product = serializer.save()

            return Response({"new product": product.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
from .serializers import ReviewSerializer, CartSerializer
from .models import Review, Cart


@api_view(['GET', 'POST'])
def review_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        review_list = []

        for review in reviews:
            review_data = {
                'review_id': review.id,
                'product_id': review.product.id,
                'content': review.content,
                'rating': review.rating
            }
            review_list.append(review_data)

        return Response({'reviews': review_list})

    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            review = serializer.save()
            return Response(
                {'id': review.id, 'message': 'Review created successfully!'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


class ProductView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class ProductDetail(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    










from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    RetrieveModelMixin,
    CreateModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
)

from .models import Product
from .serializers import ProductSerializer


class ProductAPIView(RetrieveModelMixin,
                    CreateModelMixin,
                    ListModelMixin,
                    UpdateModelMixin,
                    DestroyModelMixin,
                    GenericAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    



from rest_framework.permissions import IsAuthenticated

from .models import FavoriteProduct  
from .serializers import FavoriteProductSerializer  


class FavoriteProductViewSet(ListModelMixin,
                            CreateModelMixin,
                            DestroyModelMixin,
                            RetrieveModelMixin,
                            GenericAPIView):
    
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset

    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)








class CartView(ListModelMixin,
            CreateModelMixin,
            GenericAPIView):
    
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset

    def get(self, request, pk=None, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


from .models import ProductTag
from .serializers import ProductTagSerializer

class TagView(ListModelMixin, GenericAPIView):
    
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.viewsets import ModelViewSet

class TagList(ListAPIView):
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer
    permission_classes = [IsAuthenticated]


class ReviewView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset.filter(product_id=self.kwargs['product_id'])
        return queryset







from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .pagination import ProductPagination
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle, ScopedRateThrottle


from .permissions import IsObjectOwnerOrReadOnly
from rest_framework.exceptions import PermissionDenied

class ReviewModelViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsObjectOwnerOrReadOnly]
    pagination_class = ProductPagination

    def perform_update(self, serializer):
        review = self.get_object()
        if review.user != self.request.user:
            raise PermissionDenied("You do not have permission to update this review.")
        serializer.save()





class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['price', 'currency']
    search_fields = ['name']
    pagination_class = ProductPagination
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    # throttle_classes = [ScopedRateThrottle]
    # throttle_scope = 'ragaca'





















from .models import ProductImage
from .serializers import ProductImageSerializer


class ProductImageViewSet(ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        return self.queryset.filter(product__id=self.kwargs['product_pk'])
    




from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, get_connection


@csrf_exempt
def send_email_view(request):
    if request.method == "GET":

        sender_email = "khomaainfo@gmail.com"
        app_password = "nqiv lpxw nhxg wnkq"

        subject = "Hardcoded Test Email"
        message = "This email was sent from Django using hardcoded values."
        recipient = "giokhomaa@gmail.com"

        try:
            connection = get_connection(
                backend="django.core.mail.backends.smtp.EmailBackend",
                host="smtp.gmail.com",
                port=587,
                username=sender_email,
                password=app_password,
                use_tls=True,
            )

            send_mail(
                subject,
                message,
                sender_email,
                [recipient],
                connection=connection,
                fail_silently=False,
            )

            return JsonResponse({"message": "Email sent successfully"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only GET allowed"}, status=405)