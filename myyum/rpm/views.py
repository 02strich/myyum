from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext

from myyum.rpm.models import *
from myyum.rpm.forms import *

def repository_index(request):
    repos = Repository.objects.all()
    return render_to_response("repo_index.html", dict(repos=repos), context_instance=RequestContext(request))


def repository_view(request, repository_id):
    repo = get_object_or_404(Repository, id=repository_id)
    return render_to_response("repo_view.html", dict(repo=repo), context_instance=RequestContext(request))

    
def repository_create(request):
    form = RepositoryForm(request.POST or None)
    
    # set owner to current user
    form.instance.owner = request.user
    
    if form.is_valid():
        
        # save instance
        s = form.save()
        
        messages.add_message(request, messages.SUCCESS, "Successfully created repository.")
        return redirect('myyum.rpm.views.repository_view', s.id)
    else:
        return render_to_response("repo_create.html", dict(form=form), context_instance=RequestContext(request))


def repository_edit(request, repository_id):
    repo = get_object_or_404(Repository, id=repository_id)
    form = RepositoryForm(request.POST or None, instance=repo)
    
    if form.is_valid():
        form.save()
        
        messages.add_message(request, messages.SUCCESS, "Successfully updated repository.")
        return redirect('myyum.rpm.views.repository_view', s.id)
    else:
        return render_to_response("repo_edit.html", dict(form=form), context_instance=RequestContext(request))

def repository_delete(request, repository_id):
    repo = get_object_or_404(Repository, id=repository_id)
    
    if request.method == 'POST':
        repo.delete()
        
        messages.add_message(request, messages.SUCCESS, "Successfully deleted repository.")
        return redirect('myyum.rpm.views.repository_index')
    else:
        return render_to_response("repo_delete.html", dict(repo=repo), context_instance=RequestContext(request))


def package_upload(request, repository_id):
    repo = get_object_or_404(Repository, id=repository_id)
    
    form = PackageUploadForm(repo, request.POST or None, request.FILES or None)
    
    if form.is_valid():
        try:
            pkg = form.save()
        except IntegrityError:
            messages.add_message(request, messages.ERROR, "Package already exists.")
            return render_to_response("pkg_upload.html", dict(repo=repo, form=form), context_instance=RequestContext(request))
        
        messages.add_message(request, messages.SUCCESS, "Successfully uploaded package.")
        return redirect('myyum.rpm.views.repository_view', repo.id)
    else:
        return render_to_response("pkg_upload.html", dict(repo=repo, form=form), context_instance=RequestContext(request))


def package_view(request, repository_id, package_id):
    repo = get_object_or_404(Repository, id=repository_id)
    package = get_object_or_404(RPMPackage, id=package_id)
    
    return render_to_response("pkg_view.html", dict(repo=repo, pkg=package), context_instance=RequestContext(request))


def package_delete(request, repository_id, package_id):
    repo = get_object_or_404(Repository, id=repository_id)
    pkg = get_object_or_404(RPMPackage, id=package_id)

    if request.method == 'POST':
        pkg.delete()
        
        messages.add_message(request, messages.SUCCESS, "Successfully deleted package.")
        return redirect('myyum.rpm.views.repository_view', repo.id)
    else:
        return render_to_response("pkg_delete.html", dict(repo=repo, pkg=pkg), context_instance=RequestContext(request))

