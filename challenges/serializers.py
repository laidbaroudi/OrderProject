from rest_framework import serializers

from .models import Challenge, Entry


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ["id", "player_name", "game"]
        read_only_fields = ["id"]


class ChallengeSerializer(serializers.ModelSerializer):
    entries = EntrySerializer(many=True, read_only=True)

    class Meta:
        model = Challenge
        fields = [
            "id", "product", "description", "status", "entry_fee",
            "winner_name", "created_at", "entries",
        ]
        read_only_fields = ["id", "created_at", "winner_name"]
