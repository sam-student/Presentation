# from django.views import ListView
import csv, io

import pandas as pd
import numpy as np

import random
import statistics
# from django.contrib.auth.models import User
# from django.shortcuts import render
# from .filters import UserFilter

from django_pandas.io import read_frame

from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Avg, Max, Min, Sum


from django.http import Http404
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from carts.models import Cart
from .models import Product, Comments, Review
from accounts.models import User
from analytics.mixins import ObjectViewedMixin
from functools import reduce

from .forms import ReviewForm

from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

class ProductFeaturedListView(ListView):
    template_name = "product/list.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().featured()

# class AccessoryFeaturedListView(ListView):
#     template_name = "product/alist.html"
#
#     def get_queryset(self, *args, **kwargs):
#         request = self.request
#         return Product.objects.filter(category="Accessory")


class ProductFeaturedDetailView(LoginRequiredMixin, ObjectViewedMixin, DetailView):
    queryset = Product.objects.all().featured()
    template_name = "product/featured-detail.html"
    login_url = '/login/'
    redirect_field_name = 'redirect_to'


    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     return product.objects.featured()


class UserProductHistoryView(LoginRequiredMixin, ListView):
    #queryset = product.objects.all()
    template_name = "product/user-history.html"

    def get_context_data(self, *args, **kwargs):
        context = super(UserProductHistoryView, self).get_context_data(*args, **kwargs)
        print(context)
        return context

    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     views = request.user.objectviewed_set.by_model(Product)[:6]#.all().filter(content_type=='product')
    #     # viewed_ids = [x.object_id for x in views]
    #     # return views
    #
    #     context = {
    #         "object_list": views
    #     }
    #
    #     return render("product/user-history.html", context)

    def product_list_view(request):
        qs=Product.objects.all()
        views = request.user.objectviewed_set.by_model(Product)[:8]
        # qs = Product.objects.filter(brand__icontains=self.q, pk__in=views)
        # qs1 = qs.intersection(views).order_by('brand')
        # print(qs1)

        # paginator = Paginator(queryset_list, 12)  # Show 25 contacts per page
        # page = request.GET.get('page')
        # queryset = paginator.get_page(page)
        # queryset2 = Product.objects.filter(category="Accessory")
        # queryset2 = Product.objects.filter().select_related(views)
        # print(queryset2)
        context = {
            "object_list": views
        }

        return render(request, "product/user-history.html", context)

    def product_history_list_view(request):
        recommendations = []
        recommendations_ram = []
        recommendations_title = []

        qs=Product.objects.all()
        views = request.user.objectviewed_set.by_model(Product)[:8]
        # print(views)

        for p in views:
            obj = Product.objects.get(id=p.object_id)
            # print(obj.brand)
            recommendations.append(obj.brand)
            if obj.category == 'Phone':
                recommendations_ram.append(obj.Ram)
            recommendations_title.append(obj.title)
        print(recommendations_ram)
        print(recommendations_title)

            # obj.save()

        # for i in recommendations:
        #     print(type(i))


        # brand = Product.objects.in_bulk(['recommendations'], field_name='slug')
        # brand = Product.objects.filter(id__in=recommendations)

        # import operator
        #
        # clauses = (Q(address__icontains=p) for p in recommendations)
        # query = reduce(operator.or_, clauses)
        # site = Product.objects.filter(query)

        # qs_products = Product.objects.all()
        if recommendations:

            for values in recommendations:
                qs_brand = Product.objects.filter(brand=values)

            # print (qs_brand)

            import operator
            # ...
            condition = reduce(operator.or_, [Q(brand__icontains=s) for s in recommendations])
            condition_ram = reduce(operator.or_, [Q(Ram__icontains=r) for r in recommendations_ram])
            recommended_products = Product.objects.filter(condition)
            recommended_products_by_ram = Product.objects.filter(condition_ram)[:6]
            print(recommended_products_by_ram)


            # print (recommended_products)

            # condition = Q(brand__icontains=recommendations[0])
            # for string in recommendations[1:]:
            #     condition &= Q(brand__icontains=string)
            # bqs_brand = Product.objects.filter(condition)
            # print (bqs_brand)

            # q = Product.objects.all()
            #
            # print(q)

            # print(brand)


            # qs = Product.objects.filter(brand__icontains=self.q, pk__in=views)
            # qs1 = qs.intersection(views).order_by('brand')
            # print(qs1)

            # paginator = Paginator(queryset_list, 12)  # Show 25 contacts per page
            # page = request.GET.get('page')
            # queryset = paginator.get_page(page)
            # queryset2 = Product.objects.filter(category="Accessory")
            # queryset2 = Product.objects.filter().select_related(views)
            # print(queryset2)

            # paginator = Paginator(recommended_products, 12)  # Show 25 contacts per page
            # page = request.GET.get('page')
            # queryset_final = paginator.get_page(page)

            context = {
                "object_list": recommended_products,
                "ram_list":recommended_products_by_ram
            }
        else:

            context = {

            }



        return render(request, "product/user-recommendations.html", context)


    # def product_recommendation_view(request):
    #     queryset = request.user.objectviewed_set.by_model(Product)[:2]
    #     # paginator = Paginator(queryset_list, 12)  # Show 25 contacts per page
    #     # page = request.GET.get('page')
    #     # queryset = paginator.get_page(page)
    #     # queryset2 = Product.objects.filter(category="Accessory")
    #     print(queryset)
    #     queryset2 = Product.objects.select_related(queryset)
    #     context = {
    #         "object_list": queryset2
    #     }
    #
    #     return render(request, "product/user-history.html", context)




    # def product_list_view(request):
    #     queryset = Product.objects.all()
    #     # paginator = Paginator(queryset_list, 12)  # Show 25 contacts per page
    #     # page = request.GET.get('page')
    #     # queryset = paginator.get_page(page)
    #     # queryset2 = Product.objects.filter(category="Accessory")
    #
    #     context = {
    #         "object_list": queryset
    #     }
    #
    #     return render(request, "product/list.html", context)

class ProductListView(ListView):
    #queryset = product.objects.all()
    template_name = "product/list.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args ** kwargs)
    #     print(context)
    #     return context

    def get_queryset(self, *args, **kwargs ):
        request = self.request
        return Product.objects.all()


    def product_list_view(request):
        queryset = Product.objects.all()
        # queryset2 = Product.objects.filter(category="Accessory")

        context = {
            "object_list": queryset
        }

        return render(request, "product/list.html", context)

    def review_list(request):
        latest_review_list = Review.objects.order_by('-pub_date')[:9]
        print(latest_review_list)

        context = {'latest_review_list': latest_review_list}
        return render(request, 'product/review_list.html', context)

    def phone_list_view(request):
        queryset_list = Product.objects.filter(category="Phone").order_by('-price')
        # print (queryset_list)
        paginator = Paginator(queryset_list, 12)  # Show 25 contacts per page
        page = request.GET.get('page')
        queryset = paginator.get_page(page)


        context = {
            "object_list": queryset,
            "title":"Cell Phones"
        }

        return render(request, "product/list.html", context)

    from django.core.paginator import Paginator
    from django.shortcuts import render

    # def listing(request):
    #     contact_list = Contacts.objects.all()
    #     paginator = Paginator(contact_list, 25)  # Show 25 contacts per page
    #
    #     page = request.GET.get('page')
    #     contacts = paginator.get_page(page)
    #     return render(request, 'list.html', {'contacts': contacts})

    def accessories_view(request):
        queryset_list = Product.objects.filter(category="Accessory").order_by('-price')
        queryset1 = Product.objects.all().values('title','price','Average_Rating','Review_count')

        paginator = Paginator(queryset_list, 12)  # Show 25 contacts per page
        page = request.GET.get('page')
        queryset = paginator.get_page(page)

        context = {
            "object_list": queryset,
            "title" : "Accessories",
        }
        return render(request, "product/list.html", context)

    def samsung(request):
        queryset_list = Product.objects.filter(title__icontains="Samsung").order_by('-price')
        paginator = Paginator(queryset_list, 12)  # Show 25 contacts per page
        page = request.GET.get('page')
        queryset = paginator.get_page(page)
        context = {
            "object_list": queryset,
            "title": "Samsung Products",

        }
        return render(request, "product/list.html", context)

    def huawei(request):
        queryset_list = Product.objects.filter(title__icontains="huawei").order_by('-price')
        paginator = Paginator(queryset_list, 12)  # Show 25 contacts per page
        page = request.GET.get('page')
        queryset = paginator.get_page(page)
        context = {
            "object_list": queryset,
            "title": "Huawei Products",

        }
        return render(request, "product/list.html", context)

    def apple(request):
        queryset_list = Product.objects.filter(title__icontains="apple").order_by('-price')
        paginator = Paginator(queryset_list, 12)  # Show 25 contacts per page
        page = request.GET.get('page')
        queryset = paginator.get_page(page)
        context = {
            "object_list": queryset,
            "title": "Apple Products",

        }
        return render(request, "product/list.html", context)

    def less_than_10k(request):
        queryset_list = Product.objects.filter(price__lte="10000")
        paginator = Paginator(queryset_list, 12)  # Show 25 contacts per page
        page = request.GET.get('page')
        queryset = paginator.get_page(page)
        context = {
            "object_list": queryset,
            "title": "Below 10k Products",

        }
        return render(request, "product/list.html", context)

    def RangeOf10k20k(request):
        queryset_list = Product.objects.filter(price__range=(10000, 20000))
        paginator = Paginator(queryset_list, 12)  # Show 25 contacts per page
        page = request.GET.get('page')
        queryset = paginator.get_page(page)
        context = {
            "object_list": queryset,
            "title": "Products Ranging from 10k to 20k",

        }
        return render(request, "product/list.html", context)

    def RangeOf20k30k(request):
        queryset_list = Product.objects.filter(price__range=(20000, 30000))
        paginator = Paginator(queryset_list, 12)  # Show 25 contacts per page
        page = request.GET.get('page')
        queryset = paginator.get_page(page)
        context = {
            "object_list": queryset,
            "title": "Products Ranging from 20k to 30k",

        }
        return render(request, "product/list.html", context)

    def greater_than_30k(request):
        queryset_list = Product.objects.filter(price__gte="30000")
        paginator = Paginator(queryset_list, 12)  # Show 25 contacts per page
        page = request.GET.get('page')
        queryset = paginator.get_page(page)
        context = {
            "object_list": queryset,
            "title": "Products above 30k",

        }
        return render(request, "product/list.html", context)

    def One_GB(request):
        queryset_list = Product.objects.filter(Ram__icontains="1GB")
        paginator = Paginator(queryset_list, 12)  # Show 25 contacts per page
        page = request.GET.get('page')
        queryset = paginator.get_page(page)
        context = {
            "object_list": queryset,
            "title": "1GB Cell Phones",

        }
        return render(request, "product/list.html", context)

    def Two_GB(request):
        queryset_list = Product.objects.filter(Ram__icontains="2GB")
        paginator = Paginator(queryset_list, 12)  # Show 25 contacts per page
        page = request.GET.get('page')
        queryset = paginator.get_page(page)
        context = {
            "object_list": queryset,
            "title": "2GB Cell Phones",

        }
        return render(request, "product/list.html", context)

    def Three_GB(request):
        queryset_list = Product.objects.filter(Ram__icontains="3GB")
        paginator = Paginator(queryset_list, 12)  # Show 25 contacts per page
        page = request.GET.get('page')
        queryset = paginator.get_page(page)
        context = {
            "object_list": queryset,
            "title": "3GB Cell Phones",

        }
        return render(request, "product/list.html", context)

    def Four_GB(request):
        queryset_list = Product.objects.filter(Ram__icontains="4GB")
        paginator = Paginator(queryset_list, 12)  # Show 25 contacts per page
        page = request.GET.get('page')
        queryset = paginator.get_page(page)
        context = {
            "object_list": queryset,
            "title": "4GB or 4GB+ Cell Phones",

        }
        return render(request, "product/list.html", context)

    def Five_MP(request):
        queryset_list = Product.objects.filter(Main__icontains="5MP")
        paginator = Paginator(queryset_list, 12)  # Show 25 contacts per page
        page = request.GET.get('page')
        queryset = paginator.get_page(page)
        context = {
            "object_list": queryset,
            "title": "5MP Cell Phones",

        }
        return render(request, "product/list.html", context)

    def Eight_MP(request):
        queryset_list = Product.objects.filter(Main__icontains="8MP")
        paginator = Paginator(queryset_list, 12)  # Show 25 contacts per page
        page = request.GET.get('page')
        queryset = paginator.get_page(page)
        context = {
            "object_list": queryset,
            "title": "8MP Cell Phones",

        }
        return render(request, "product/list.html", context)

    def Twelve_MP(request):
        queryset_list = Product.objects.filter(Main__icontains="12MP")
        paginator = Paginator(queryset_list, 12)  # Show 25 contacts per page
        page = request.GET.get('page')
        queryset = paginator.get_page(page)
        context = {
            "object_list": queryset,
            "title": "12MP Cell Phones",

        }
        return render(request, "product/list.html", context)

    def TwelveMore_MP(request):
        queryset_list = Product.objects.filter(Main__icontains="12MP")
        paginator = Paginator(queryset_list, 12)  # Show 25 contacts per page
        page = request.GET.get('page')
        queryset = paginator.get_page(page)
        context = {
            "object_list": queryset,
            "title": "12MP+ Cell Phones",

        }
        return render(request, "product/list.html", context)

    def pproduct_view(request):

        current_average = []
        current_review_count = []
        predicted_products = []
        predicted_products_result = []

        qs = Product.objects.all()

        queryset = Product.objects.all().values('title','price','Average_Rating','Review_count')
        # print(queryset)
        for avg in queryset:
            current_average.append(float(avg['Average_Rating']))
            current_review_count.append(float(avg['Review_count']))

        print(current_average)
        average_result = sum(current_average)/len(current_average)
        print(average_result)

        minimum_criteria = np.quantile(current_review_count, 0.7)
        print(minimum_criteria)

        for avr,rc in zip(current_average,current_review_count):
            print(avr,"  ",rc)
            predicted_products = (rc / (rc + minimum_criteria) * avr) + (minimum_criteria / (minimum_criteria + rc) * average_result)
            print(avr," ",rc," ",predicted_products)
            predicted_products_result.append(predicted_products)


        print(predicted_products)



        # Product.Populrity_Score.append('predicted_products')

        queryset = Product.objects.all()

        # print(len(queryset))
        for value, p in enumerate(queryset):
            obj = Product.objects.get(id=p.id)
            obj.Populrity_Score=predicted_products_result[value]
            obj.save()

        # print(queryset)

        # obj = Product('Populrity_Score')

        queryset1_list = Product.objects.order_by('-Populrity_Score')
        print(queryset1_list)
        paginator = Paginator(queryset1_list, 12)  # Show 25 contacts per page
        page = request.GET.get('page')
        queryset_final = paginator.get_page(page)


        # for current_average,current_review_count in list_data:

        # print(result)



        # queryset1 = np.mean(Product.Average_Rating)
        #
        # queryset2 = Product.objects.values('Review_count').quantile(0.90)
        # print (queryset2)



        # for p in qs:
        #
        #
        # df = read_frame(qs)
        # df1 = df.head()

        context = {

            "object_list": queryset_final,
            "title": "Top Rated Products"

        }

        return render(request, "product/plist.html", context)



    # def Ten(request):
    #     queryset = Product.objects.filter(price="10000")
    #
    #     context = {
    #         "object_list": queryset
    #     }
    #     return render(request, "product/list.html", context)
    #
    # def TenToTwenty(request):
    #     queryset = Product.objects.filter(price="10000")
    #
    #     context = {
    #         "object_list": queryset
    #     }
    #     return render(request, "product/list.html", context)
    #
    # def TwentyToThirty(request):
    #     queryset = Product.objects.filter(price="10000")
    #
    #     context = {
    #         "object_list": queryset
    #     }
    #     return render(request, "product/list.html", context)

# class AccessoryListView(ListView):
#     #queryset = product.objects.all()
#     template_name = "product/alist.html"
#
#     # def get_context_data(self, *args, **kwargs):
#     #     context = super(ProductListView, self).get_context_data(*args ** kwargs)
#     #     print(context)
#     #     return context
#
#     def get_queryset(self, *args, **kwargs ):
#         request = self.request
#         return Product.objects.filter(category="Accessory")
#
#
#     def accessory_list_view(request):
#         queryset = Product.objects.filter(category="Accessory")
#         context = {
#             "object_list": queryset
#         }
#
#         return render(request, "product/alist.html", context)


class ProductDetailSlugView(LoginRequiredMixin, ObjectViewedMixin, DetailView):
    queryset = Product.objects.all()
    template_name = "product/detail.html"
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get_context_data(self,*args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        print(self.object.id)
        # reviews=Review.objects.get(pk=self.object.id)
        # print(reviews)
        latest_review_list = Review.objects.all().order_by('-pub_date')
        review=[]
        # review_type=[]
        for obj in latest_review_list:
            if obj.product.id == self.object.id:
                review.append(obj.rating)
                review_count = len(review)
                review_type=int(review_count)
                mean_rating=statistics.mean(review)
                obj = Product.objects.get(id=self.object.id)
                obj.R_C=review_type
                obj.A_R=mean_rating
                obj.save()



        # print(review_count)
        # print(type(review_type))
        # print (type(mean_rating))
        # for review in latest_review_list:
        #     reviews_for = Review.objects.get()
        # print(reviews_for)

        #     average_reviews= Review.objects.all().aggregate(Avg('rating'))
        # # print (average_reviews)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        context['latest_review_list'] = latest_review_list


        # context = \
        #     {'review_list':review_list,
        #      'cart':cart_obj,
        #      'object':queryset
        #      }


        return context

    # def get_object(self, *args, **kwargs):
    #     request = self.request
    #     slug = self.kwargs.get("slug")
    #     #instance = get_object_or_404(product , slugs=slug, active=True)
    #
    #     try:
    #         instance = Product.objects.get(slug=slug,active=True)
    #     except Product.DoesNotExist:
    #         raise Http404("Not found..")
    #     except Product.MultipleObjectsReturned:
    #         qs = Product.objects.filter(slug=slug,active=True)
    #         instance=qs.first()
    #     except:
    #         raise Http404("Uhmm")
    #
    #     # object_viewed_signal.send(instance.__class__, instance=instance, request=request)
    #     return instance


# class Product_Acc_DetailSlugView(DetailView):
#     queryset = Product.objects.all()
#     template_name = "product/adetail.html"
#
#     def get_context_data(self,*args, **kwargs):
#         context = super(Product_Acc_DetailSlugView, self).get_context_data(*args, **kwargs)
#         cart_obj, new_obj = Cart.objects.new_or_get(self.request)
#         context['cart'] = cart_obj
#         return context
#
#     def get_object(self, *args, **kwargs):
#         request = self.request
#         slug = self.kwargs.get("slug")
#         #instance = get_object_or_404(product , slugs=slug, active=True)
#
#         try:
#             instance = Product.objects.get(slug=slug,active=True)
#         except Product.DoesNotExist:
#             raise Http404("Not found..")
#         except Product.MultipleObjectsReturned:
#             qs = Product.objects.filter(slug=slug,active=True)
#             instance=qs.first()
#         except:
#             raise Http404("Uhmm")
#
#         return instance

# class ProductDetailView(LoginRequiredMixin, ObjectViewedMixin, DetailView):
#     #queryset = product.objects.all()
#     template_name = "product/detail.html"
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
#         # print(context)
#         # context['abc'] = 123
#         return context
#
#     def get_object(self, *args, **kwargs):
#         request =self.request
#         pk = self.kwargs.get("pk")
#         instance = Product.objects.get_by_id(pk)
#         if instance is None:
#             raise Http404("product doesn't exist")
#         return instance
#
#     # def get_queryset(self, *args, **kwargs ):
#     #     request = self.request
#     #     pk = self.kwargs.get("pk")
#     #     return product.objects.filter(pk=pk)
#
#
# def product_detail_view(request, pk=None, *args, **kwargs):
#         #instance = product.objects.get(pk=pk, featured=True)
#         #instance = get_object_or_404(Prdoduct, pk=pk , featured=True)
#     # try:
#     #     instance =product.objects.get(id=pk)
#     # except product.DoesNotExist:
#     #     print('no product here')
#     #     raise Http404("product does,not exist")
#     # except:
#     #     print("huh?")
#
#     # latest_review_list = Review.objects.get_by_id(pk).order_by('-pub_date')[:9]
#     # print(latest_review_list)
#     instance = Product.objects.get_by_id(pk)
#     if instance is None:
#         raise Http404("product doesn't exist")
#     # print(instance)
#     #
#     # qs = product.objects.filter(id=pk)
#     # if qs.exists() and qs.count() ==1:
#     #     instance = qs.first()
#     # else:
#     #     raise Http404("product does,not exist")
#
#     context = {
#         "object": instance,
#         # "latest_review_list": latest_review_list,
#     }
#     return render(request, "product/detail.html", context)


# def review_list(request):
#     latest_review_list = Review.objects.order_by('-pub_date')[:9]
#     print(latest_review_list)
#
#     context = {'latest_review_list': latest_review_list}
#     return render(request, 'product/review_list.html', context)

def review_d_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list': latest_review_list}
    return render(request, 'product/review_list.html', context)

def review_detail(request, product_id):
    review = get_object_or_404(Review, pk=product_id)
    return render(request, 'product/detail.html', {'review': review})


def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        user_name = form.cleaned_data['user_name']
        review = Review()
        review.product = product
        review.user_name = user_name
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('product:detail', args=(product.slug,)))

    return render(request, 'product/add_review.html', {'product': product, 'form': form})




@permission_required('admin.can_add_log_entry')
def product_upload(request):
    template = 'product_upload.html'

    prompt = {
        'order': 'Order of our csv should be like your model'
    }


    if request.method == 'GET':
        return render(request, template , prompt)

    csv_file= request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request,"this is not a csv file")

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=",", quotechar="|" ):
       _, created = Product.objects.update_or_create(
            title=column[0],
            slug=column[1],
            category=column[2],
            price=column[3],
            Charging=column[4],
            Torch=column[5],
            Games=column[6],
            Messaging=column[7],
            Browser=column[8],
            Audio=column[9],
            Data=column[10],
            NFC=column[11],
            USB =column[12],
            GPS=column[13],
            Bluetooth=column[14],
            Wifi=column[15],
            Front=column[16],
            Main=column[17],
            card=column[18],
            BuiltIn=column[19],
            Features=column[20],
            Protection=column[21],
            Resolution=column[22],
            Size=column[23],
            Technology=column[24],
            GPU=column[25],
            Chipset=column[26],
            CPU=column[27],
            FourGBand=column[28],
            ThreeGBand=column[29],
            TwoGBand=column[30],
            Color=column[31],
            SIM=column[32],
            Weight=column[33],
            Dimension=column[34],
            UIBuild=column[35],
            OperatingSystem=column[36],
            image=column[37],
            image1=column[38],
            image2=column[39],
            Review_count=column[40],
            Average_Rating=column[41],
            Reviews=column[42],
            Ram=column[43],
            Populrity_Score=column[44],
            Knowledge_Score=column[45],
        )

    context ={}
    return render(request, template, context)

def advanced_search(request):
    template = 'product/snippets/search_form.html';
    context = {}
    return render(request, template, context)