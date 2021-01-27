from django.urls import path
from django.contrib.auth.decorators import login_required
from teams.views import *

app_name = 'teams'

urlpatterns = [
    path('', login_required(TeamHomeView.as_view()), name='team_home'),

    path('create/', login_required(CreateTeam.as_view()), name='create_team'),
    path('join/', login_required(JoinTeam.as_view()), name='join_team'),

    # Manage Team
    path('<str:team>/', login_required(ManageTeam.as_view()), name='manage_team'),
    path('<str:team>/leave/', login_required(LeaveTeam.as_view()), name='leave_team'),
    path('<str:team>/delete', login_required(DeleteTeam.as_view()), name='delete_team'),

    path('<str:team>/<str:user>/', login_required(KickUser.as_view()), name='kick_user'),
]

# TODO: SLUGIFY URL!
