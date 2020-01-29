from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.urls import reverse_lazy
from github import Github
from .models import MergeRequest
from .forms import MergeRequestCreationForm



class MergeRequestListView(LoginRequiredMixin, ListView):
    model = MergeRequest
    template_name = 'core/requests.html'
    context_object_name = 'merge_requests'
    ordering = ['-date_opened']


class MergeRequestDetailView(LoginRequiredMixin, DetailView):
    model = MergeRequest


class MergeRequestCreateView(LoginRequiredMixin, CreateView):
    model = MergeRequest
    form_class = MergeRequestCreationForm
    success_url = reverse_lazy('core-requests')

    def form_valid(self, form):
        form.instance.author = self.request.user

        send_mail(
            'Merge Request',
            '{} wants to merge branch {} of {} into {} \nPlease go to http://127.0.0.1:8000/requests to view this.'.format(
                form.instance.author,
                form.instance.source_branch,
                form.instance.repo,
                form.instance.target_branch
            ),
            'from@example.com',
            [form.instance.target_email],
            fail_silently=False,
        )
        return super().form_valid(form)

class MergeRequestDeleteView(LoginRequiredMixin, DeleteView):
    model = MergeRequest
    success_url = '/requests'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        send_mail(
            'Merge Request',
            'The following merge request was deleted by {}: {}'.format(
                request.user.username,
                obj.title
            ),
            request.user.email,
            [obj.target_email],
            fail_silently=False,
        )
        return super().delete(request, *args, **kwargs)

def merge_request_merge(request, pk):
    merge_request = MergeRequest.objects.filter(pk=pk).first()
    send_mail(
        'Merge Request',
        'The following merge request was approved by {}: {}\nIt is being merged now.'.format(
            request.user.username,
            merge_request.title
        ),
        request.user.email,
        [merge_request.target_email],
        fail_silently=False,
    )
    print(request.user.social_auth.values())
    access_token = request.user.social_auth.get(provider='github').access_token
    git_instance = Github(access_token)

    repo = git_instance.get_user().get_repo(merge_request.repo)

    base = repo.get_branch(merge_request.target_branch)
    head = repo.get_branch(merge_request.source_branch)

    merge_to_master = repo.merge(base, head.commit.sha, "Merge from {} into {} approved by {}".format(
        head,
        base,
        request.user.username
    ))
    merge_request.status = 'Merged'
    merge_request.save()
    return redirect('core-requests')



def load_repos(request):
    access_token = request.user.social_auth.get(provider='github').extra_data['access_token']
    git_instance = Github(access_token)
    repos = git_instance.get_user().get_repos()
    return render(request, 'core/repo_dropdown_list_options.html', {'repos': repos})

def load_branches(request):
    repo = request.GET.get('repo')
    access_token = request.user.social_auth.get(provider='github').extra_data['access_token']
    git_instance = Github(access_token)
    branches = []
    for branch in git_instance.get_user().get_repo(repo).get_branches():
        branches.append(branch.name)
    if request.GET.get('source'):
        # Remove master as source
        branches.remove('master')
    if request.GET.get('source_branch'):
        branches.remove(request.GET.get('source_branch'))

    return render(request, 'core/branch_dropdown_list_options.html', {'branches': branches})
