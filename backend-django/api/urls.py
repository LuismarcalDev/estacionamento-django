from django.urls import re_path

from api.views import cliente_views
from api.views import dashboard_views
from api.views import docs_views
from api.views import permanencia_views
from api.views import vaga_views
from api.views import veiculo_views


urlpatterns = [
    re_path(r"^docs/?$", docs_views.swagger_ui),
    re_path(r"^schema/?$", docs_views.openapi_schema),
    re_path(r"^clientes/?$", cliente_views.lista_clientes),
    re_path(r"^clientes/(?P<id>\d+)/?$", cliente_views.detalhe_cliente),
    re_path(r"^veiculos/?$", veiculo_views.lista_veiculos),
    re_path(r"^veiculos/(?P<id>\d+)/?$", veiculo_views.detalhe_veiculo),
    re_path(r"^vagas/?$", vaga_views.lista_vagas),
    re_path(r"^vagas/(?P<id>\d+)/?$", vaga_views.detalhe_vaga),
    re_path(r"^permanencias/entrada/?$", permanencia_views.entrada),
    re_path(
        r"^permanencias/(?P<id>\d+)/saida/?$",
        permanencia_views.saida,
    ),
    re_path(r"^permanencias/?$", permanencia_views.lista_permanencias),
    re_path(r"^dashboard/?$", dashboard_views.dashboard),
]
