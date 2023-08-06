from ozonparser.models import Product
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from ozonparser.serializers import ProductSerializer
from ozonparser.tasks import process
from django.http import HttpResponse
from ozonparser.models import Product

class ProductListAPIView(generics.ListAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
class ProductRetrieveAPIView(generics.RetrieveAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

class ParseProductsAPIView(APIView):
    http_method_names = ['get','post']
    def get(self,request):
        usernames = [[_product.name,_product.price,_product.description,_product.image_url,_product.discount] for _product in Product.objects.all()]
        return Response(usernames)
    def post(self, request, format=None):
        products_count = request.data
        products_count = min(products_count, 50)  # Limit maximum count to 50

        # Perform the parsing task using the specified products_count
        process.apply_async(args =(products_count,))
        return Response({"message": f"Parsing task started.products_count = {products_count} "})

def url(request,id):
    getid = Product.objects.filter(id = id).last()
    return  HttpResponse('<meta http-equiv="refresh" content="0; url=https://www.ozon.ru' + getid.url +'">' )