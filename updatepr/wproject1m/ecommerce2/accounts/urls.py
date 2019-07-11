from django.conf.urls import url
from product.views import UserProductHistoryView


urlpatterns = [

    url(r'history/product/$', UserProductHistoryView.as_view(), name='user-product-history')


]