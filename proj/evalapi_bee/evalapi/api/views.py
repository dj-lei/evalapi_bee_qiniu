from rest_framework.views import APIView  # NOQA F401
from khas_core.rest.viewsets import ModelViewSet  # NOQA F401
from rest_framework.response import Response

from evalapi import serializers


class EvaluationView(ModelViewSet):
    rest_actions = ('list', )
    serializer_class = serializers.EvalSerialzier

    def list(self, request, *args, **kwargs):
        ser = self.get_serializer(data=self.request.query_params)
        ser.is_valid(raise_exception=True)

        return Response(data=ser.data['result'])


class PriceTrendView(EvaluationView):
    rest_actions = ('list', )
    serializer_class = serializers.EvalPriceTrend


class FuturePriceTrendView(EvaluationView):
    rest_actions = ('list', )
    serializer_class = serializers.EvalFuturePrice


class ResidualPriceTrendView(EvaluationView):
    rest_actions = ('list', )
    serializer_class = serializers.EvalResidualPrice
