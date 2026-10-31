import random

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Challenge, Entry
from .serializers import ChallengeSerializer, EntrySerializer


class ChallengeViewSet(viewsets.ModelViewSet):
    serializer_class = ChallengeSerializer
    queryset = Challenge.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["post"])
    def join(self, request, pk=None):
        challenge = self.get_object()
        serializer = EntrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(challenge=challenge)
        return Response(ChallengeSerializer(challenge).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def start(self, request, pk=None):
        challenge = self.get_object()
        challenge.status = Challenge.Status.LIVE
        challenge.save(update_fields=["status"])
        return Response(ChallengeSerializer(challenge).data)

    @action(detail=True, methods=["post"])
    def declare(self, request, pk=None):
        challenge = self.get_object()
        winner = request.data.get("winner_name", "").strip()
        if not winner:
            return Response({"detail": "winner_name is required."}, status=status.HTTP_400_BAD_REQUEST)
        challenge.winner_name = winner
        challenge.status = Challenge.Status.DONE
        challenge.save(update_fields=["winner_name", "status"])
        return Response(ChallengeSerializer(challenge).data)

    @action(detail=True, methods=["post"])
    def auto_winner(self, request, pk=None):
        challenge = self.get_object()
        entries = list(challenge.entries.all())
        if not entries:
            return Response({"detail": "No entries yet."}, status=status.HTTP_400_BAD_REQUEST)
        winner = random.choice(entries)
        challenge.winner_name = winner.player_name
        challenge.status = Challenge.Status.DONE
        challenge.save(update_fields=["winner_name", "status"])
        return Response(ChallengeSerializer(challenge).data)
