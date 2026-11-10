import json

from django.db import IntegrityError
from django.http import JsonResponse

from api.models import Cliente
from api.serializers import cliente_to_dict


def lista_clientes(request):
    if request.method == "GET":
        dados = [cliente_to_dict(cliente) for cliente in Cliente.objects.all()]
        return JsonResponse(dados, safe=False)

    if request.method != "POST":
        return JsonResponse({"error": "Método não permitido"}, status=405)

    try:
        dados = json.loads(request.body)
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "JSON inválido"}, status=400)

    if not isinstance(dados, dict):
        return JsonResponse({"error": "JSON inválido"}, status=400)

    nome = str(dados.get("nome", "")).strip()
    cpf = str(dados.get("cpf", "")).strip()

    if not nome or not cpf:
        return JsonResponse(
            {"error": "nome e cpf são obrigatórios"},
            status=400,
        )

    if Cliente.objects.filter(cpf=cpf).exists():
        return JsonResponse({"error": "CPF já cadastrado"}, status=409)

    try:
        cliente = Cliente.objects.create(
            nome=nome,
            cpf=cpf,
            telefone=dados.get("telefone") or None,
            email=dados.get("email") or None,
        )
    except IntegrityError:
        return JsonResponse({"error": "CPF já cadastrado"}, status=409)

    return JsonResponse(cliente_to_dict(cliente), status=201)


def detalhe_cliente(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
    except Cliente.DoesNotExist:
        return JsonResponse({"error": "Cliente não encontrado"}, status=404)

    if request.method == "GET":
        return JsonResponse(cliente_to_dict(cliente))

    if request.method == "DELETE":
        cliente.delete()
        return JsonResponse({"message": "Cliente excluído com sucesso"})

    if request.method != "PUT":
        return JsonResponse({"error": "Método não permitido"}, status=405)

    try:
        dados = json.loads(request.body)
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"error": "JSON inválido"}, status=400)

    if not isinstance(dados, dict):
        return JsonResponse({"error": "JSON inválido"}, status=400)

    nome = str(dados.get("nome", cliente.nome)).strip()
    cpf = str(dados.get("cpf", cliente.cpf)).strip()

    if not nome or not cpf:
        return JsonResponse(
            {"error": "nome e cpf são obrigatórios"},
            status=400,
        )

    cpf_duplicado = Cliente.objects.filter(cpf=cpf).exclude(id=id).exists()
    if cpf_duplicado:
        return JsonResponse({"error": "CPF já cadastrado"}, status=409)

    cliente.nome = nome
    cliente.cpf = cpf
    cliente.telefone = dados.get("telefone", cliente.telefone) or None
    cliente.email = dados.get("email", cliente.email) or None

    try:
        cliente.save()
    except IntegrityError:
        return JsonResponse({"error": "CPF já cadastrado"}, status=409)

    return JsonResponse(cliente_to_dict(cliente))
