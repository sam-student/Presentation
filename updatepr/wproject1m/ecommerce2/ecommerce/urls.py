"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from rate.views import review_detail,wine_list,wine_detail,add_review
from django.urls import path
from django.conf.urls import  url

from django.conf import settings
from django.conf.urls.static import static,settings

from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView


from product.views import product_upload,ProductListView,ProductFeaturedDetailView,ProductFeaturedListView,ProductDetailSlugView


# from pproducts.views import product_list_view,product_detail_view


# from huaweiproducts.views import huaweiproduct_upload,product_list_view,product_detail_view




from billing.views import payment_method_view, payment_method_createview
from carts.views import cart_home
from accounts.views import LoginView,RegisterView, guest_register_view
from addresses.views import checkout_address_create_view, checkout_address_reuse_view
from .views import home_page,about_page,contact_page,cart_page

urlpatterns = [
    url(r'^$',home_page, name="home"),
    url(r'^about/$',about_page, name="about"),
    url(r'^contact/$',contact_page, name="contact"),
    url(r'^login/$',LoginView.as_view(), name="login"),
    url(r'^checkout/address/create/$', checkout_address_create_view, name="checkout_address_create"),
    url(r'^checkout/address/reuse/$', checkout_address_reuse_view, name="checkout_address_reuse"),
    url(r'^register/guest/$', guest_register_view, name="guest_register"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^billing/payment-method/$', payment_method_view, name="billing-payment-method"),
    url(r'^billing/payment-method/create/$', payment_method_createview, name="billing-payment-method-endpoint"),
    url(r'^register/$',RegisterView.as_view(), name="register"),
    url(r'^bootstrap/$',TemplateView.as_view(template_name="bootstrap/example.html")),
    url(r'^products/',include(("products.urls","products"), namespace = "products")),
    url(r'^product/', include(("product.urls", "product"), namespace="product")),
    # url(r'^product/', include(("product.urls", "product"), namespace="product")),
    url(r'^account/', include(("accounts.urls", "accounts"), namespace="account")),
    url(r'^orders/', include(("orders.urls", "orders"), namespace="orders")),
    path('',include('stocks.urls')),
    url(r'^accessories/', include(("accessories.urls", "accessories"), namespace="accessories")),

    url(r'^search/', include(("search.urls", "search"), namespace="search")),
    url(r'^searchprice/', include(("searchprice.urls", "searchprice"), namespace="searchprice")),
    url(r'^searchram/', include(("searchram.urls", "searchram"), namespace="searchram")),
    url(r'^searchknowledge/', include(("searchknowledge.urls", "searchknowledge"), namespace="searchknowledge")),

    url(r'^cart/$', cart_home, name="cart"),
    url(r'^cart/', include(("carts.urls", "carts"), namespace="cart")),

    path('upload-csv/', product_upload, name="product_upload"),
    path('upload-apple-csv/', product_upload, name="aproduct_upload"),

    url(r'^review/(?P<review_id>[0-9]+)/$', review_detail, name='review_detail'),
    # ex: /wine/
    url(r'^show/', wine_list, name='wine_list'),
    # ex: /wine/5/
    url(r'^wine/(?P<wine_id>[0-9]+)/$', wine_detail, name='wine_detail'),
    url(r'^wine/(?P<wine_id>[0-9]+)/add_review/$', add_review, name='add_review'),

    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
