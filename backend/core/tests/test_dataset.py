import os

from django.test import TestCase
from rest_framework.test import APILiveServerTestCase, RequestsClient, APIClient
from rest_framework import status
from django.urls import reverse
from core.models import Dataset
from core.serializers import DatasetSerializer
from login.models import OsmUser
from login.models import OsmUser

API_BASE = "http://testserver/api/v1"

# Set the custom headers
headersList = {
    "accept": "application/json",
    "access-token": os.environ.get("TESTING_TOKEN"),
}


class DatasetListTestViews(TestCase):
    def setUp(self):
        # Initialize test data
        self.client = APIClient()
        self.osm_user = OsmUser.objects.create(osm_id="111", username="UserOne")
        self.dataset = Dataset.objects.create(
            name="Dataset one", created_by=self.osm_user, status=0
        )

    def test_dataset_list_view(self):
        """
        Test the dataset list view.
        """
        url = reverse("dataset-list")
        response = self.client.get(url)
        datasets = Dataset.objects.all()
        serializer = DatasetSerializer(datasets, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dataset_retrieve_view(self):
        """
        Test the dataset retrieve view.
        """
        dataset_id = self.dataset.id
        url = reverse("dataset-detail", args=[dataset_id])
        response = self.client.get(url)
        dataset = Dataset.objects.get(id=dataset_id)
        serializer = DatasetSerializer(dataset)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDatasetCreateView(APILiveServerTestCase):
    def setUp(self):
        # Initialize test data
        self.client = RequestsClient()
        self.osm_user = OsmUser.objects.create(osm_id="111", username="UserOne")
        self.dataset = Dataset.objects.create(
            name="Dataset one", created_by=self.osm_user, status=0
        )

    def test_dataset_create_view(self):
        # test that dataset works if authenticated and authorized
        user = self.osm_user.osm_id
        data = {
            "name": "Dataset two",
            "user": user,
        }
        response = self.client.post(f"{API_BASE}/dataset/", data, headers=headersList)
        self.assertEqual(Dataset.objects.count(), 2)

    def test_auth_required(self):
        # Test that permission is required to create dataset
        user = self.osm_user.osm_id
        data = {
            "name": "Dataset three",
            "user": user,
        }
        response = self.client.post(f"{API_BASE}/dataset/", data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
