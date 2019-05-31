from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from deal_records import serializers


class FakeDealRecordView(GenericAPIView):
    serializer_class = serializers.DealHistorySerializer

    def get(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.query_params)
        ser.is_valid(raise_exception=True)

        return Response(ser.data)



