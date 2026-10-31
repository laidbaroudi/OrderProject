from rest_framework import serializers

from .models import AISetting, ShopSetting, TeamMember


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ["id", "name", "role"]


class AISettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AISetting
        fields = [
            "id", "mode", "auto_call", "call_from", "call_until",
            "retries", "voice", "opening_line", "shop_notes", "release_limit",
        ]


class ShopSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopSetting
        fields = ["id", "shop_name", "currency", "phone"]
