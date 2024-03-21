import os

from django.test import TestCase
from rest_framework.test import APILiveServerTestCase, RequestsClient, APIClient
from rest_framework import status
from django.urls import reverse
from core.models import (
    Dataset,
    Training,
    Feedback,
    FeedbackAOI,
    FeedbackLabel,
    Model,
)
from core.serializers import (
    FeedbackSerializer,
    FeedbackAOISerializer,
    FeedbackLabelSerializer,
)
from login.models import OsmUser

API_BASE = "http://testserver/api/v1"

# Set the custom headers
headersList = {
    "accept": "application/json",
    "access-token": os.environ.get("TESTING_TOKEN"),
}


class TestFeedbackListView(TestCase):
    def setUp(self):
        # Initialize test data
        self.client = APIClient()
        self.osm_user = OsmUser.objects.create(osm_id="111", username="UserOne")
        self.dataset = Dataset.objects.create(
            name="Dataset one", created_by=self.osm_user, status=0
        )
        self.model = Model.objects.create(
            name="Model one", dataset=self.dataset, created_by=self.osm_user, status=0
        )
        self.training = Training.objects.create(
            model=self.model,
            zoom_level=[19, 20, 21, 22],
            epochs=10,
            batch_size=32,
            created_by=self.osm_user,
        )
        self.feedback_aoi = FeedbackAOI.objects.create(
            training=self.training,
            geom="POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))",
            user=self.osm_user,
            source_imagery="https://www.testurl.com",
        )
        self.feedback_label = FeedbackLabel.objects.create(
            feedback_aoi=self.feedback_aoi, geom="POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))"
        )
        self.feedback = Feedback.objects.create(
            training=self.training,
            zoom_level=20,
            feedback_type="TP",
            geom="POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))",
            user=self.osm_user,
            source_imagery="https://www.testurl.com",
        )
        self.feedback_label = FeedbackLabel.objects.create(
            feedback_aoi=self.feedback_aoi, geom="POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))"
        )

    def test_feedback_view(self):
        # Test feedback list view
        url = reverse("feedback-list")
        response = self.client.get(url)
        feedback = Feedback.objects.all()
        serializer = FeedbackSerializer(feedback, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_feedback_label_view(self):
        # Test feedback label list view
        url = reverse("feedbacklabel-list")
        response = self.client.get(url)
        feedback_labels = FeedbackLabel.objects.all()
        serializer = FeedbackLabelSerializer(feedback_labels, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_feedback_aoi_view(self):
        # Test feedback AOI list view
        url = reverse("feedbackaoi-list")
        response = self.client.get(url)
        feedback_aois = FeedbackAOI.objects.all()
        serializer = FeedbackAOISerializer(feedback_aois, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestFeedbackCreateView(APILiveServerTestCase):
    def setUp(self):
        # Initialize test data
        self.client = RequestsClient()
        self.osm_user = OsmUser.objects.create(osm_id="111", username="UserOne")
        self.dataset = Dataset.objects.create(
            name="Dataset one", created_by=self.osm_user, status=0
        )
        self.model = Model.objects.create(
            name="Model one", dataset=self.dataset, created_by=self.osm_user, status=0
        )
        self.training = Training.objects.create(
            model=self.model,
            zoom_level=[19, 20, 21, 22],
            epochs=10,
            batch_size=32,
            created_by=self.osm_user,
        )
        self.feedback = Feedback.objects.create(
            training=self.training,
            zoom_level=20,
            feedback_type="TP",
            geom="POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))",
            user=self.osm_user,
            source_imagery="https://www.testurl.com",
        )

    def test_feedback_create_view(self):
        # test that feedback creation works if authenticated and authorized
        user = self.osm_user.osm_id
        training = self.training.id
        data = {
            "training": training,
            "geom": "POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))",
            "zoom_level": 20,
            "feedback_type": "TP",
            "user": user,
            "source_imagery": "https://www.testurl.com",
        }
        response = self.client.post(f"{API_BASE}/feedback/", data, headers=headersList)
        self.assertEqual(Feedback.objects.count(), 2)

    def test_feedback_auth_required(self):
        # Test that permission is required to create feedback
        user = self.osm_user.osm_id
        training = self.training.id
        data = {
            "training": training,
            "geom": "POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))",
            "zoom_level": 20,
            "feedback_type": "TP",
            "user": user,
            "source_imagery": "https://www.testurl.com",
        }
        response = self.client.post(f"{API_BASE}/feedback/", data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_feedback_aoi_create_view(self):
        # test that feedback AOI creation works if authenticated and authorized
        user = self.osm_user.osm_id
        training = self.training.id
        data = {
            "training": training,
            "geom": "POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))",
            "user": user,
            "source_imagery": "https://www.testurl.com",
        }
        response = self.client.post(f"{API_BASE}/feedback-aoi/", data, headers=headersList)
        self.assertEqual(FeedbackAOI.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_feedback_aoi_auth_require(self):
        # test that feedback AOI creation does not work if authenticated and authorized
        user = self.osm_user.osm_id
        training = self.training.id
        data = {
            "training": training,
            "geom": "POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))",
            "user": user,
            "source_imagery": "https://www.testurl.com",
        }
        response = self.client.post(f"{API_BASE}/feedback-aoi/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


