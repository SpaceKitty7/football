from django.db import models
from django.conf import settings


class League(models.Model):
    """Fantasy football league"""
    LEAGUE_TYPES = [
        ('standard', 'Standard'),
        ('ppr', 'PPR'),
        ('half_ppr', 'Half PPR'),
        ('dynasty', 'Dynasty'),
        ('keeper', 'Keeper'),
    ]

    SCORING_TYPES = [
        ('head_to_head', 'Head to Head'),
        ('points', 'Total Points'),
        ('roto', 'Rotisserie'),
    ]

    name = models.CharField(max_length=100)
    commissioner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='commissioned_leagues'
    )
    league_type = models.CharField(max_length=20, choices=LEAGUE_TYPES, default='standard')
    scoring_type = models.CharField(max_length=20, choices=SCORING_TYPES, default='head_to_head')
    max_teams = models.PositiveIntegerField(default=12)
    is_public = models.BooleanField(default=True)
    entry_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    prize_pool = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    draft_date = models.DateTimeField(blank=True, null=True)
    season_year = models.PositiveIntegerField(default=2024)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.season_year})"

    @property
    def current_team_count(self):
        return self.teams.count()

    @property
    def spots_available(self):
        return self.max_teams - self.current_team_count


class NFLPlayer(models.Model):
    """Real NFL player data"""
    POSITIONS = [
        ('QB', 'Quarterback'),
        ('RB', 'Running Back'),
        ('WR', 'Wide Receiver'),
        ('TE', 'Tight End'),
        ('K', 'Kicker'),
        ('DEF', 'Defense/Special Teams'),
    ]

    NFL_TEAMS = [
        ('ARI', 'Arizona Cardinals'),
        ('ATL', 'Atlanta Falcons'),
        ('BAL', 'Baltimore Ravens'),
        ('BUF', 'Buffalo Bills'),
        ('CAR', 'Carolina Panthers'),
        ('CHI', 'Chicago Bears'),
        ('CIN', 'Cincinnati Bengals'),
        ('CLE', 'Cleveland Browns'),
        ('DAL', 'Dallas Cowboys'),
        ('DEN', 'Denver Broncos'),
        ('DET', 'Detroit Lions'),
        ('GB', 'Green Bay Packers'),
        ('HOU', 'Houston Texans'),
        ('IND', 'Indianapolis Colts'),
        ('JAX', 'Jacksonville Jaguars'),
        ('KC', 'Kansas City Chiefs'),
        ('LAC', 'Los Angeles Chargers'),
        ('LAR', 'Los Angeles Rams'),
        ('LV', 'Las Vegas Raiders'),
        ('MIA', 'Miami Dolphins'),
        ('MIN', 'Minnesota Vikings'),
        ('NE', 'New England Patriots'),
        ('NO', 'New Orleans Saints'),
        ('NYG', 'New York Giants'),
        ('NYJ', 'New York Jets'),
        ('PHI', 'Philadelphia Eagles'),
        ('PIT', 'Pittsburgh Steelers'),
        ('SEA', 'Seattle Seahawks'),
        ('SF', 'San Francisco 49ers'),
        ('TB', 'Tampa Bay Buccaneers'),
        ('TEN', 'Tennessee Titans'),
        ('WAS', 'Washington Commanders'),
    ]

    name = models.CharField(max_length=100)
    position = models.CharField(max_length=3, choices=POSITIONS)
    nfl_team = models.CharField(max_length=3, choices=NFL_TEAMS)
    jersey_number = models.PositiveIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_injured = models.BooleanField(default=False)
    injury_status = models.CharField(max_length=50, blank=True, null=True)
    bye_week = models.PositiveIntegerField(blank=True, null=True)

    # Season stats (updated weekly)
    points_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    average_points = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.position} - {self.nfl_team})"

    class Meta:
        ordering = ['position', 'name']


class FantasyTeam(models.Model):
    """User's team within a league"""
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='fantasy_teams'
    )
    league = models.ForeignKey(
        League,
        on_delete=models.CASCADE,
        related_name='teams'
    )
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    ties = models.PositiveIntegerField(default=0)
    points_for = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    points_against = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.owner.username})"

    class Meta:
        unique_together = ['owner', 'league']


class Roster(models.Model):
    """Player assignment to a fantasy team"""
    ROSTER_POSITIONS = [
        ('QB', 'Quarterback'),
        ('RB1', 'Running Back 1'),
        ('RB2', 'Running Back 2'),
        ('WR1', 'Wide Receiver 1'),
        ('WR2', 'Wide Receiver 2'),
        ('TE', 'Tight End'),
        ('FLEX', 'Flex'),
        ('K', 'Kicker'),
        ('DEF', 'Defense'),
        ('BN1', 'Bench 1'),
        ('BN2', 'Bench 2'),
        ('BN3', 'Bench 3'),
        ('BN4', 'Bench 4'),
        ('BN5', 'Bench 5'),
        ('IR', 'Injured Reserve'),
    ]

    fantasy_team = models.ForeignKey(
        FantasyTeam,
        on_delete=models.CASCADE,
        related_name='roster'
    )
    player = models.ForeignKey(
        NFLPlayer,
        on_delete=models.CASCADE,
        related_name='roster_assignments'
    )
    roster_position = models.CharField(max_length=4, choices=ROSTER_POSITIONS)
    is_starter = models.BooleanField(default=False)

    acquired_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player.name} on {self.fantasy_team.name} ({self.roster_position})"

    class Meta:
        unique_together = ['fantasy_team', 'player']


class Matchup(models.Model):
    """Weekly matchup between two teams"""
    league = models.ForeignKey(
        League,
        on_delete=models.CASCADE,
        related_name='matchups'
    )
    week = models.PositiveIntegerField()
    home_team = models.ForeignKey(
        FantasyTeam,
        on_delete=models.CASCADE,
        related_name='home_matchups'
    )
    away_team = models.ForeignKey(
        FantasyTeam,
        on_delete=models.CASCADE,
        related_name='away_matchups'
    )
    home_score = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    away_score = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    is_complete = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Week {self.week}: {self.away_team.name} @ {self.home_team.name}"

    class Meta:
        unique_together = ['league', 'week', 'home_team', 'away_team']
