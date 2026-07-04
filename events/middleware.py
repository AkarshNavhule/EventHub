# events/middleware.py
import time
import logging

# Set up a standard Python logger
logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        # One-time configuration and initialization.
        # get_response is a callable provided by Django that passes the request to the next middleware or view.
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request BEFORE the view (and later middleware) are called.
        start_time = time.time()

        # The request is passed down the chain to the view, and a response is generated
        response = self.get_response(request)

        # Code to be executed for each request/response AFTER the view is called.
        duration = time.time() - start_time

        # Log the method (GET/POST), the path (/api/events/), the status code (200/201), and the duration
        logger.info(f"{request.method} {request.path} - {response.status_code} - {duration:.2f}s")

        return response