# from django.views import ListView
from django.http import Http404
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404

# Create your views here.
from carts.models import Cart
from .models import Products

class ProductFeaturedListView(ListView):
    template_name = "products/list.html"

    def get_queryset(self, *args, **kwargs ):
        request = self.request
        return Products.objects.all().featured()


class ProductFeaturedDetailView(DetailView):
    queryset = Products.objects.all().featured()
    template_name = "products/featured-detail.html"

    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     return product.objects.featured()

class ProductListView(ListView):
    #queryset = product.objects.all()
    template_name = "products/list.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args ** kwargs)
    #     print(context)
    #     return context

    def get_queryset(self, *args, **kwargs ):
        request = self.request
        return Products.objects.all()


def product_list_view(request):
    queryset = Products.objects.all()
    context = {
        "object_list": queryset
    }

    return render(request, "products/list.html", context)

class ProductDetailSlugView(DetailView):
    queryset = Products.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self,*args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get("slug")
        #instance = get_object_or_404(product , slugs=slug, active=True)

        try:
            instance = Products.objects.get(slug=slug,active=True)
        except Products.DoesNotExist:
            raise Http404("Not found..")
        except Products.MultipleObjectsReturned:
            qs = Products.objects.filter(slug=slug,active=True)
            instance=qs.first()
        except:
            raise Http404("Uhmm")

        return instance

class ProductDetailView(DetailView):
    #queryset = product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        # context['abc'] = 123
        return context

    def get_object(self, *args, **kwargs):
        request =self.request
        pk = self.kwargs.get("pk")
        instance = Products.objects.get_by_id(pk)
        if instance is None:
            raise Http404("product doesn't exist")
        return instance

    # def get_queryset(self, *args, **kwargs ):
    #     request = self.request
    #     pk = self.kwargs.get("pk")
    #     return product.objects.filter(pk=pk)


def product_detail_view(request, pk=None, *args, **kwargs):
        #instance = product.objects.get(pk=pk, featured=True)
        #instance = get_object_or_404(Prdoduct, pk=pk , featured=True)
    # try:
    #     instance =product.objects.get(id=pk)
    # except product.DoesNotExist:
    #     print('no product here')
    #     raise Http404("product does,not exist")
    # except:
    #     print("huh?")

    instance = Products.objects.get_by_id(pk)
    if instance is None:
        raise Http404("product doesn't exist")
    # print(instance)
    #
    # qs = product.objects.filter(id=pk)
    # if qs.exists() and qs.count() ==1:
    #     instance = qs.first()
    # else:
    #     raise Http404("product does,not exist")

    context = {
        "object": instance
    }
    return render(request, "products/detail.html", context)


