from django.http import HttpResponse


class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "OPTIONS":
            response = HttpResponse(status=204)
            self._adicionar_cors(response)
            return response

        response = self.get_response(request)
        self._adicionar_cors(response)

        return response

    def _adicionar_cors(self, response):
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = (
            "GET, POST, PUT, DELETE, OPTIONS"
        )
        response["Access-Control-Allow-Headers"] = "Content-Type"
