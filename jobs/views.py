from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job, Application
from .forms import JobForm, ApplicationForm

def home(request):
    query = request.GET.get('q', '')
    if query:
        jobs = Job.objects.filter(title__icontains=query).order_by('-date_posted')
    else:
        jobs = Job.objects.all().order_by('-date_posted')
    job_count = Job.objects.count()
    return render(request, 'jobs/home.html', {'jobs': jobs, 'query': query, 'job_count': job_count})

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    has_applied = False
    if request.user.is_authenticated and request.user.user_type == 'candidate':
        has_applied = Application.objects.filter(job=job, candidate=request.user).exists()
    return render(request, 'jobs/job_detail.html', {'job': job, 'has_applied': has_applied})

@login_required
def create_job(request):
    if request.user.user_type != 'employer':
        messages.error(request, 'Only employers can post jobs.')
        return redirect('home')
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm()
    return render(request, 'jobs/job_form.html', {'form': form, 'title': 'Post a New Job'})

@login_required
def update_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.user != job.employer:
        messages.error(request, 'You are not authorized to edit this job.')
        return redirect('home')
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/job_form.html', {'form': form, 'title': 'Update Job'})

@login_required
def delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.user != job.employer:
        messages.error(request, 'You are not authorized to delete this job.')
        return redirect('home')
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully!')
        return redirect('home')
    return render(request, 'jobs/job_confirm_delete.html', {'job': job})

@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.user.user_type != 'candidate':
        messages.error(request, 'Only candidates can apply for jobs.')
        return redirect('job_detail', pk=pk)
    if Application.objects.filter(job=job, candidate=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_detail', pk=pk)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.candidate = request.user
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('job_detail', pk=pk)
    else:
        form = ApplicationForm()
    return render(request, 'jobs/apply.html', {'form': form, 'job': job})

@login_required
def dashboard(request):
    user = request.user
    if user.user_type == 'employer':
        jobs = Job.objects.filter(employer=user).order_by('-date_posted')
        total_applications = Application.objects.filter(job__employer=user).count()
        return render(request, 'jobs/dashboard_employer.html', {
            'jobs': jobs,
            'total_applications': total_applications,
        })
    else:
        applications = Application.objects.filter(candidate=user).order_by('-date_applied')
        return render(request, 'jobs/dashboard_candidate.html', {
            'applications': applications,
        })
