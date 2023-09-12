import socket
import logging

request_logger = logging.getLogger(__name__)


class RequestLogMiddleware:
    """Middleware для логирования запросов к API."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        log_data = {
            "remote_address": request.META["REMOTE_ADDR"],
            "server_hostname": socket.gethostname(),
            "request_method": request.method,
            "request_path": request.get_full_path(),
        }

        response = self.get_response(request)

        request_logger.info(msg=log_data)

        return response

    def process_exception(self, request, exception):
        """Обрабатывает исключения и выполняет их запись в лог."""
        try:
            raise exception
        except Exception as e:
            request_logger.exception("Unhandled Exception: " + str(e))
        return exception
