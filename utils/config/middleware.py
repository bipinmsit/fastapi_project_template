import time
from utils.config.logger import logger
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# Set up a dedicated logger for the middleware
# middleware_logger = logging.getLogger("timing_middleware")
# middleware_logger.setLevel(logging.INFO)


class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()  # Record the start time
        response = await call_next(request)  # Process the request
        process_time = time.time() - start_time  # Calculate the time taken
        # Log the time taken for the request
        logger.info(
            f"Request: {request.method} {request.url.path} - Time taken: {process_time:.4f} sec"
        )

        # Optionally add the time taken to the response headers
        response.headers["X-Process-Time"] = str(process_time)
        return response
