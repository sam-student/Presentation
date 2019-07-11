from django.shortcuts import render
from django.views.generic import ListView
from django import forms

import numpy as np

# Create your views here.
from product.models import Product

class SearchProductView(ListView):
    #queryset = A_Product.objects.all()
    template_name = "searchknowledge/view.html"

    def get_context_data(self, *args, **kwargs):
        context=super(SearchProductView , self).get_context_data(*args, **kwargs)
        query = self.request.GET.get("q")
        query1 = self.request.GET.get("q1")
        query2 = self.request.GET.get("q2")
        query3 = self.request.GET.get("q3")

        context["query"] = query
        context["query1"] = query1
        context["query2"] = query2
        context["query3"] = query3



        #SearchQuery.objects.create(query=query)

        return context

    def get_queryset(self, *args, **kwargs ):
        request = self.request
        method_dict = request.GET
        query = method_dict.get("q", None)
        query1 = method_dict.get("q1", None)
        query2 = method_dict.get("q2", None)
        query3 = method_dict.get("q3", None)



        #print(query)
        if query is not None:

            queryset = Product.objects.filter(title__icontains=query).filter(price__range=(query1, query2)).filter(
                Color__icontains=query3)
            # print(queryset)
            if queryset:

                current_average = []
                current_review_count = []
                predicted_products = []
                predicted_products_result = []
                knowledge_list = []

                queryset1 = queryset.values('title', 'price', 'Average_Rating', 'Review_count')
                print(queryset1)

                # print(queryset)
                for avg in queryset1:
                    current_average.append(float(avg['Average_Rating']))
                    current_review_count.append(float(avg['Review_count']))

                print(current_average)
                average_result = sum(current_average) / len(current_average)
                print(average_result)

                minimum_criteria = np.quantile(current_review_count, 0.7)
                print(minimum_criteria)

                for avr, rc in zip(current_average, current_review_count):
                    print(avr, "  ", rc)
                    predicted_products = (rc / (rc + minimum_criteria) * avr) + (
                            minimum_criteria / (minimum_criteria + rc) * average_result)
                    print(avr, " ", rc, " ", predicted_products)
                    predicted_products_result.append(predicted_products)

                print(predicted_products_result)

                # queryset4 = Product.objects.filter(pk__in = predicted_products_result)
                # Product.Populrity_Score.append('predicted_products')

                queryset3 = Product.objects.all()
                # print(queryset3)
                # print(len(queryset)
                for value, p in enumerate(queryset):
                    obj = Product.objects.get(id=p.id)
                    #     print("objj: ", obj)
                    obj.Knowledge_Score = predicted_products_result[value]
                    obj.save()

            # li[value+1]

            # print(queryset)

            # obj = Product('Populrity_Score')

                queryset2 = Product.objects.all().filter(title__icontains=query).filter(price__range=(query1,query2)).filter(Color__icontains=query3)
                queryset4 = queryset2.order_by('-Knowledge_Score')
                print(queryset4)

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
            else:
                queryset4 = Product.objects.filter(title__icontains=query).filter(price__range=(query1, query2)).filter(
                Color__icontains=query3)
                print('No result found')

            context = {

                "object_list": queryset4
            }

            return queryset4
            # return A_Product.objects.filter(price__icontains=query)
            # return A_Product.objects.filter(memory__icontains=query)

        return Product.objects.featured()
        #return A_Product.objects.filter(title__icontains="samsung")


    # def pproduct_view(request):
    #
    #     current_average = []
    #     current_review_count = []
    #     predicted_products = []
    #     predicted_products_result = []
    #
    #     qs = Product.objects.all()
    #
    #     queryset = Product.objects.all().values('title','price','Average_Rating','Review_count')
    #     # print(queryset)
    #     for avg in queryset:
    #         current_average.append(float(avg['Average_Rating']))
    #         current_review_count.append(float(avg['Review_count']))
    #
    #     print(current_average)
    #     average_result = sum(current_average)/len(current_average)
    #     print(average_result)
    #
    #     minimum_criteria = np.quantile(current_review_count, 0.7)
    #     print(minimum_criteria)
    #
    #     for avr,rc in zip(current_average,current_review_count):
    #         print(avr,"  ",rc)
    #         predicted_products = (rc / (rc + minimum_criteria) * avr) + (minimum_criteria / (minimum_criteria + rc) * average_result)
    #         print(avr," ",rc," ",predicted_products)
    #         predicted_products_result.append(predicted_products)
    #
    #
    #     print(predicted_products)
    #
    #
    #
    #     # Product.Populrity_Score.append('predicted_products')
    #
    #     queryset = Product.objects.all()
    #
    #     # print(len(queryset))
    #     for value, p in enumerate(queryset):
    #         obj = Product.objects.get(id=p.id)
    #         obj.Populrity_Score=predicted_products_result[value]
    #         obj.save()
    #
    #     # print(queryset)
    #
    #     # obj = Product('Populrity_Score')
    #
    #     queryset1 = Product.objects.order_by('-Populrity_Score')
    #     print(queryset1)
    #
    #
    #     # for current_average,current_review_count in list_data:
    #
    #     # print(result)
    #
    #
    #
    #     # queryset1 = np.mean(Product.Average_Rating)
    #     #
    #     # queryset2 = Product.objects.values('Review_count').quantile(0.90)
    #     # print (queryset2)
    #
    #
    #
    #     # for p in qs:
    #     #
    #     #
    #     # df = read_frame(qs)
    #     # df1 = df.head()
    #
    #     context = {
    #
    #         "object_list": queryset1
    #     }
    #
    #     return render(request, "product/list.html", context)