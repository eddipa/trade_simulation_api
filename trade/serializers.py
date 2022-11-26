from rest_framework import serializers

from .models import Simulation


class SimulationSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField(read_only=True)
    img = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Simulation
        fields = [
            'data',
            'img'
        ]

    def get_data(self, obj):
        return obj.simulate()

    def get_img(self, obj):
        return obj.img()
