from django.urls import path
from django.contrib.auth.decorators import login_required
from teams.views import *

app_name = 'teams'

urlpatterns = [
    path('', login_required(TeamHomeView.as_view()), name='team_home'),

    path('create/', login_required(CreateTeam.as_view()), name='create_team'),
    path('join/', login_required(JoinTeam.as_view()), name='join_team'),

    # Manage Team
    path('<slug:team>/', login_required(ManageTeam.as_view()), name='manage_team'),
    path('<slug:team>/identifier/', login_required(ChangeTeamIdentifier.as_view()), name='change_identifier'),
    path('<slug:team>/name/', login_required(ChangeTeamName.as_view()), name='change_name'),

    path('<slug:team>/join/<str:user>/', login_required(AcceptUser.as_view()), name='accept_user'),
    path('<slug:team>/leave/<str:user>/', login_required(KickUser.as_view()), name='kick_user'),

    path('<slug:team>/leave/', login_required(LeaveTeam.as_view()), name='leave_team'),
    path('<slug:team>/delete/', login_required(DeleteTeam.as_view()), name='delete_team'),
]
