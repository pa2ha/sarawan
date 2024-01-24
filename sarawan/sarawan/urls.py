from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from products.views import CartViewSet, CategoryViewSet, ProductViewSet
from rest_framework.routers import DefaultRouter

from .drf_yasg import schema_view

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
    path('redoc/', schema_view.with_ui('redoc',
                                       cache_timeout=0), name='schema-redoc'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
                                         cache_timeout=0), name='schema'
                                                                '-swagger-ui'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
