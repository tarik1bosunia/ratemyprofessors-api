import time
import logging

logger = logging.getLogger(__name__)


class LogRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the incoming request
        request_start_time = time.time()
        logger.info(f"Request: {request.method} {request.path}")

        # Process the request by passing it to the next middleware/view
        response = self.get_response(request)

        # Log the response details
        response_time = time.time() - request_start_time
        logger.info(f"Response: {response.status_code} {request.path} (Time: {response_time:.3f}s)")

        return response
