from rest_framework import serializers
from .models import *


class SuggestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suggestions
        fields = '__all__'
        depth = 2


class DivisionGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = "__all__"
        depth = 2


class DivisionPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = [
            "name",
            "admin",
        ]


class SubDivisionGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubDivision
        fields = "__all__"
        depth = 2


class SubDivisionPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubDivision
        fields = [
            "name",
            "admin",
            "division",
        ]


class ProblemTypeGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemType
        fields = "__all__"
        depth = 2


class ProblemTypePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemType
        fields = [
            "type_name",
            "time_required",
            "responsible_division",
            "responsible_sub_divifany",
        ]


class SubmittedProblemsGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmittedProblems
        fields = "__all__"
        depth = 2


class SubmittedProblemsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmittedProblems
        fields = [
            "problem_type",
            "current_responsible_division",
            "current_responsible_sub_divifany",
            "submitted_problem",
            "user_submitted",
        ]


class TrackProblemGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackProblem
        fields = "__all__"
        depth = 2


class TrackProblemPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackProblem
        fields = [
            "problem",
            "current_responsible_division",
            "current_responsible_sub_divifany",
            "time_since_submission",
        ]


class ProblemEvidenceGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemEvidence
        fields = "__all__"
        depth = 2


class ProblemEvidencePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemEvidence
        fields = [
            "problem",
            "file_type",
            "evdc",
            "message"
        ]


class NotificationPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "division",
            "notification",
            "user",
            "sub_divifany",
        ]


class NotificationGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
        depth = 2