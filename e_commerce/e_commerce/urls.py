"""e_commerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from mainapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeListView.as_view() , name='home'),
    path('base/', views.BaseListView.as_view() , name='base'),
    path('product/<int:pk>/', views.ItemDetailView.as_view(), name='product'),
    path('order/', views.OrderListView.as_view(), name = 'order_register'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add-to-cart'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove-from-cart'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('category_list/', views.CategoryList.as_view(), name='category_list'),
    path('category_details/<int:pk>', views.ItemsListView,name="category_details"),
    path('thank_you/', views.thank_you,name="thank_you"),
    path('checkout/', views.CheckOutCreateView.as_view() , name = 'checkout'),
    path('', include('django.contrib.auth.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

