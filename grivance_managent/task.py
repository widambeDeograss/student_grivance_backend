from background_task import background


@background(schedule=60)  # Run every 60 seconds, adjust as needed
def run_grievance_workflow():
    from django.urls import reverse
    from django.test.client import RequestFactory
    from rest_framework.test import APIClient

    # Use a client to simulate a request
    client = APIClient()
    response = client.get(reverse('grievance-workflow'))
    print(response.json())  # Log response or handle accordingly
