from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import generics, mixins, status
from rest_framework.decorators import api_view,APIView
from .models import PurchaseOrder, Vendor
from .serializers import PurchaseOrderSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .views import CustomPaginator

# Create your views here.



class PurchaseOrderRetrieveUpdateDeleteView(generics.GenericAPIView,mixins.RetrieveModelMixin,mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    """
    a view class for retreiving, updating and deleting vendor data.
    """    
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    pk = None
    # def get_object(self):
    #     print(" in get object pk ",self.pk)
    #     po= get_object_or_404(self.queryset, pk=self.pk)
    #     print(" in get object po ",po)
    #     return po
    # def get_object(self, pk):
    #     return get_object_or_404(self.queryset, pk=pk)    


    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.kwargs['pk'])


    def put(self, request, pk, *args, **kwargs):
        """
        api for updating Purchase Order data.
        """                

        instance = self.get_object()
        vendor_id = request.data.get('vendor')
        
        # Using get_object_or_404 to get the vendor instance
        vendor_instance = get_object_or_404(Vendor, pk=vendor_id)
        
        # Update the 'vendor' field in the request data
        request.data['vendor'] = vendor_instance

        # Use serializer update method directly
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # If you want to return a response, you can do so
        return Response(serializer.data, status=status.HTTP_200_OK)


    def get(self, request, pk, *args, **kwargs):
        """
        api for retreiving Purchase Order data.
        """        
        # return self.retrieve(request, id=pk)
        # self.pk = pk
        return self.retrieve(request, pk=pk, *args, **kwargs)


    def delete(self, request, pk, *args, **kwargs):
        """
        api for deleting Purchase Order data.
        """                
        self.pk = pk
        return self.destroy(request, id=pk)
# class VendorListCreateView(APIView):
class PurchaseOrderListCreateView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):    
    """
    a view class for creating and listing vendors
    """

    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    pagination_class = CustomPaginator
    def get(self, request: Request, *args, **kwargs):
        """
        api for listing Purchase Order
        """        
        return self.list(request, *args, **kwargs)

    # def post(self, request: Request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        api for creating PurchaseOrder
        """        
        return self.create(request, *args, **kwargs)        
        # serializer = PurchaseOrderSerializer(data=request.data)
        # # self.get_serializer(data=request.data)


        # if  serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.validated_data, status=status.HTTP_201_CREATED)   


        # return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    # def perform_create(self, serializer):
    #     # print(" in perform create of purchase order serializer",serializer)
    #     # print(" in perform create of purchase order serializer validated_data",serializer.validated_data)
    #     # validated_data = serializer.validated_data

    #     # # Update the 'vendor' key if needed
    #     # vendor_id = validated_data['vendor']
    #     # print("  in perform create of purchase order serializer vendor_id",vendor_id)
    #     # # validated_data['vendor'] = Vendor.objects.get(id=vendor_id)
    #     # # serializer.save()
    #     # print("  in perform create of purchase order serializer validated_data",serializer.validated_data)
    #     return super().perform_create(serializer)            