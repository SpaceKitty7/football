from django.contrib import admin
from .models import League, NFLPlayer, FantasyTeam, Roster, Matchup


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ['name', 'commissioner', 'league_type', 'max_teams', 'current_team_count', 'is_public', 'season_year']
    list_filter = ['league_type', 'scoring_type', 'is_public', 'is_active', 'season_year']
    search_fields = ['name', 'commissioner__username']
    ordering = ['-created_at']


@admin.register(NFLPlayer)
class NFLPlayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'nfl_team', 'is_active', 'is_injured', 'points_total', 'average_points']
    list_filter = ['position', 'nfl_team', 'is_active', 'is_injured']
    search_fields = ['name']
    ordering = ['position', 'name']


@admin.register(FantasyTeam)
class FantasyTeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'league', 'wins', 'losses', 'ties', 'points_for']
    list_filter = ['league']
    search_fields = ['name', 'owner__username']
    ordering = ['-points_for']


@admin.register(Roster)
class RosterAdmin(admin.ModelAdmin):
    list_display = ['player', 'fantasy_team', 'roster_position', 'is_starter']
    list_filter = ['roster_position', 'is_starter', 'fantasy_team__league']
    search_fields = ['player__name', 'fantasy_team__name']


@admin.register(Matchup)
class MatchupAdmin(admin.ModelAdmin):
    list_display = ['league', 'week', 'home_team', 'away_team', 'home_score', 'away_score', 'is_complete']
    list_filter = ['league', 'week', 'is_complete']
    ordering = ['league', 'week']
