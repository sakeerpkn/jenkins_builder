from django.shortcuts import render

from login.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

import sys
from jenkinsapi.jenkins import Jenkins

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/projects/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })
 
    return render_to_response(
    'registration/register.html',
    variables,
    )
 

 
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')
 

def get_server_instance():
	jenkins_url = 'http://52.74.16.86:8080'
	server = Jenkins(jenkins_url, username = 'jenkins_ci', password = 'ee10d479a75e080e409a11a9c6dc3f8b')
	return server

@csrf_protect
@login_required
def projects(request):
	"""
	list all the current projects in jenkins
	"""

	jenkins = get_server_instance()
	if request.method == 'GET':
		print("itss GET call")
		jobs = jenkins.keys()
		return render_to_response('builds/projects.html',RequestContext(request, { 'jobs': jobs }))
	else:
  		all_jobs = []
		all_jobs = request.POST.getlist('jobs_name')
		for job in all_jobs:
			if (jenkins.has_job(job)):
				jenkins.build_job(job)
			else:
				pass
		return render_to_response('builds/projects.html',RequestContext(request, { }))
	    
	   
