from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('category/<slug:category_slug>/', views.ProductListView.as_view(), name='product_list_by_category'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('comment/<int:product_id>/', views.CommentCreateView.as_view(), name='comment_create'),
]