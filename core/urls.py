from django.urls import path
from .views import (
    MergeRequestListView,
    MergeRequestDeleteView,
    MergeRequestDetailView,
    MergeRequestCreateView,
    merge_request_merge,
    load_repos,
    load_branches)

urlpatterns = [
    path('', MergeRequestCreateView.as_view(), name='core-home'),
    path('requests/', MergeRequestListView.as_view(), name='core-requests'),
    path('requests/<int:pk>/', MergeRequestDetailView.as_view(), name='merge-request-detail'),
    path('requests/<int:pk>/merge', merge_request_merge, name='merge-request-merge'),
    path('requests/<int:pk>/delete', MergeRequestDeleteView.as_view(), name='merge-request-delete'),
    path('ajax/load-repos/', load_repos, name='ajax_load_repos'),
    path('ajax/load-branches/', load_branches, name='ajax_load_branches'),
]
