from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'leagues', views.LeagueViewSet)
router.register(r'players', views.NFLPlayerViewSet)
router.register(r'teams', views.FantasyTeamViewSet)
router.register(r'matchups', views.MatchupViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
