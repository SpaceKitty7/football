from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import League, NFLPlayer, FantasyTeam, Roster, Matchup
from .serializers import (
    LeagueSerializer, LeagueCreateSerializer, NFLPlayerSerializer,
    FantasyTeamSerializer, RosterSerializer, MatchupSerializer
)


class LeagueViewSet(viewsets.ModelViewSet):
    queryset = League.objects.filter(is_active=True)
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return LeagueCreateSerializer
        return LeagueSerializer

    def get_queryset(self):
        queryset = League.objects.filter(is_active=True)

        # Filter by public/private
        is_public = self.request.query_params.get('is_public')
        if is_public is not None:
            queryset = queryset.filter(is_public=is_public.lower() == 'true')

        # Filter by league type
        league_type = self.request.query_params.get('league_type')
        if league_type:
            queryset = queryset.filter(league_type=league_type)

        # Filter by available spots
        has_spots = self.request.query_params.get('has_spots')
        if has_spots and has_spots.lower() == 'true':
            queryset = [l for l in queryset if l.spots_available > 0]

        return queryset

    def perform_create(self, serializer):
        serializer.save(commissioner=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def join(self, request, pk=None):
        league = self.get_object()

        # Check if already a member
        if FantasyTeam.objects.filter(league=league, owner=request.user).exists():
            return Response(
                {'error': 'You are already a member of this league'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if league has spots
        if league.spots_available <= 0:
            return Response(
                {'error': 'This league is full'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create team for user
        team_name = request.data.get('team_name', f"{request.user.username}'s Team")
        team = FantasyTeam.objects.create(
            name=team_name,
            owner=request.user,
            league=league
        )

        return Response({
            'message': f'Successfully joined {league.name}',
            'team': FantasyTeamSerializer(team).data
        }, status=status.HTTP_201_CREATED)


class NFLPlayerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NFLPlayer.objects.filter(is_active=True)
    serializer_class = NFLPlayerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = NFLPlayer.objects.filter(is_active=True)

        position = self.request.query_params.get('position')
        if position:
            queryset = queryset.filter(position=position)

        team = self.request.query_params.get('team')
        if team:
            queryset = queryset.filter(nfl_team=team)

        return queryset


class FantasyTeamViewSet(viewsets.ModelViewSet):
    queryset = FantasyTeam.objects.all()
    serializer_class = FantasyTeamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FantasyTeam.objects.filter(owner=self.request.user)

    @action(detail=True, methods=['get'])
    def roster(self, request, pk=None):
        team = self.get_object()
        roster = Roster.objects.filter(fantasy_team=team)
        serializer = RosterSerializer(roster, many=True)
        return Response(serializer.data)


class MatchupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Matchup.objects.all()
    serializer_class = MatchupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Matchup.objects.all()

        league_id = self.request.query_params.get('league')
        if league_id:
            queryset = queryset.filter(league_id=league_id)

        week = self.request.query_params.get('week')
        if week:
            queryset = queryset.filter(week=week)

        return queryset
