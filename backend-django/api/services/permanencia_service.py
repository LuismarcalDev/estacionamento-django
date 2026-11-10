import math
from datetime import datetime
from decimal import Decimal

from django.db import transaction

from ..models import Permanencia, Veiculo, Vaga


@transaction.atomic
def registrar_entrada(veiculo_id, vaga_id):
    try:
        veiculo = Veiculo.objects.get(id=veiculo_id)
    except (Veiculo.DoesNotExist, ValueError, TypeError):
        raise ValueError("Veículo não encontrado")

    permanencia_aberta = Permanencia.objects.filter(
        veiculo=veiculo,
        status=Permanencia.STATUS_ABERTO
    ).exists()

    if permanencia_aberta:
        raise ValueError(
            "Veículo já possui uma permanência aberta"
        )

    try:
        vaga = Vaga.objects.get(id=vaga_id)
    except (Vaga.DoesNotExist, ValueError, TypeError):
        raise ValueError("Vaga não encontrada")

    if vaga.status != Vaga.STATUS_LIVRE:
        raise ValueError("Vaga já está ocupada")

    vaga.status = Vaga.STATUS_OCUPADA
    vaga.save()

    permanencia = Permanencia.objects.create(
        veiculo=veiculo,
        vaga=vaga,
        data_hora_entrada=datetime.now(),
        data_hora_saida=None,
        valor_total=None,
        status=Permanencia.STATUS_ABERTO,
    )

    return permanencia


@transaction.atomic
def registrar_saida(permanencia_id):
    try:
        permanencia = Permanencia.objects.get(id=permanencia_id)
    except (Permanencia.DoesNotExist, ValueError, TypeError):
        raise ValueError("Permanência não encontrada")

    if permanencia.status != Permanencia.STATUS_ABERTO:
        raise ValueError("Permanência já está finalizada")

    data_saida = datetime.now()

    valor = _calcular_valor(
        permanencia.data_hora_entrada,
        data_saida
    )

    permanencia.data_hora_saida = data_saida
    permanencia.valor_total = valor
    permanencia.status = Permanencia.STATUS_FINALIZADO
    permanencia.save()

    vaga = permanencia.vaga
    vaga.status = Vaga.STATUS_LIVRE
    vaga.save()

    return permanencia


def _calcular_valor(entrada, saida):
    diferenca = saida - entrada

    minutos = diferenca.total_seconds() / 60

    horas = math.ceil(minutos / 60)

    if horas < 1:
        horas = 1

    tarifa = Decimal("5.00")

    return Decimal(horas) * tarifa
