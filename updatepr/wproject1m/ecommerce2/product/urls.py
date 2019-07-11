
from django.urls import path
from django.conf.urls import url

from .views import \
    (
    ProductListView, \
    # AccessoryListView,\
    ProductDetailSlugView,
    # Product_Acc_DetailSlugView
    advanced_search,
    UserProductHistoryView,
    review_detail,
    # review_list,
    add_review,
)

urlpatterns = [
    url(r'^$',ProductListView.as_view(), name="list"),
    # url(r'^accessories/$', ProductListView.search, name="alist"),
    url(r'^$', advanced_search, name="search"),

    url(r'^accessories/$', ProductListView.accessories_view, name="alist"),
    url(r'^Phones/$', ProductListView.phone_list_view, name="plist"),

    # url(r'^pproducts/$', ProductListView.pproduct_view, name="ppplist"),
    url(r'^pproducts/$', ProductListView.pproduct_view, name="pplist"),
    # url(r'^ppproducts/$', ProductListView.Popular, name="ppplist"),

    url(r'^history products/$', UserProductHistoryView.product_list_view, name="history"),

    url(r'^recommended products/$', UserProductHistoryView.product_history_list_view, name="recommendations"),

    url(r'^samsung products/$', ProductListView.samsung, name="samsunglist"),
    url(r'^apple products/$', ProductListView.apple, name="applelist"),
    url(r'^huawei products/$', ProductListView.huawei, name="huaweilist"),

    url(r'^10k products/$', ProductListView.less_than_10k, name="10klist"),
    url(r'^10kto20k products/$', ProductListView.RangeOf10k20k, name="10to20klist"),
    url(r'^20kto30k products/$', ProductListView.RangeOf20k30k, name="20to30klist"),
    url(r'^30k products/$', ProductListView.greater_than_30k, name="30klist"),

    url(r'^1GB products/$', ProductListView.One_GB, name="1GBlist"),
    url(r'^2GB products/$', ProductListView.Two_GB, name="2GBlist"),
    url(r'^3GB products/$', ProductListView.Three_GB, name="3GBlist"),
    url(r'^4GB products/$', ProductListView.Four_GB, name="4GBlist"),

    url(r'^5MP products/$', ProductListView.Five_MP, name="5MPlist"),
    url(r'^8MP products/$', ProductListView.Eight_MP, name="8MPlist"),
    url(r'^12MP products/$', ProductListView.Twelve_MP, name="12MPlist"),
    url(r'^12+MP products/$', ProductListView.TwelveMore_MP, name="12MP+list"),

    url(r'^review_list', ProductListView.review_list, name='review_list'),
    # ex: /review/5/
    url(r'^review/(?P<product_id>[0-9]+)/$', review_detail, name='review_detail'),
    url(r'^add_review/(?P<product_id>[0-9]+)/add_review/$', add_review, name='add_review'),


    # url(r'^Mobiles of Ten Thousand /$', ProductListView.Ten, name="Tenlist"),


    # url(r'^$',AccessoryListView.as_view(), name="alist"),
    url(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name="detail"),
    # url(r'^(?P<slug>[\w-]+)/$', Product_Acc_DetailSlugView.as_view(), name="adetail"),

]
