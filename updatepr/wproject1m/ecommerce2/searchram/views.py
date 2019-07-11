from django.shortcuts import render
from django.views.generic import ListView

# Create your views here.
from product.models import Product

class SearchProductView(ListView):
    #queryset = product.objects.all()
    template_name = "searchram/view.html"

    def get_context_data(self, *args, **kwargs):
        context=super(SearchProductView , self).get_context_data(*args, **kwargs)
        query = self.request.GET.get("q")
        context["query"] = query
        #SearchQuery.objects.create(query=query)

        return context

    def get_queryset(self, *args, **kwargs ):
        request = self.request
        method_dict = request.GET
        query = method_dict.get("q", None)
        #print(query)
        if query is not None:
            # return product.objects.filter(title__icontains=query)
            return Product.objects.filter(Ram__icontains = query )
            # return product.objects.filter(memory__icontains=query)

        return Products.objects.featured()
        #return product.objects.filter(title__icontains="samsung")