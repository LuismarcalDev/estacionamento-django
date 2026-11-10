OPENAPI_SCHEMA = {
    "openapi": "3.0.3",
    "info": {
        "title": "Sistema de Estacionamento API",
        "version": "1.0.0",
        "description": (
            "API REST do sistema de estacionamento desenvolvida com Django. "
            "As rotas aceitam URLs com ou sem barra final."
        ),
    },
    "servers": [
        {
            "url": "/",
            "description": "Servidor atual",
        }
    ],
    "tags": [
        {"name": "Dashboard"},
        {"name": "Clientes"},
        {"name": "Veículos"},
        {"name": "Vagas"},
        {"name": "Permanências"},
    ],
    "paths": {
        "/api/dashboard": {
            "get": {
                "tags": ["Dashboard"],
                "summary": "Consultar indicadores do estacionamento",
                "responses": {
                    "200": {
                        "description": "Indicadores atuais",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Dashboard"
                                }
                            }
                        },
                    }
                },
            }
        },
        "/api/clientes": {
            "get": {
                "tags": ["Clientes"],
                "summary": "Listar clientes",
                "responses": {
                    "200": {
                        "description": "Lista de clientes",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/components/schemas/Cliente"
                                    },
                                }
                            }
                        },
                    }
                },
            },
            "post": {
                "tags": ["Clientes"],
                "summary": "Cadastrar cliente",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/ClienteInput"
                            }
                        }
                    },
                },
                "responses": {
                    "201": {
                        "description": "Cliente cadastrado",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Cliente"
                                }
                            }
                        },
                    },
                    "400": {"$ref": "#/components/responses/ErroValidacao"},
                    "409": {"$ref": "#/components/responses/Conflito"},
                },
            },
        },
        "/api/clientes/{id}": {
            "parameters": [{"$ref": "#/components/parameters/Id"}],
            "get": {
                "tags": ["Clientes"],
                "summary": "Consultar cliente",
                "responses": {
                    "200": {
                        "description": "Cliente encontrado",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Cliente"
                                }
                            }
                        },
                    },
                    "404": {"$ref": "#/components/responses/NaoEncontrado"},
                },
            },
            "put": {
                "tags": ["Clientes"],
                "summary": "Atualizar cliente",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/ClienteUpdate"
                            }
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": "Cliente atualizado",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Cliente"
                                }
                            }
                        },
                    },
                    "400": {"$ref": "#/components/responses/ErroValidacao"},
                    "404": {"$ref": "#/components/responses/NaoEncontrado"},
                    "409": {"$ref": "#/components/responses/Conflito"},
                },
            },
            "delete": {
                "tags": ["Clientes"],
                "summary": "Excluir cliente",
                "responses": {
                    "200": {"$ref": "#/components/responses/Sucesso"},
                    "404": {"$ref": "#/components/responses/NaoEncontrado"},
                },
            },
        },
        "/api/veiculos": {
            "get": {
                "tags": ["Veículos"],
                "summary": "Listar veículos",
                "responses": {
                    "200": {
                        "description": "Lista de veículos",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/components/schemas/Veiculo"
                                    },
                                }
                            }
                        },
                    }
                },
            },
            "post": {
                "tags": ["Veículos"],
                "summary": "Cadastrar veículo",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/VeiculoInput"
                            }
                        }
                    },
                },
                "responses": {
                    "201": {
                        "description": "Veículo cadastrado",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Veiculo"
                                }
                            }
                        },
                    },
                    "400": {"$ref": "#/components/responses/ErroValidacao"},
                    "404": {"$ref": "#/components/responses/NaoEncontrado"},
                    "409": {"$ref": "#/components/responses/Conflito"},
                },
            },
        },
        "/api/veiculos/{id}": {
            "parameters": [{"$ref": "#/components/parameters/Id"}],
            "get": {
                "tags": ["Veículos"],
                "summary": "Consultar veículo",
                "responses": {
                    "200": {
                        "description": "Veículo encontrado",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Veiculo"
                                }
                            }
                        },
                    },
                    "404": {"$ref": "#/components/responses/NaoEncontrado"},
                },
            },
            "put": {
                "tags": ["Veículos"],
                "summary": "Atualizar veículo",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/VeiculoUpdate"
                            }
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": "Veículo atualizado",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Veiculo"
                                }
                            }
                        },
                    },
                    "400": {"$ref": "#/components/responses/ErroValidacao"},
                    "404": {"$ref": "#/components/responses/NaoEncontrado"},
                    "409": {"$ref": "#/components/responses/Conflito"},
                },
            },
            "delete": {
                "tags": ["Veículos"],
                "summary": "Excluir veículo",
                "responses": {
                    "200": {"$ref": "#/components/responses/Sucesso"},
                    "404": {"$ref": "#/components/responses/NaoEncontrado"},
                },
            },
        },
        "/api/vagas": {
            "get": {
                "tags": ["Vagas"],
                "summary": "Listar vagas",
                "parameters": [
                    {
                        "name": "status",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "enum": ["LIVRE", "OCUPADA"],
                        },
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Lista de vagas",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/components/schemas/Vaga"
                                    },
                                }
                            }
                        },
                    }
                },
            },
            "post": {
                "tags": ["Vagas"],
                "summary": "Cadastrar vaga",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/VagaInput"
                            }
                        }
                    },
                },
                "responses": {
                    "201": {
                        "description": "Vaga cadastrada",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Vaga"}
                            }
                        },
                    },
                    "400": {"$ref": "#/components/responses/ErroValidacao"},
                    "409": {"$ref": "#/components/responses/Conflito"},
                },
            },
        },
        "/api/vagas/{id}": {
            "parameters": [{"$ref": "#/components/parameters/Id"}],
            "get": {
                "tags": ["Vagas"],
                "summary": "Consultar vaga",
                "responses": {
                    "200": {
                        "description": "Vaga encontrada",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Vaga"}
                            }
                        },
                    },
                    "404": {"$ref": "#/components/responses/NaoEncontrado"},
                },
            },
            "put": {
                "tags": ["Vagas"],
                "summary": "Atualizar vaga",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/VagaUpdate"
                            }
                        }
                    },
                },
                "responses": {
                    "200": {
                        "description": "Vaga atualizada",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Vaga"}
                            }
                        },
                    },
                    "400": {"$ref": "#/components/responses/ErroValidacao"},
                    "404": {"$ref": "#/components/responses/NaoEncontrado"},
                    "409": {"$ref": "#/components/responses/Conflito"},
                },
            },
            "delete": {
                "tags": ["Vagas"],
                "summary": "Excluir vaga",
                "responses": {
                    "200": {"$ref": "#/components/responses/Sucesso"},
                    "404": {"$ref": "#/components/responses/NaoEncontrado"},
                },
            },
        },
        "/api/permanencias": {
            "get": {
                "tags": ["Permanências"],
                "summary": "Listar permanências",
                "parameters": [
                    {
                        "name": "status",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "enum": ["ABERTO", "FINALIZADO"],
                        },
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Lista de permanências",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/components/schemas/Permanencia"
                                    },
                                }
                            }
                        },
                    }
                },
            }
        },
        "/api/permanencias/entrada": {
            "post": {
                "tags": ["Permanências"],
                "summary": "Registrar entrada de veículo",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/EntradaInput"
                            }
                        }
                    },
                },
                "responses": {
                    "201": {
                        "description": "Entrada registrada",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Permanencia"
                                }
                            }
                        },
                    },
                    "400": {"$ref": "#/components/responses/ErroValidacao"},
                    "404": {"$ref": "#/components/responses/NaoEncontrado"},
                    "409": {"$ref": "#/components/responses/Conflito"},
                },
            }
        },
        "/api/permanencias/{id}/saida": {
            "parameters": [{"$ref": "#/components/parameters/Id"}],
            "put": {
                "tags": ["Permanências"],
                "summary": "Registrar saída e calcular valor",
                "responses": {
                    "200": {
                        "description": "Saída registrada",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Permanencia"
                                }
                            }
                        },
                    },
                    "404": {"$ref": "#/components/responses/NaoEncontrado"},
                    "409": {"$ref": "#/components/responses/Conflito"},
                },
            },
        },
    },
    "components": {
        "parameters": {
            "Id": {
                "name": "id",
                "in": "path",
                "required": True,
                "description": "Identificador numérico do recurso",
                "schema": {"type": "integer", "minimum": 1},
            }
        },
        "responses": {
            "ErroValidacao": {
                "description": "Dados inválidos",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/Erro"}
                    }
                },
            },
            "NaoEncontrado": {
                "description": "Recurso não encontrado",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/Erro"}
                    }
                },
            },
            "Conflito": {
                "description": "Conflito com o estado atual ou valor duplicado",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/Erro"}
                    }
                },
            },
            "Sucesso": {
                "description": "Operação concluída",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/Mensagem"}
                    }
                },
            },
        },
        "schemas": {
            "Cliente": {
                "type": "object",
                "required": ["id", "nome", "cpf"],
                "properties": {
                    "id": {"type": "integer", "example": 1},
                    "nome": {"type": "string", "example": "Ana Souza"},
                    "cpf": {"type": "string", "example": "123.456.789-00"},
                    "telefone": {
                        "type": "string",
                        "nullable": True,
                        "example": "(11) 99999-9999",
                    },
                    "email": {
                        "type": "string",
                        "nullable": True,
                        "example": "ana@email.com",
                    },
                },
            },
            "ClienteInput": {
                "type": "object",
                "required": ["nome", "cpf"],
                "properties": {
                    "nome": {"type": "string", "example": "Ana Souza"},
                    "cpf": {"type": "string", "example": "123.456.789-00"},
                    "telefone": {"type": "string", "nullable": True},
                    "email": {"type": "string", "nullable": True},
                },
            },
            "ClienteUpdate": {
                "type": "object",
                "properties": {
                    "nome": {"type": "string"},
                    "cpf": {"type": "string"},
                    "telefone": {"type": "string", "nullable": True},
                    "email": {"type": "string", "nullable": True},
                },
            },
            "Veiculo": {
                "type": "object",
                "required": [
                    "id",
                    "clienteId",
                    "clienteNome",
                    "placa",
                    "marca",
                    "modelo",
                    "cor",
                ],
                "properties": {
                    "id": {"type": "integer", "example": 1},
                    "clienteId": {"type": "integer", "example": 1},
                    "clienteNome": {"type": "string", "example": "Ana Souza"},
                    "placa": {"type": "string", "example": "ABC-1234"},
                    "marca": {"type": "string", "example": "Toyota"},
                    "modelo": {"type": "string", "example": "Corolla"},
                    "cor": {"type": "string", "example": "Branco"},
                },
            },
            "VeiculoInput": {
                "type": "object",
                "required": ["placa", "marca", "modelo", "cor", "clienteId"],
                "properties": {
                    "placa": {"type": "string", "example": "ABC-1234"},
                    "marca": {"type": "string", "example": "Toyota"},
                    "modelo": {"type": "string", "example": "Corolla"},
                    "cor": {"type": "string", "example": "Branco"},
                    "clienteId": {"type": "integer", "example": 1},
                },
            },
            "VeiculoUpdate": {
                "type": "object",
                "properties": {
                    "placa": {"type": "string"},
                    "marca": {"type": "string"},
                    "modelo": {"type": "string"},
                    "cor": {"type": "string"},
                    "clienteId": {"type": "integer"},
                },
            },
            "Vaga": {
                "type": "object",
                "required": ["id", "numero", "tipo", "status"],
                "properties": {
                    "id": {"type": "integer", "example": 1},
                    "numero": {"type": "string", "example": "A01"},
                    "tipo": {
                        "type": "string",
                        "enum": ["CARRO", "MOTO"],
                    },
                    "status": {
                        "type": "string",
                        "enum": ["LIVRE", "OCUPADA"],
                    },
                },
            },
            "VagaInput": {
                "type": "object",
                "required": ["numero", "tipo"],
                "properties": {
                    "numero": {"type": "string", "example": "A01"},
                    "tipo": {
                        "type": "string",
                        "enum": ["CARRO", "MOTO"],
                    },
                    "status": {
                        "type": "string",
                        "enum": ["LIVRE", "OCUPADA"],
                        "default": "LIVRE",
                    },
                },
            },
            "VagaUpdate": {
                "type": "object",
                "properties": {
                    "numero": {"type": "string"},
                    "tipo": {
                        "type": "string",
                        "enum": ["CARRO", "MOTO"],
                    },
                    "status": {
                        "type": "string",
                        "enum": ["LIVRE", "OCUPADA"],
                    },
                },
            },
            "EntradaInput": {
                "type": "object",
                "required": ["veiculoId", "vagaId"],
                "properties": {
                    "veiculoId": {"type": "integer", "example": 1},
                    "vagaId": {"type": "integer", "example": 1},
                },
            },
            "Permanencia": {
                "type": "object",
                "required": [
                    "id",
                    "veiculoId",
                    "veiculoPlaca",
                    "veiculoModelo",
                    "vagaId",
                    "vagaNumero",
                    "dataHoraEntrada",
                    "status",
                ],
                "properties": {
                    "id": {"type": "integer", "example": 1},
                    "veiculoId": {"type": "integer", "example": 1},
                    "veiculoPlaca": {"type": "string", "example": "ABC-1234"},
                    "veiculoModelo": {"type": "string", "example": "Corolla"},
                    "vagaId": {"type": "integer", "example": 1},
                    "vagaNumero": {"type": "string", "example": "A01"},
                    "dataHoraEntrada": {
                        "type": "string",
                        "format": "date-time",
                    },
                    "dataHoraSaida": {
                        "type": "string",
                        "format": "date-time",
                        "nullable": True,
                    },
                    "valorTotal": {
                        "type": "string",
                        "nullable": True,
                        "example": "5.00",
                    },
                    "status": {
                        "type": "string",
                        "enum": ["ABERTO", "FINALIZADO"],
                    },
                },
            },
            "Dashboard": {
                "type": "object",
                "required": [
                    "totalVagas",
                    "vagasLivres",
                    "vagasOcupadas",
                    "veiculosEstacionados",
                ],
                "properties": {
                    "totalVagas": {"type": "integer", "example": 10},
                    "vagasLivres": {"type": "integer", "example": 7},
                    "vagasOcupadas": {"type": "integer", "example": 3},
                    "veiculosEstacionados": {"type": "integer", "example": 3},
                },
            },
            "Erro": {
                "type": "object",
                "required": ["error"],
                "properties": {
                    "error": {
                        "type": "string",
                        "example": "Recurso não encontrado",
                    }
                },
            },
            "Mensagem": {
                "type": "object",
                "required": ["message"],
                "properties": {
                    "message": {
                        "type": "string",
                        "example": "Operação concluída com sucesso",
                    }
                },
            },
        },
    },
}
