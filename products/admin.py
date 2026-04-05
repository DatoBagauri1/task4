from django.contrib import admin
from .models import Product, ProductImage, ProductTag, FavoriteProduct, Cart, Review


admin.site.register(Product)
admin.site.register(ProductImage)
@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
admin.site.register(FavoriteProduct)
admin.site.register(Cart)
admin.site.register(Review)
