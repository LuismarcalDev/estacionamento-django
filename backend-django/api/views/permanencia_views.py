import json

from django.http import JsonResponse

from api.models import Permanencia
from api.serializers import permanencia_to_dict
from api.services.permanencia_service import registrar_entrada, registrar_saida


def entrada(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método não permitido"}, status=405)

    try:
        dados = json.loads(request.body)
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "JSON inválido"}, status=400)

    if not isinstance(dados, dict):
        return JsonResponse({"error": "JSON inválido"}, status=400)

    veiculo_id = dados.get("veiculoId")
    vaga_id = dados.get("vagaId")

    if not veiculo_id or not vaga_id:
        return JsonResponse(
            {"error": "veiculoId e vagaId são obrigatórios"},
            status=400,
        )

    try:
        permanencia = registrar_entrada(veiculo_id, vaga_id)
    except ValueError as erro:
        return JsonResponse(
            {"error": str(erro)},
            status=_status_do_erro(erro),
        )

    return JsonResponse(permanencia_to_dict(permanencia), status=201)


def saida(request, id):
    if request.method != "PUT":
        return JsonResponse({"error": "Método não permitido"}, status=405)

    try:
        permanencia = registrar_saida(id)
    except ValueError as erro:
        return JsonResponse(
            {"error": str(erro)},
            status=_status_do_erro(erro),
        )

    return JsonResponse(permanencia_to_dict(permanencia))


def lista_permanencias(request):
    if request.method != "GET":
        return JsonResponse({"error": "Método não permitido"}, status=405)

    permanencias = Permanencia.objects.select_related("veiculo", "vaga").all()
    status = request.GET.get("status")
    if status:
        permanencias = permanencias.filter(status=status.upper())

    dados = [
        permanencia_to_dict(permanencia)
        for permanencia in permanencias
    ]
    return JsonResponse(dados, safe=False)


def _status_do_erro(erro):
    if "não encontrad" in str(erro).lower():
        return 404
    return 409
