from django.urls import path, include
from rest_framework.routers import DefaultRouter

from article import views

router = DefaultRouter()
router.register('tags', views.TagViewSet)

app_name = 'article'

urlpatterns = [
    path('', include(router.urls))
]