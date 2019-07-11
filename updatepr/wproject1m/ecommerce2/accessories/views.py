# from django.views import ListView
from django.http import Http404
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404

# Create your views here.
from carts.models import Cart
from .models import Accessories

class ProductFeaturedListView(ListView):
    template_name = "accessories/list.html"

    def get_queryset(self, *args, **kwargs ):
        request = self.request
        return Accessories.objects.all().featured()


class ProductFeaturedDetailView(DetailView):
    queryset = Accessories.objects.all().featured()
    template_name = "accessories/featured-detail.html"

    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     return Accessories.objects.featured()

class ProductListView(ListView):
    #queryset = Accessories.objects.all()
    template_name = "accessories/list.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(AccessoriesListView, self).get_context_data(*args ** kwargs)
    #     print(context)
    #     return context

    def get_queryset(self, *args, **kwargs ):
        request = self.request
        return Accessories.objects.all()


def Product_list_view(request):
    queryset = Accessories.objects.all()
    context = {
        "object_list": queryset
    }

    return render(request, "accessories/list.html", context)

class ProductDetailSlugView(DetailView):
    queryset = Accessories.objects.all()
    template_name = "accessories/detail.html"

    def get_context_data(self,*args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get("slug")
        #instance = get_object_or_404(Accessories , slugs=slug, active=True)

        try:
            instance = Accessories.objects.get(slug=slug,active=True)
        except Accessories.DoesNotExist:
            raise Http404("Not found..")
        except Accessories.MultipleObjectsReturned:
            qs = Accessories.objects.filter(slug=slug,active=True)
            instance=qs.first()
        except:
            raise Http404("Uhmm")

        return instance

class ProductDetailView(DetailView):
    #queryset = Accessories.objects.all()
    template_name = "accessories/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        # context['abc'] = 123
        return context

    def get_object(self, *args, **kwargs):
        request =self.request
        pk = self.kwargs.get("pk")
        instance = Accessories.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Accessories doesn't exist")
        return instance

    # def get_queryset(self, *args, **kwargs ):
    #     request = self.request
    #     pk = self.kwargs.get("pk")
    #     return Accessories.objects.filter(pk=pk)


def Product_detail_view(request, pk=None, *args, **kwargs):
        #instance = Accessories.objects.get(pk=pk, featured=True)
        #instance = get_object_or_404(Prdoduct, pk=pk , featured=True)
    # try:
    #     instance =Accessories.objects.get(id=pk)
    # except Accessories.DoesNotExist:
    #     print('no Accessories here')
    #     raise Http404("Accessories does,not exist")
    # except:
    #     print("huh?")

    instance = Accessories.objects.get_by_id(pk)
    if instance is None:
        raise Http404("Accessories doesn't exist")
    # print(instance)
    #
    # qs = Accessories.objects.filter(id=pk)
    # if qs.exists() and qs.count() ==1:
    #     instance = qs.first()
    # else:
    #     raise Http404("product does,not exist")

    context = {
        "object": instance
    }
    return render(request, "accessories/detail.html", context)


