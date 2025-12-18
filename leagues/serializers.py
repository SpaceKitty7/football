from rest_framework import serializers
from .models import League, NFLPlayer, FantasyTeam, Roster, Matchup
from accounts.serializers import UserSerializer


class NFLPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFLPlayer
        fields = '__all__'


class LeagueSerializer(serializers.ModelSerializer):
    commissioner = UserSerializer(read_only=True)
    current_team_count = serializers.ReadOnlyField()
    spots_available = serializers.ReadOnlyField()

    class Meta:
        model = League
        fields = [
            'id', 'name', 'commissioner', 'league_type', 'scoring_type',
            'max_teams', 'is_public', 'entry_fee', 'prize_pool',
            'draft_date', 'season_year', 'is_active',
            'current_team_count', 'spots_available', 'created_at'
        ]
        read_only_fields = ['id', 'commissioner', 'created_at']


class LeagueCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = [
            'name', 'league_type', 'scoring_type', 'max_teams',
            'is_public', 'entry_fee', 'prize_pool', 'draft_date', 'season_year'
        ]


class FantasyTeamSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    league = LeagueSerializer(read_only=True)

    class Meta:
        model = FantasyTeam
        fields = [
            'id', 'name', 'owner', 'league', 'wins', 'losses', 'ties',
            'points_for', 'points_against', 'created_at'
        ]
        read_only_fields = ['id', 'owner', 'league', 'wins', 'losses', 'ties', 'points_for', 'points_against', 'created_at']


class RosterSerializer(serializers.ModelSerializer):
    player = NFLPlayerSerializer(read_only=True)

    class Meta:
        model = Roster
        fields = ['id', 'player', 'roster_position', 'is_starter', 'acquired_date']


class MatchupSerializer(serializers.ModelSerializer):
    home_team = FantasyTeamSerializer(read_only=True)
    away_team = FantasyTeamSerializer(read_only=True)

    class Meta:
        model = Matchup
        fields = [
            'id', 'league', 'week', 'home_team', 'away_team',
            'home_score', 'away_score', 'is_complete'
        ]
