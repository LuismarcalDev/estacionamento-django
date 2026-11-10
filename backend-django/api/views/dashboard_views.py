from django.http import JsonResponse

from api.models import Permanencia, Vaga


def dashboard(request):
    if request.method != "GET":
        return JsonResponse({"error": "Método não permitido"}, status=405)

    return JsonResponse(
        {
            "totalVagas": Vaga.objects.count(),
            "vagasLivres": Vaga.objects.filter(
                status=Vaga.STATUS_LIVRE
            ).count(),
            "vagasOcupadas": Vaga.objects.filter(
                status=Vaga.STATUS_OCUPADA
            ).count(),
            "veiculosEstacionados": Permanencia.objects.filter(
                status=Permanencia.STATUS_ABERTO
            ).count(),
        }
    )
