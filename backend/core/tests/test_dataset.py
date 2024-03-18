from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from core.models import Dataset
from core.serializers import DatasetSerializer
from login.models import OsmUser


class DatasetTestViews(TestCase):
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
