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
    account_size = request.GET['size']
    total_trades = request.GET['total']
    risk_per_trade = request.GET['risk']
    win_rate = request.GET['winrate']
    risk_reward = request.GET['riskreward']

    sim_obj = Simulation()
    sim_obj.account_size
    sim_obj.total_trades
    sim_obj.risk_per_trade
    sim_obj.win_rate
    sim_obj.risk_reward

    serializer = SimulationSerializer(sim_obj)

    #data = sim_obj.simulate()

    return Response(serializer.data)
