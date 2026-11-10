import json
from datetime import datetime, timedelta

from django.test import Client, TestCase

from api.models import Permanencia, Vaga


class ApiIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)

    def enviar_json(self, metodo, caminho, dados=None):
        return getattr(self.client, metodo)(
            caminho,
            data=json.dumps(dados or {}),
            content_type="application/json",
        )

    def criar_cliente(self, cpf="123.456.789-00"):
        resposta = self.enviar_json(
            "post",
            "/api/clientes",
            {
                "nome": "Maria Silva",
                "cpf": cpf,
                "telefone": "11999999999",
                "email": "maria@example.com",
            },
        )
        self.assertEqual(resposta.status_code, 201)
        return resposta.json()

    def criar_veiculo(self, cliente_id, placa="ABC-1234"):
        resposta = self.enviar_json(
            "post",
            "/api/veiculos",
            {
                "placa": placa,
                "marca": "Toyota",
                "modelo": "Corolla",
                "cor": "Branco",
                "clienteId": cliente_id,
            },
        )
        self.assertEqual(resposta.status_code, 201)
        return resposta.json()

    def criar_vaga(self, numero="A01"):
        resposta = self.enviar_json(
            "post",
            "/api/vagas",
            {"numero": numero, "tipo": "CARRO"},
        )
        self.assertEqual(resposta.status_code, 201)
        return resposta.json()

    def test_fluxo_completo_compativel_com_frontend(self):
        cliente = self.criar_cliente()
        veiculo = self.criar_veiculo(cliente["id"])
        vaga = self.criar_vaga()

        entrada = self.enviar_json(
            "post",
            "/api/permanencias/entrada",
            {"veiculoId": veiculo["id"], "vagaId": vaga["id"]},
        )
        self.assertEqual(entrada.status_code, 201)
        self.assertEqual(entrada.json()["status"], "ABERTO")
        self.assertIn("dataHoraEntrada", entrada.json())

        conflito = self.enviar_json(
            "post",
            "/api/permanencias/entrada",
            {"veiculoId": veiculo["id"], "vagaId": vaga["id"]},
        )
        self.assertEqual(conflito.status_code, 409)

        permanencia = Permanencia.objects.get(id=entrada.json()["id"])
        permanencia.data_hora_entrada = datetime.now() - timedelta(minutes=61)
        permanencia.save(update_fields=["data_hora_entrada"])

        saida = self.enviar_json(
            "put",
            f"/api/permanencias/{permanencia.id}/saida",
        )
        self.assertEqual(saida.status_code, 200)
        self.assertEqual(saida.json()["status"], "FINALIZADO")
        self.assertEqual(saida.json()["valorTotal"], "10.00")

        vaga_atualizada = Vaga.objects.get(id=vaga["id"])
        self.assertEqual(vaga_atualizada.status, Vaga.STATUS_LIVRE)

        abertas = self.client.get("/api/permanencias?status=ABERTO")
        finalizadas = self.client.get("/api/permanencias?status=FINALIZADO")
        self.assertEqual(abertas.json(), [])
        self.assertEqual(len(finalizadas.json()), 1)

        dashboard = self.client.get("/api/dashboard").json()
        self.assertEqual(
            set(dashboard),
            {
                "totalVagas",
                "vagasLivres",
                "vagasOcupadas",
                "veiculosEstacionados",
            },
        )
        self.assertEqual(dashboard["vagasLivres"], 1)
        self.assertEqual(dashboard["veiculosEstacionados"], 0)

    def test_conflitos_de_campos_unicos_retornam_409(self):
        cliente = self.criar_cliente()

        cpf_duplicado = self.enviar_json(
            "post",
            "/api/clientes",
            {"nome": "Outra Pessoa", "cpf": "123.456.789-00"},
        )
        self.assertEqual(cpf_duplicado.status_code, 409)

        self.criar_veiculo(cliente["id"])
        placa_duplicada = self.enviar_json(
            "post",
            "/api/veiculos",
            {
                "placa": "ABC-1234",
                "marca": "Honda",
                "modelo": "Civic",
                "cor": "Preto",
                "clienteId": cliente["id"],
            },
        )
        self.assertEqual(placa_duplicada.status_code, 409)

        self.criar_vaga()
        vaga_duplicada = self.enviar_json(
            "post",
            "/api/vagas",
            {"numero": "A01", "tipo": "MOTO"},
        )
        self.assertEqual(vaga_duplicada.status_code, 409)

    def test_validacoes_e_rotas_com_barra_final(self):
        cliente_invalido = self.enviar_json(
            "post",
            "/api/clientes/",
            {"nome": "", "cpf": ""},
        )
        self.assertEqual(cliente_invalido.status_code, 400)

        vaga_invalida = self.enviar_json(
            "post",
            "/api/vagas/",
            {"numero": "A01", "tipo": "CAMINHAO"},
        )
        self.assertEqual(vaga_invalida.status_code, 400)

        self.assertEqual(self.client.get("/api/clientes/").status_code, 200)
        self.assertEqual(self.client.get("/api/clientes").status_code, 200)
        self.assertEqual(self.client.get("/api/clientes/999").status_code, 404)

    def test_filtro_de_vagas(self):
        self.criar_vaga("A01")
        self.criar_vaga("A02")
        Vaga.objects.filter(numero="A02").update(status=Vaga.STATUS_OCUPADA)

        livres = self.client.get("/api/vagas?status=LIVRE").json()
        ocupadas = self.client.get("/api/vagas?status=OCUPADA").json()

        self.assertEqual([vaga["numero"] for vaga in livres], ["A01"])
        self.assertEqual([vaga["numero"] for vaga in ocupadas], ["A02"])

    def test_documentacao_openapi_e_swagger(self):
        schema = self.client.get("/api/schema")
        self.assertEqual(schema.status_code, 200)
        self.assertEqual(schema.json()["openapi"], "3.0.3")
        self.assertIn("/api/clientes", schema.json()["paths"])
        self.assertIn("/api/permanencias/{id}/saida", schema.json()["paths"])

        swagger = self.client.get("/api/docs")
        self.assertEqual(swagger.status_code, 200)
        self.assertContains(swagger, "SwaggerUIBundle")
        self.assertContains(swagger, "url: '/api/schema'")
