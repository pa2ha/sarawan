from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from products.views import CartViewSet, CategoryViewSet, ProductViewSet
from rest_framework.routers import DefaultRouter

v1_router = DefaultRouter()
v1_router.register('category', CategoryViewSet)
v1_router.register('product', ProductViewSet)
v1_router.register('cart', CartViewSet, )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(v1_router.urls)),
    path('auth/', include('djoser.urls')),
    # JWT-эндпоинты, для управления JWT-токенами:
    path('auth/', include('djoser.urls.jwt')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
