from django.forms import ValidationError
from django.shortcuts import render
# from pytz import timezone,datetime
from datetime import datetime
# import pytz
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import generics, mixins, status
from rest_framework.decorators import api_view,APIView,permission_classes
from .models import HistoricalPerformance, PurchaseOrder, Vendor
from .serializers import PurchaseOrderSerializer, VendorSerializer,HistoricalPerformanceSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import QueryDict


# Create your views here.
@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def homepage(request:Request):
    response= {"message":"Hello, world"}
    return Response(data=response,status=status.HTTP_200_OK)



class CustomPaginator(PageNumberPagination):
    page_size = 3
    page_query_param = "page"
    page_size_query_param = "page_size"

class VendorRetrieveUpdateDeleteView(generics.GenericAPIView,mixins.RetrieveModelMixin,mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    """
    a view class for retreiving, updating and deleting vendor data.
    """    
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()

    def get(self, request, pk, *args, **kwargs):
        """
        api for retreiving vendor data.
        """        
        return self.retrieve(request, id=pk)

    def put(self, request, pk, *args, **kwargs):
        """
        api for updating vendor data.
        """                

        return self.update(request, id=pk, *args, **kwargs)


    def delete(self, request, pk, *args, **kwargs):
        """
        api for deleting vendor data.
        """                
        return self.destroy(request, id=pk)



class VendorListCreateView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):    
    """
    a view class for creating and listing vendors
    """

    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Vendor.objects.all()
    pagination_class = CustomPaginator

    def perform_create(self, serializer):
        serializer.save()
        return super().perform_create(serializer)    
    def get(self, request: Request, *args, **kwargs):
        """
        api for listing vendors
        """        
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        api for creating vendors
        """        
        return self.create(request, *args, **kwargs)

class PurchaseOrderAcknowledgmentView(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin
    ):
    """
    API view for updating the acknowledgment status of a Purchase Order.
    """ 
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        # Assuming the URL parameter is named 'pk' for the Purchase Order primary key
        pk = self.kwargs.get('pk')
        return generics.get_object_or_404(PurchaseOrder, pk=pk)


    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, required=True, description="Purchase order ID"),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'vendor': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID of the vendor",
                ),
                'acknowledgment_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Acknowledgment date"),
            },
            required=['vendor',  'acknowledgment_date'],
        ),
        responses={
            200: PurchaseOrderSerializer,
            400: "Bad Request",
            404: "Not Found",
        },
        operation_description="Update the acknowledgment status of a Purchase Order.",
    )    
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.acknowledgment_date = request.data.get('acknowledgment_date')
        instance.save()
        return Response(self.get_serializer(instance).data, status=status.HTTP_200_OK)
class VendorPerformanceView(generics.RetrieveAPIView):
    # API endpoint for retrieving a vendor's performance metrics
    # Supports GET request
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, required=True, description="Vendor ID"),
        ],

        responses={
            200: HistoricalPerformanceSerializer,
            400: "Bad Request",
            404: "Not Found",
        },
        operation_description="retreive performance metrics  of a Vendor.",
    )  
    def get(self, request, pk, *args, **kwargs):
        """
        api for retreiving HistoricalPerformance data.
        """        
        # print(" Retreiving historical performance for vendor ",pk)
        return self.retrieve(request, id=pk)    
    def get_object(self):
        # Assuming the URL parameter is named 'pk' for the HistoricalPerformance primary key
        queryset_length = len(HistoricalPerformance.objects.all())
        if queryset_length == 0:
            return {}

        pk = self.kwargs.get('pk')
        return generics.get_object_or_404(HistoricalPerformance, pk=pk)
    