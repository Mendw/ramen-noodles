from rest_framework import serializers

from daily_notes.models import (
    Day,
    Goal
)

class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = '__all__'

class GoalSerializer(serializers.ModelSerializer):
    year  = serializers.IntegerField(required=False)
    month = serializers.IntegerField(required=False)

    class Meta:
        model = Goal
        fields = '__all__'