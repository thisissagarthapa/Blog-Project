from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import BlogSerializers
from .models import BlogModel
from django.db.models import Q
from django.core.paginator import Paginator

class BlogAPiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self,request):
        try:
            blog=BlogModel.objects.filter(user=request.user)
            if request.GET.get('search'):
                search=request.GET.get('search')
                blog=BlogModel.objects.filter(Q(title__icontains=search)| Q(blog_text__icontains=search))
            serializer=BlogSerializers(blog,many=True)
            return Response({
                'msg':'data fetched successfully',
                'data':serializer.data
            })
            
        except Exception as e:
            print(e)
            return Response({
                'msg':'something went wrong',
                'data':{},           
                },status=status.HTTP_400_BAD_REQUEST)
            
    
    def post(self, request):
        data = request.data.copy()  
        
        data['user'] = request.user.id
        
        serializer = BlogSerializers(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'msg': 'Blog created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'msg': 'Something went wrong',
            'errors': serializer.errors 
        }, status=status.HTTP_400_BAD_REQUEST)
        
        
            
    def patch(self, request):
        try:
            data = request.data
            # Use the correct field name for UUID
            blogs = BlogModel.objects.filter(uuid=data.get('uuid'))

            if not blogs.exists():
                return Response({
                    'data': {},
                    'msg': 'Invalid blog UUID',
                }, status=status.HTTP_400_BAD_REQUEST)

            if request.user != blogs[0].user:
                return Response({
                    'data': {},
                    'msg': 'You are not authorized to update this blog',
                }, status=status.HTTP_403_FORBIDDEN) 

            serializer = BlogSerializers(blogs[0], data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'msg': 'Blog updated successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK) 

            return Response({
                'msg': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({
                'msg': 'Something went wrong',
                'data': {},
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self,request):
        try:
            data = request.data
            blogs = BlogModel.objects.filter(uuid=data.get('uuid'))

            if not blogs.exists():
                return Response({
                    'data': {},
                    'msg': 'Invalid blog UUID',
                }, status=status.HTTP_400_BAD_REQUEST)

            if request.user != blogs[0].user:
                return Response({
                    'data': {},
                    'msg': 'You are not authorized to delete this blog',
                }, status=status.HTTP_403_FORBIDDEN)
                
            blogs[0].delete()
            return Response({
                    'msg': 'Blog deleted successfully',
                    'data': {}
                }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(e)
            return Response({
                'msg': 'Something went wrong',
                'data': {},
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class PublicApiView(APIView):
    def get(self, request):
        try:
            blog = BlogModel.objects.all()
            
            if request.GET.get('search'):
                search = request.GET.get('search')
                blog = BlogModel.objects.filter(Q(title__icontains=search) | Q(blog_text__icontains=search))
            page_number = request.GET.get('page', 1)
            paginator = Paginator(blog, 10)  
            page_obj = paginator.get_page(page_number)
            serializer = BlogSerializers(page_obj, many=True)
            return Response({
                'msg': 'Data fetched successfully',
                'data': serializer.data,
                'total_pages': paginator.num_pages, 
                'current_page': page_obj.number, 
            })
        except Exception as e:
            print(e)
            return Response({
                'msg': 'Something went wrong or invalid page',
                'data': {},
            }, status=status.HTTP_400_BAD_REQUEST)

class SingleBlogApiView(APIView):
    def get(self, request, uuid):
        try:
            blog = BlogModel.objects.filter(uuid=uuid).first()
            if not blog:
                return Response({
                    'msg': 'Blog not found',
                    'data': {},
                }, status=status.HTTP_404_NOT_FOUND)
            serializer = BlogSerializers(blog)
            return Response({
                'msg': 'Blog fetched successfully',
                'data': serializer.data
            })
        except Exception as e:
            print(e)
            return Response({
                'msg': 'Something went wrong',
                'data': {},
            }, status=status.HTTP_400_BAD_REQUEST)
         