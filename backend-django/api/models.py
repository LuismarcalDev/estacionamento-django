from django.db import models


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'clientes'


class Veiculo(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='veiculos'
    )
    placa = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    cor = models.CharField(max_length=50)

    class Meta:
        db_table = 'veiculos'


class Vaga(models.Model):
    TIPO_CARRO = 'CARRO'
    TIPO_MOTO = 'MOTO'

    TIPO_CHOICES = [
        (TIPO_CARRO, 'Carro'),
        (TIPO_MOTO, 'Moto'),
    ]

    STATUS_LIVRE = 'LIVRE'
    STATUS_OCUPADA = 'OCUPADA'

    STATUS_CHOICES = [
        (STATUS_LIVRE, 'Livre'),
        (STATUS_OCUPADA, 'Ocupada'),
    ]

    numero = models.CharField(max_length=20, unique=True)
    tipo = models.CharField(
        max_length=10,
        choices=TIPO_CHOICES
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_LIVRE
    )

    class Meta:
        db_table = 'vagas'


class Permanencia(models.Model):
    STATUS_ABERTO = 'ABERTO'
    STATUS_FINALIZADO = 'FINALIZADO'

    STATUS_CHOICES = [
        (STATUS_ABERTO, 'Aberto'),
        (STATUS_FINALIZADO, 'Finalizado'),
    ]

    veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.CASCADE,
        related_name='permanencias'
    )
    vaga = models.ForeignKey(
        Vaga,
        on_delete=models.CASCADE,
        related_name='permanencias'
    )
    data_hora_entrada = models.DateTimeField()
    data_hora_saida = models.DateTimeField(blank=True, null=True)
    valor_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_ABERTO
    )

    class Meta:
        db_table = 'permanencias'
