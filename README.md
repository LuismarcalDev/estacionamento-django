# Sistema de Estacionamento

Sistema web com backend em Django, banco SQLite e frontend em HTML, CSS e JavaScript servido pelo Nginx.

## Executar com Docker

```bash
docker compose up --build -d
```

Serviços disponíveis

| Serviço | Endereço |
|---|---|
| Frontend | http://localhost:3000 |
| Backend | http://localhost:8080 |
| Swagger UI | http://localhost:3000/api/docs |
| OpenAPI JSON | http://localhost:3000/api/schema |

O backend executa as migrations automaticamente ao iniciar. O banco fica no volume `sqlite_data` e permanece disponível apó reinicializações.

Para acompanhar os logs

```bash
docker compose logs -f backend
```

Para encerrar os serviços

```bash
docker compose down
```

## Executar o backend localmente

Use Python 3.11 ou superior.

```bash
cd backend-django
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8080
```

Para executar os testes

```bash
python manage.py test
```

## Estrutura

```text
.
├── backend-django
│   ├── api
│   ├── estacionamento
│   ├── Dockerfile
│   ├── manage.py
│   └── requirements.txt
├── frontend
├── docker-compose.yml
└── README.md
```

## Endpoints

| Método | Endpoint |
|---|---|
| GET, POST | `/api/clientes` |
| GET, PUT, DELETE | `/api/clientes/{id}` |
| GET, POST | `/api/veiculos` |
| GET, PUT, DELETE | `/api/veiculos/{id}` |
| GET, POST | `/api/vagas` |
| GET, PUT, DELETE | `/api/vagas/{id}` |
| POST | `/api/permanencias/entrada` |
| PUT | `/api/permanencias/{id}/saida` |
| GET | `/api/permanencias` |
| GET | `/api/dashboard` |

As rotas aceitam URLs com ou sem barra final. Os endpoints de listagem de vagas e permanências aceitam o filtro `status` na query string.

## Documentação interativa

O Swagger UI permite consultar e executar os endpoints pelo navegador:

```text
http://localhost:3000/api/docs
```

A especificação OpenAPI 3 pode ser consultada diretamente em:

```text
http://localhost:3000/api/schema
```
