from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from mentorski_app import models, forms
from .forms import StudentForm, LoginForm, PredmetiForm
from .models import Predmeti, Korisnici, Upisi


# Create your views here.
def register(request): 
    if request.method == "POST":
            admn = request.user
            username = request.POST.get('username', '')
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            password = request.POST.get('password1', '')
            useremail = request.POST.get('email', '')
            status = request.POST.get('status', '')
            form = StudentForm(request.POST)
            user = authenticate(request, useremail=useremail, password=password)
            if user is None and form.is_valid():
                user = get_user_model().objects.create_user(username=username,first_name=first_name, last_name=last_name, password=password, email=useremail, is_staff=False, is_superuser=False, role='student', status=status)
                user.save()
                login(request, user)
                userid=Korisnici.objects.get(username=username)
                return HttpResponseRedirect('/upisni_list/'+str(userid.id))
            else:
                messages.error(request, f'Something went wrong!')
                return HttpResponseRedirect('/register')
    elif request.method == "GET":
        return render(request, 'register.html', {'form':StudentForm})
    

def logoutPg(request):
    logout(request)
    messages.success(request, f'You have been logged out successfully!')
    response = HttpResponseRedirect('/login')
    # Redirect to a success page.
    return response

def loginPg(request):
    form=LoginForm()
    if request.method == "POST":
        form=LoginForm(request.POST)
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, email=email, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff == True:
                return HttpResponseRedirect('/courses')
            else:
                userid=Korisnici.objects.get(username=username)
                return HttpResponseRedirect('/upisni_list/'+str(userid.id))
        else:
            messages.success(request, f'An error occured!')
            return HttpResponseRedirect('/login')
    if request.method == "GET":        
        return render(request, 'login.html', {'form':form})


@login_required(login_url='login')
def courses(request): 
    all_courses = Predmeti.objects.all()
    return render(request, 'courses.html', context = {'all_courses': all_courses})

#Add/Update/View/Delete course
def Add_course(request):
    user = request.user
    form = PredmetiForm()
    if request.method == 'POST':
        form = PredmetiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('courses')
        return HttpResponseRedirect('/add')
    if request.method == 'GET':
        return render(request, 'add.html', context = {'form':form, 'user':user})

def delete_course(request,pid):
    course = Predmeti.objects.get(id=pid)
    course.delete() 
    return HttpResponseRedirect('/courses')

def course_delete(request,pid):
    course = Predmeti.objects.get(id=pid)
    return render(request, 'course_delete.html', context = {'course': course})   
   

def detail_course(request,pid):
    course = Predmeti.objects.get(id=pid)
    all_courses = Predmeti.objects.all()
    return render (request, 'courses.html', context = {'all_courses':all_courses,'course': course})
    if request.method=="POST":
        return HttpResponseRedirect('/courses'+str(pid))

def edit_course(request,pid):
    obj = get_object_or_404(Predmeti, id = pid)
    course = Predmeti.objects.get(id=pid)
    form = PredmetiForm(instance=course)
    if request.method=="POST":
        form = PredmetiForm(request.POST, instance = obj)
        if form.is_valid():
            obj.save()
        return HttpResponseRedirect('/courses')
    return render(request, 'edit.html', context = {'form':form,'course': obj})    

@login_required(login_url='login')
def students(request):
    popis = Korisnici.objects.all()
    return render (request, 'students.html', context = {'popis': popis})

#Student View
def neupisani_predmeti(kid):
    subjects=Predmeti.objects.all()
    upisni_list=Upisi.objects.all().filter(korisnici_id=kid)
    neupisani_red={}
    neupisani_izv={}
    upisani={}
    for s in subjects:
        for u in upisni_list:
            if s.id == u.predmeti_id.id:
                if u.korisnici_id.status == 'redovni':
                    upisani.update({s.ime:s.sem_redovni})
                if u.korisnici_id.status == 'izvanredni':
                    upisani.update({s.ime:s.sem_izvanredni})
    for s in subjects:
        if s.ime not in upisani:
            neupisani_red.update({s.id:s.ime})
            neupisani_izv.update({s.id:s.ime})
    return neupisani_red, neupisani_izv

@login_required(login_url='login')
def upisni_list(request,kid): 
    upisni = Upisi.objects.filter(korisnici_id=kid)
    usr = Korisnici.objects.get(id=kid)
    neupisanir, neupisanii = neupisani_predmeti(kid)
    svi = Predmeti.objects.all()
    return render(request, 'upisni_list.html', context = {'usr': usr, 'upisni':upisni, 'neupisanir':neupisanir,'neupisanii':neupisanii, 'svi':svi,})

def pass_subj(request, pid, sid):
    predmet=Upisi.objects.get(predmeti_id=pid, korisnici_id=sid)
    predmet.status="passed"
    predmet.save()
    return HttpResponseRedirect('/upisni_list/'+str(sid))

def repeat_subj(request, pid, sid):
    predmet=Upisi.objects.get(predmeti_id=pid, korisnici_id=sid)
    if predmet.status == "not_passed":
        predmet.repeat_subj = predmet.repeat_subj+1
    else:
        predmet.status="not_passed"
    predmet.save()
    return HttpResponseRedirect('/upisni_list/'+str(sid))

def remove_subj(request, id):
    u=Upisi.objects.get(id=id)
    sid=u.korisnici_id_id
    u.delete()
    return HttpResponseRedirect('/upisni_list/'+str(sid))

def add_subj(request, pid, sid):
        upis=Upisi()
        upis.predmeti_id_id = pid
        upis.korisnici_id_id = sid
        upis.status = "enrolled"
        upis.save()
        return HttpResponseRedirect('/upisni_list/'+str(sid))

