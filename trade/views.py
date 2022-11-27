from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Simulation

from .serializers import SimulationSerializer


@api_view(['GET'])
def simulation(request):
    """
    Simulation method

    This method generates simulation data in a json format

    Parameters
    ----------
    arg1 :
        request

    Returns
    -------
    JsonResponse

    """

    sim_obj = Simulation()
    sim_obj.account_size = float(request.GET['size'])
    sim_obj.total_trades = int(request.GET['total'])
    sim_obj.risk_per_trade = float(request.GET['risk'])
    sim_obj.win_rate = float(request.GET['winrate'])
    sim_obj.risk_reward = float(request.GET['riskreward'])

    serializer = SimulationSerializer(sim_obj)

    return Response(serializer.data)
