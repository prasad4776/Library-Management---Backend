from django.urls import include

from rest_framework.routers import DefaultRouter
from django.conf.urls import url

from .views import BookViewSet, AuthorViewSet, IssueViewSet, ObtainAuthToken, LogoutView  # ,LoginView, LogoutView

router = DefaultRouter()
router.register('book', BookViewSet, basename='book')
router.register('author', AuthorViewSet, basename='author')
router.register('issue', IssueViewSet, basename='issue')

urlpatterns = [
    url('', include(router.urls)),
    url('api/v1/auth/login/', ObtainAuthToken.as_view()),
    url('api/v1/auth/logout/', LogoutView.as_view()),
]
