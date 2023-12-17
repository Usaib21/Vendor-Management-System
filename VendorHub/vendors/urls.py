# urls.py
from django.urls import path
# from .views import VendorListCreateView, VendorDetailView,PurchaseOrderListCreateView, PurchaseOrderDetailView
from .views import *
urlpatterns = [
    path('api/vendors/', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('api/vendors/<int:pk>/', VendorDetailView.as_view(), name='vendor-detail'),
    
    path('api/purchase_orders/', PurchaseOrderListCreateView.as_view(), name='purchaseorder-list-create'),
    path('api/purchase_orders/<int:pk>/', PurchaseOrderDetailView.as_view(), name='purchaseorder-detail'),
    
    path('api/vendors/<int:vendor_id>/performance/', vendor_performance, name='vendor-performance'),
    path('api/purchase_orders/<int:po_id>/acknowledge/', acknowledge_purchase_order, name='acknowledge-purchase-order'),
]
