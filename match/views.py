from rest_framework import generics
from rest_framework.response import Response

from .models import Match, MatchData
from .serializers import MatchSerializer, MatchDataSerializer

class MatchListView(generics.ListAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    # Optional: Add filtering logic
    def get_queryset(self):
        queryset = Match.objects.all()

        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        # Add custom metadata to the response
        response.data = {
            "status": "success",
            "total_matches": len(response.data),
            "matches": response.data
        }
        return Response(response.data)

class MatchDataListView(generics.ListAPIView):

    serializer_class = MatchDataSerializer

    # Optional: Add filtering logic
    def get_queryset(self):
        # Get optional filtering parameter from URL query (e.g., ?char=some_value)
        char = self.request.query_params.get('char', None)
        print("checing chat", char)
        # Filter MatchData by 'match_id' field, using 'char' if provided
        queryset = MatchData.objects.filter(match_id=char)
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        # Add custom metadata to the JSON response
        response.data = {
            "status": "success",
            "total_match_data": len(response.data),
            "match_data": response.data
        }
        return Response(response.data)
