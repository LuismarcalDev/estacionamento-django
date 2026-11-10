from django.http import HttpResponse, JsonResponse

from api.openapi import OPENAPI_SCHEMA


SWAGGER_HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Sistema de Estacionamento API</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui.css">
  <style>
    body { margin: 0; background: #fafafa; }
    .swagger-ui .topbar { display: none; }
  </style>
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui-bundle.js" crossorigin></script>
  <script>
    window.onload = () => {
      window.ui = SwaggerUIBundle({
        url: '/api/schema',
        dom_id: '#swagger-ui',
        deepLinking: true,
        displayRequestDuration: true,
        filter: true,
        persistAuthorization: true,
        presets: [SwaggerUIBundle.presets.apis],
        layout: 'BaseLayout'
      });
    };
  </script>
</body>
</html>
"""


def openapi_schema(request):
    if request.method != "GET":
        return JsonResponse({"error": "Método não permitido"}, status=405)

    return JsonResponse(
        OPENAPI_SCHEMA,
        json_dumps_params={"ensure_ascii": False},
    )


def swagger_ui(request):
    if request.method != "GET":
        return JsonResponse({"error": "Método não permitido"}, status=405)

    return HttpResponse(SWAGGER_HTML, content_type="text/html; charset=utf-8")
