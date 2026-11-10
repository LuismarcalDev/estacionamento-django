from .models import Cliente, Veiculo, Vaga, Permanencia


def cliente_to_dict(cliente):
    return {
        "id": cliente.id,
        "nome": cliente.nome,
        "cpf": cliente.cpf,
        "telefone": cliente.telefone,
        "email": cliente.email,
    }


def veiculo_to_dict(veiculo):
    return {
        "id": veiculo.id,
        "clienteId": veiculo.cliente_id,
        "clienteNome": veiculo.cliente.nome,
        "placa": veiculo.placa,
        "marca": veiculo.marca,
        "modelo": veiculo.modelo,
        "cor": veiculo.cor,
    }


def vaga_to_dict(vaga):
    return {
        "id": vaga.id,
        "numero": vaga.numero,
        "tipo": vaga.tipo,
        "status": vaga.status,
    }


def permanencia_to_dict(permanencia):
    return {
        "id": permanencia.id,
        "veiculoId": permanencia.veiculo_id,
        "veiculoPlaca": permanencia.veiculo.placa,
        "veiculoModelo": permanencia.veiculo.modelo,
        "vagaId": permanencia.vaga_id,
        "vagaNumero": permanencia.vaga.numero,
        "dataHoraEntrada": permanencia.data_hora_entrada,
        "dataHoraSaida": permanencia.data_hora_saida,
        "valorTotal": (
            str(permanencia.valor_total)
            if permanencia.valor_total is not None
            else None
        ),
        "status": permanencia.status,
    }
