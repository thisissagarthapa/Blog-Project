from django.urls import path
from .views import BlogAPiView,PublicApiView,SingleBlogApiView
urlpatterns = [
    path('blog/',BlogAPiView.as_view(),name='blog'),
    path('public-blog/', PublicApiView.as_view(), name='public_blogs'),
    path('blogs/<uuid:uuid>/', SingleBlogApiView.as_view(), name='single_blog')
]
