from django.urls import path
from .views  import PurchaseOrderAcknowledgmentView, VendorPerformanceView, homepage
from .views import VendorListCreateView,VendorRetrieveUpdateDeleteView
from .viewsPO import PurchaseOrderListCreateView,PurchaseOrderRetrieveUpdateDeleteView
urlpatterns = [
    path('home/',homepage,name="homepage"),    
    path('vendors/',VendorListCreateView.as_view(),name='list_vendors'),
    path('vendors/<int:pk>/',VendorRetrieveUpdateDeleteView.as_view(),name="vendor_detail"),
    path('purchaseorder/',PurchaseOrderListCreateView.as_view(),name='purchase_order_vendors'),
    path('purchaseorder/<int:pk>/',PurchaseOrderRetrieveUpdateDeleteView.as_view(),name="purchase_order_detail")  ,  
    path('purchaseorder/<int:pk>/acknowledge/', PurchaseOrderAcknowledgmentView.as_view(), name='purchase-order-acknowledge'),
    path('vendors/<int:pk>/performance/', VendorPerformanceView.as_view(), name='vendor-performance'),

]