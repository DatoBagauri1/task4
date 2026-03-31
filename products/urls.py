from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter, DefaultRouter

urlpatterns = [
    # path("products/", views.products, name="products"),
    # path("reviews/", views.review_view, name="review_view"),

    # path('product-apiview/', views.ProductView.as_view(), name='product'),
    # path('product-apiview/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),

    # path('products-genericapiview/', views.ProductAPIView.as_view(), name="products_genericapiview"),
    # path('products-genericapiview/<int:pk>', views.ProductAPIView.as_view(), name='product_genericapiview'),

    # path("favorite-product/", views.FavoriteProductViewSet.as_view(), name="favorite_product"),
    # path("favorite-product/<int:pk>/", views.FavoriteProductViewSet.as_view()),

    # path("cart-flow/", views.CartView.as_view()),

    # path("tag-list/", views.TagView.as_view()),
    # path("tags/", views.TagList.as_view()),

    # path("review-view/<int:product_id>/", views.ReviewView.as_view()),

    # path('product-model-view-set/', views.ProductModelViewSet.as_view({"get": "list", "post": "create"})),
    # path('product-model-view-set/<int:pk>/', views.ProductModelViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"})),

]

from rest_framework_nested import routers

# router = SimpleRouter()
router = DefaultRouter()
router.register('products', views.ProductModelViewSet)

product_router = routers.NestedDefaultRouter(
    router,
    'products',
    lookup='product',
)

product_router.register('images', views.ProductImageViewSet, basename="product_image")

urlpatterns += router.urls
urlpatterns += product_router.urls