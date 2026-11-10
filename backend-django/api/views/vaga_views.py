import json

from django.db import IntegrityError
from django.http import JsonResponse

from api.models import Vaga
from api.serializers import vaga_to_dict


TIPOS_VALIDOS = {Vaga.TIPO_CARRO, Vaga.TIPO_MOTO}
STATUS_VALIDOS = {Vaga.STATUS_LIVRE, Vaga.STATUS_OCUPADA}


def lista_vagas(request):
    if request.method == "GET":
        vagas = Vaga.objects.all()
        status = request.GET.get("status")
        if status:
            vagas = vagas.filter(status=status.upper())

        dados = [vaga_to_dict(vaga) for vaga in vagas]
        return JsonResponse(dados, safe=False)

    if request.method != "POST":
        return JsonResponse({"error": "Método não permitido"}, status=405)

    try:
        dados = json.loads(request.body)
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "JSON inválido"}, status=400)

    if not isinstance(dados, dict):
        return JsonResponse({"error": "JSON inválido"}, status=400)

    numero = str(dados.get("numero", "")).strip().upper()
    tipo = str(dados.get("tipo", "")).strip().upper()
    status = str(dados.get("status", Vaga.STATUS_LIVRE)).strip().upper()

    erro = _validar_vaga(numero, tipo, status)
    if erro:
        return JsonResponse({"error": erro}, status=400)

    if Vaga.objects.filter(numero=numero).exists():
        return JsonResponse({"error": "Número de vaga já cadastrado"}, status=409)

    try:
        vaga = Vaga.objects.create(numero=numero, tipo=tipo, status=status)
    except IntegrityError:
        return JsonResponse({"error": "Número de vaga já cadastrado"}, status=409)

    return JsonResponse(vaga_to_dict(vaga), status=201)


def detalhe_vaga(request, id):
    try:
        vaga = Vaga.objects.get(id=id)
    except Vaga.DoesNotExist:
        return JsonResponse({"error": "Vaga não encontrada"}, status=404)

    if request.method == "GET":
        return JsonResponse(vaga_to_dict(vaga))

    if request.method == "DELETE":
        vaga.delete()
        return JsonResponse({"message": "Vaga excluída com sucesso"})

    if request.method != "PUT":
        return JsonResponse({"error": "Método não permitido"}, status=405)

    try:
        dados = json.loads(request.body)
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "JSON inválido"}, status=400)

    if not isinstance(dados, dict):
        return JsonResponse({"error": "JSON inválido"}, status=400)

    numero = str(dados.get("numero", vaga.numero)).strip().upper()
    tipo = str(dados.get("tipo", vaga.tipo)).strip().upper()
    status = str(dados.get("status", vaga.status)).strip().upper()

    erro = _validar_vaga(numero, tipo, status)
    if erro:
        return JsonResponse({"error": erro}, status=400)

    numero_duplicado = Vaga.objects.filter(numero=numero).exclude(id=id).exists()
    if numero_duplicado:
        return JsonResponse({"error": "Número de vaga já cadastrado"}, status=409)

    vaga.numero = numero
    vaga.tipo = tipo
    vaga.status = status

    try:
        vaga.save()
    except IntegrityError:
        return JsonResponse({"error": "Número de vaga já cadastrado"}, status=409)

    return JsonResponse(vaga_to_dict(vaga))


def _validar_vaga(numero, tipo, status):
    if not numero or not tipo:
        return "numero e tipo são obrigatórios"
    if tipo not in TIPOS_VALIDOS:
        return "tipo deve ser CARRO ou MOTO"
    if status not in STATUS_VALIDOS:
        return "status deve ser LIVRE ou OCUPADA"
    return None
