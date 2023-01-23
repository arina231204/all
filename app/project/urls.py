from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from accounts import views as acc_view
from posts import views as po_view




ac_router = routers.DefaultRouter()
ac_router.register('register', acc_view.AuthorViewSet, basename='Author')

po_router = routers.DefaultRouter()
po_router.register('posts', po_view.PostsViewSet)
po_router.register('rating', po_view.RatingViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Yandex API",
      default_version='v-0.01-alpha',
      description="API для взаимодействия с Yandex API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="arinaten23@gmail.com"),
      license=openapi.License(name="No Licence"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(ac_router.urls)),
    path('api/', include(po_router.urls)),
    path('api/auth/', include('rest_framework.urls')),
    path('api/auth/token/', obtain_auth_token),
    path('comments/', po_view.CommentsList.as_view(),),
    path('comments/<int:pk>/', po_view.CommentsDetail.as_view()),
    path('swagger/', schema_view.with_ui('swagger'),  name='swagger_doc' ),
]
