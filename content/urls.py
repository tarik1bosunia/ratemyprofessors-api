from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'content', views.ContentViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'likes', views.LikeViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Include all the routes registered in the router
    path('comments/<int:content_id>/', views.CommentListView.as_view(), name='comment-list'),
]