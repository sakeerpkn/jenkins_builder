from forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from jenkinsapi.jenkins import Jenkins
from django.contrib.auth.models import User
from jenkins_interface_py27.constants import JENKINS_URL,\
    JENKINS_PASSWORD, JENKINS_USERNAME

@csrf_protect
def register(request):
    """
    register a user
    """
    form = RegistrationForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
#         form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password1'],
                                            email=form.cleaned_data['email']
                                            )
            print user
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return HttpResponseRedirect('/projects/')
    else:
        print "not post"
#         form = RegistrationForm()
    variables = RequestContext(request, {'form': form})
    return render_to_response('registration/register.html',variables)
 

 
def logout_page(request):
    """
    logout function
    """
    logout(request)
    return HttpResponseRedirect('/')
 

def get_server_instance():
    """
    get the server instance
    """
    server = Jenkins(JENKINS_URL, username = JENKINS_USERNAME, password = JENKINS_PASSWORD)
    return server

@csrf_protect
@login_required
def projects(request):
    """
    list all the current projects in jenkins
    """
    all_jobs = []
    builds = []
    jobs = []
    jenkins = get_server_instance()
    if request.method == 'GET':
        jobs = jenkins.keys()
        return render_to_response('builds/projects.html',RequestContext(request, { 'jobs': jobs }))
    else:
        all_jobs = request.POST.getlist('jobs_name')
        for job in all_jobs:
            if (jenkins.has_job(job)):
                build_info = {}
                jenkins.build_job(job)
                lgb = jenkins[job].get_last_good_build()
                lgb = str(lgb).split()
                build_info['job_name'] = lgb[0]
                build_info['build_number'] = lgb[1].replace("#", "")
                success_build_url = JENKINS_URL + '/job/' +  build_info['job_name'] + '/' + build_info['build_number']
                build_info['build_url'] = success_build_url
                builds.append(build_info)
            else:
                pass
        return render_to_response('builds/projects.html',RequestContext(request, {'builds':builds }))
        
        