from rest_framework.test import APITestCase, APIRequestFactory
from vms.views import VendorListCreateView,VendorRetrieveUpdateDeleteView
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from vms.models import Vendor, PurchaseOrder


User = get_user_model()
def test_homepage_returns_hello_world_message(self):
    # Make a GET request to the homepage
    response = self.client.get(reverse("homepage"))

    # Assert that the response status code is 200 OK
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Assert that the response data contains the expected message
    expected_data = {"message": "Hello, world"}
    self.assertDictEqual(response.data, expected_data)

class HelloWorldTestCase(APITestCase):
    def test_hello_world(self):
        response = self.client.get(reverse("homepage"))

        self.assertEqual(response.status_code, 200, "Expected response status code to be 200")
        self.assertEqual(response.json()["message"], "Hello, world", "Expected response message to be 'Hello, world'")


class VendorListTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("list_vendors")

        self.authenticate()
        
        self.vendor_data = {
                            "name":"vendor 3 name",
                            "contact_details":"vendor 3 contact_details",
                            "address":"vendor 3 address",
                            "vendor_code":"vendor 3 vendor_code22211"	
                        }
        self.vendor_create()

        # self.purchase_order = PurchaseOrder.objects.create(po_number='PO123', vendor=Vendor.objects.get(pk=1))

    def authenticate(self):

        resp=self.client.post(
            reverse("signup"),
            {
                "email": "user@app.com",
                "password": "passwordforuser##!123",
                "username": "ordinaryuser",
            },
        )

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        response = self.client.post(
            reverse("token_obtain_pair"),
            {
                "email": "user@app.com",
                "password": "passwordforuser##!123",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.data)
        token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def vendor_create(self):
        # sample_data = 
        response = self.client.post(reverse("list_vendors"), self.vendor_data, format="json") # sample_data)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.list_vendors()
        # self.assertEqual(response.data["title"], sample_data["title"])
        
    def test_1_vendor_retrieve(self):

        response = self.client.get(reverse("vendor_detail",kwargs={"pk":1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "vendor 3 name")

    def test_2_vendor_update(self):
        url1=reverse("vendor_detail",kwargs={"pk":1})
        response = self.client.put(url1,{
                        "name": "string11",
                        "contact_details": "string22",
                        "address": "string33",
                        "vendor_code": "string44",
                        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "string11")
    def test_3_list_vendors(self):
        


        response = self.client.get(reverse("list_vendors"),kwargs={"page_size":3})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_4_vendor_get(self):

        response = self.client.get(reverse("vendor_detail",kwargs={"pk":1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)



    def test_6_create_po(self):

        self.po_data1 = {
            "po_number": "PO001",
            "vendor": 1,
            "order_date": "2023-12-09T12:00:00Z",
            "delivery_date": "2023-12-10T12:00:00Z",
            "items": '{"item": "Test Item"}',
            "quantity": "10",
            "status": "completed",
            "issue_date": "2023-12-09T12:00:00Z",
        }  
        response = self.client.post(reverse("purchase_order_vendors"), data=self.po_data1, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url1=reverse("purchase_order_detail",kwargs={"pk":1})
        # print(" in test_6_get_po url1=", url1)
        response = self.client.get(url1, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.get_po()
        self.update_po()
        self.vendor_data = {
                            "name":"vendor 3 name 1",
                            "contact_details":"vendor 3 contact_details 1",
                            "address":"vendor 3 address 1",
                            "vendor_code":"vendor 3 vendor_code22211 1"	
                        }
        self.vendor_create()                
        self.purchase_order_acknowledge_view()
        self.vendor_performance_view()

    
    def get_po(self):

        self.po_data1 = {
            "po_number": "PO001",
            "vendor": 1,
            "order_date": "2023-12-09T12:00:00Z",
            "delivery_date": "2023-12-10T12:00:00Z",
            "items": '{"item": "Test Item"}',
            "quantity": "10",
            "status": "completed",
            "issue_date": "2023-12-09T12:00:00Z",
        }
        url1=reverse("purchase_order_detail",kwargs={"pk":1})
        response = self.client.get(url1, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def update_po(self):

        self.po_data1 = {
            "po_number": "PO001",
            "vendor": 1,
            "order_date": "2023-12-09T12:00:00Z",
            "delivery_date": "2023-12-10T12:00:00Z",
            "items": '{"item": "Test Item"}',
            "quantity": "10",
            "status": "completed",
            "issue_date": "2023-12-09T12:00:00Z",
        }
        url1=reverse("purchase_order_detail",kwargs={"pk":1})
        # print(" in test_6_update_po url1=", url1)
        response = self.client.put(url1, data=self.po_data1, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def purchase_order_acknowledge_view(self):
        url = reverse('purchase-order-acknowledge', kwargs={'pk': 1})
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)    

    def vendor_performance_view(self):
        url = reverse('vendor-performance', kwargs={'pk': 1})
        print(" in vendor_performance_view url=", url)
        response = self.client.get(url)
        print(" in vendor_performance_view response=", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)    

        
    # def test_7_purchase_order_acknowledge_view(self):
    #     url = reverse('purchase-order-acknowledge', kwargs={'pk': 1})
    #     print ( " in test_7_purchase_order_acknowledge_view url=", url)
    #     response = self.client.put(url)
    #     print ( " in test_7_purchase_order_acknowledge_view response=", response.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)            
    def test_100_vendor_delete(self):

        response = self.client.delete(reverse("vendor_detail",kwargs={"pk":1}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # print(" in vendor_delete response=", response.data)
        # self.assertEqual(response.data["results"], [])

    def tearDown(self):
        pass

