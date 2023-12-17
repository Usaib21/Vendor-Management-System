
# VendorHub API

VendorHub is an API for managing vendors, purchase orders, and evaluating vendor performance.

## Setup Instructions

**Clone the Repository:**
   ```bash
   git clone <Vendor Management System>
   cd VendorHub
   VPS E:\Vendor Management System\VendorHub>

1.Create and Activate Virtual Environment:
    python -m venv venv
    source `venv\Scripts\activate`

2.Install Dependencies:
   pip install -r requirements.txt

3.Install Django Rest Framework:
   pip install djangorestframework

4.Create and Apply Migrations:
  python manage.py makemigrations
  python manage.py migrate

5.Create Superuser (Optional):
  python manage.py createsuperuser

6.Run Development Server:
  python manage.py runserver
The API will be accessible at http://localhost:8000/.

 **VendorHub API**


## API Endpoints:

1. Vendors
List/Create Vendors:
Endpoint: /api/vendors/
Method: GET (List), POST (Create)

Retrieve/Update/Delete Vendor:
Endpoint: /api/vendors/<vendor_id>/
Method: GET (Retrieve), PUT/PATCH (Update), DELETE (Delete)

2. Purchase Orders
List/Create Purchase Orders:
Endpoint: /api/purchase_orders/
Method: GET (List), POST (Create)

Retrieve/Update/Delete Purchase Order:
Endpoint: /api/purchase_orders/<po_id>/
Method: GET (Retrieve), PUT/PATCH (Update), DELETE (Delete)

Acknowledge Purchase Order:
Endpoint: /api/purchase_orders/<po_id>/acknowledge/
Method: POST

3. Vendor Performance
Retrieve Vendor Performance Metrics:
Endpoint: /api/vendors/<vendor_id>/performance/
Method: GET

**Documentation**

[Documentation](https://www.django-rest-framework.org/)

For detailed API documentation, visit API Documentation.


**Project Overview**

VendorHub provides the following functionalities:

Vendor Profile Management:
List and create vendors.
Retrieve, update, and delete vendor profiles.


Purchase Order Tracking:
List and create purchase orders.
Retrieve, update, and delete purchase orders.
Acknowledge purchase orders.

Vendor Performance Evaluation:
Retrieve metrics for a vendor's on-time delivery rate, quality rating average, average response time, and fulfillment rate.
Metrics are updated in real-time based on purchase order data modifications.
