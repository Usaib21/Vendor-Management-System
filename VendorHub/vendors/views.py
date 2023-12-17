from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import *
from .serializers import VendorSerializer, PurchaseOrderSerializer, VendorPerformanceSerializer
from rest_framework.response import Response
from django.db.models import Avg, Count, F
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework import status

#1. Vendor Profile Management:

class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


#2. Purchase Order Tracking:

class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    
#3. Vendor Performance Evaluation:    
      
class VendorPerformanceView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorPerformanceSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        try:
             # Logic for On-Time Delivery Rate
            completed_pos = PurchaseOrder.objects.filter(vendor=instance, status='completed')
            total_completed_pos = completed_pos.count()

            if total_completed_pos > 0:
                on_time_deliveries = completed_pos.filter(delivery_date__lte=timezone.now()).count()
                on_time_delivery_rate = (on_time_deliveries / total_completed_pos) * 100
            else:
                on_time_delivery_rate = 0.0 

            # Logic for Quality Rating Average
            quality_ratings = completed_pos.exclude(quality_rating__isnull=True)
            quality_rating_avg = quality_ratings.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0

            # Logic for Average Response Time
            acknowledged_pos = completed_pos.exclude(acknowledgment_date__isnull=True)

            # Print acknowledgment dates for debugging
            acknowledgment_dates = list(acknowledged_pos.values_list('acknowledgment_date', flat=True))
            print(f"Acknowledgment Dates: {acknowledgment_dates}")

            response_times = acknowledged_pos.annotate(
                response_time=timezone.now() - F('acknowledgment_date')
            ).values_list('response_time', flat=True)

            # Print response times for debugging
            print(f"Response Times: {response_times}")

            avg_response_time_seconds = (
                sum(response_time.total_seconds() for response_time in response_times) /
                len(response_times)
            ) if response_times else 0

            # Logic for Fulfilment Rate
            successful_pos = completed_pos.filter(quality_rating__isnull=False)
            fulfilment_rate = (successful_pos.count() / total_completed_pos) * 100 if total_completed_pos > 0 else 0

            # Update or create HistoricalPerformance entry
            HistoricalPerformance.objects.update_or_create(
                vendor=instance,
                date=timezone.now(),
                defaults={
                    'on_time_delivery_rate': on_time_delivery_rate,
                    'quality_rating_avg': quality_rating_avg,
                    'average_response_time': avg_response_time_seconds,
                    'fulfillment_rate': fulfilment_rate,
                }
            )

            # Print debug messages
            print(f"On-Time Delivery Rate: {on_time_delivery_rate}%")
            print(f"Quality Rating Average: {quality_rating_avg}")
            print(f"Average Response Time: {avg_response_time_seconds}")
            print(f"Fulfilment Rate: {fulfilment_rate}%")

            # Return the calculated metrics
            return Response({
                'on_time_delivery_rate': on_time_delivery_rate,
                'quality_rating_avg': quality_rating_avg,
                'average_response_time': avg_response_time_seconds,
                'fulfillment_rate': fulfilment_rate,
            })
        except Exception as e:
            print(f"Error: {e}")
            raise
        
        
@api_view(['GET'])
def vendor_performance(request, vendor_id):
    try:
        # Get the vendor instance
        vendor = Vendor.objects.get(pk=vendor_id)

        # Logic for On-Time Delivery Rate
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        total_completed_pos = completed_pos.count()

        if total_completed_pos > 0:
            on_time_deliveries = completed_pos.filter(delivery_date__lte=timezone.now()).count()
            on_time_delivery_rate = (on_time_deliveries / total_completed_pos) * 100
        else:
            on_time_delivery_rate = 0.0  # I set rate to 0% when there are no completed orders

        # Logic for Quality Rating Average
        quality_ratings = completed_pos.exclude(quality_rating__isnull=True)
        quality_rating_avg = quality_ratings.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0

        # Logic for Average Response Time
        acknowledged_pos = completed_pos.exclude(acknowledgment_date__isnull=True)
        response_times = acknowledged_pos.annotate(
            response_time=timezone.now() - F('acknowledgment_date')
        ).values_list('response_time', flat=True)

        avg_response_time_seconds = (
            sum(response_time.total_seconds() for response_time in response_times) /
            len(response_times)
        ) if response_times else 0

        # Logic for Fulfillment Rate
        successful_pos = completed_pos.filter(quality_rating__isnull=False)
        fulfilment_rate = (successful_pos.count() / total_completed_pos) * 100 if total_completed_pos > 0 else 0

        # Update or create HistoricalPerformance entry
        HistoricalPerformance.objects.update_or_create(
            vendor=vendor,
            date=timezone.now(),
            defaults={
                'on_time_delivery_rate': on_time_delivery_rate,
                'quality_rating_avg': quality_rating_avg,
                'average_response_time': avg_response_time_seconds,
                'fulfillment_rate': fulfilment_rate,
            }
        )

        # Return the calculated metrics
        return Response({
            'on_time_delivery_rate': on_time_delivery_rate,
            'quality_rating_avg': quality_rating_avg,
            'average_response_time': avg_response_time_seconds,
            'fulfillment_rate': fulfilment_rate,
        })
    except Vendor.DoesNotExist:
        return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def acknowledge_purchase_order(request, po_id):
    try:
        # Get the purchase order instance
        purchase_order = PurchaseOrder.objects.get(pk=po_id)

        # Update acknowledgment_date
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()

        # Return success response
        return Response({'message': 'Purchase Order acknowledged successfully'})
    except PurchaseOrder.DoesNotExist:
        return Response({'error': 'Purchase Order not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)