import json

from django.db import IntegrityError
from django.http import JsonResponse

from api.models import Cliente, Veiculo
from api.serializers import veiculo_to_dict


def lista_veiculos(request):
    if request.method == "GET":
        veiculos = Veiculo.objects.select_related("cliente").all()
        dados = [veiculo_to_dict(veiculo) for veiculo in veiculos]
        return JsonResponse(dados, safe=False)

    if request.method != "POST":
        return JsonResponse({"error": "Método não permitido"}, status=405)

    try:
        dados = json.loads(request.body)
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "JSON inválido"}, status=400)

    if not isinstance(dados, dict):
        return JsonResponse({"error": "JSON inválido"}, status=400)

    placa = str(dados.get("placa", "")).strip().upper()
    marca = str(dados.get("marca", "")).strip()
    modelo = str(dados.get("modelo", "")).strip()
    cor = str(dados.get("cor", "")).strip()
    cliente_id = dados.get("clienteId")

    if not all([placa, marca, modelo, cor, cliente_id]):
        return JsonResponse(
            {
                "error": (
                    "placa, marca, modelo, cor e clienteId "
                    "são obrigatórios"
                )
            },
            status=400,
        )

    try:
        cliente = Cliente.objects.get(id=cliente_id)
    except (Cliente.DoesNotExist, ValueError, TypeError):
        return JsonResponse({"error": "Cliente não encontrado"}, status=404)

    if Veiculo.objects.filter(placa=placa).exists():
        return JsonResponse({"error": "Placa já cadastrada"}, status=409)

    try:
        veiculo = Veiculo.objects.create(
            cliente=cliente,
            placa=placa,
            marca=marca,
            modelo=modelo,
            cor=cor,
        )
    except IntegrityError:
        return JsonResponse({"error": "Placa já cadastrada"}, status=409)

    return JsonResponse(veiculo_to_dict(veiculo), status=201)


def detalhe_veiculo(request, id):
    try:
        veiculo = Veiculo.objects.select_related("cliente").get(id=id)
    except Veiculo.DoesNotExist:
        return JsonResponse({"error": "Veículo não encontrado"}, status=404)

    if request.method == "GET":
        return JsonResponse(veiculo_to_dict(veiculo))

    if request.method == "DELETE":
        veiculo.delete()
        return JsonResponse({"message": "Veículo excluído com sucesso"})

    if request.method != "PUT":
        return JsonResponse({"error": "Método não permitido"}, status=405)

    try:
        dados = json.loads(request.body)
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "JSON inválido"}, status=400)

    if not isinstance(dados, dict):
        return JsonResponse({"error": "JSON inválido"}, status=400)

    placa = str(dados.get("placa", veiculo.placa)).strip().upper()
    marca = str(dados.get("marca", veiculo.marca)).strip()
    modelo = str(dados.get("modelo", veiculo.modelo)).strip()
    cor = str(dados.get("cor", veiculo.cor)).strip()

    if not all([placa, marca, modelo, cor]):
        return JsonResponse(
            {"error": "placa, marca, modelo e cor são obrigatórios"},
            status=400,
        )

    if "clienteId" in dados:
        try:
            veiculo.cliente = Cliente.objects.get(id=dados["clienteId"])
        except (Cliente.DoesNotExist, ValueError, TypeError):
            return JsonResponse({"error": "Cliente não encontrado"}, status=404)

    placa_duplicada = Veiculo.objects.filter(placa=placa).exclude(id=id).exists()
    if placa_duplicada:
        return JsonResponse({"error": "Placa já cadastrada"}, status=409)

    veiculo.placa = placa
    veiculo.marca = marca
    veiculo.modelo = modelo
    veiculo.cor = cor

    try:
        veiculo.save()
    except IntegrityError:
        return JsonResponse({"error": "Placa já cadastrada"}, status=409)

    return JsonResponse(veiculo_to_dict(veiculo))
