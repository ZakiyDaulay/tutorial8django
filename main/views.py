from django.shortcuts import render,redirect,reverse
from main.forms import MoodEntryForm
from main.models import MoodEntry
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse



@login_required(login_url='/login')
def show_main(request):

    context = {
        'name': request.user.username,
        'class': 'PBP KKI',
        'npm': '2306170130',

        'last_login': request.COOKIES.get('last_login', 'No recent login information')
    }

    return render(request, "main.html", context)


def create_mood_entry(request):
    form = MoodEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        mood_entry = form.save(commit=False)
        mood_entry.user = request.user
        mood_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_mood_entry.html", context)

def show_xml(request):
    data = MoodEntry.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_xml_by_id(request, id):
    data = MoodEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")
def show_json(request):
    data =  MoodEntry.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
def show_json_by_id(request, id):
    data = MoodEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

       
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                response = HttpResponseRedirect(reverse("main:show_main"))
                response.set_cookie('last_login', str(datetime.datetime.now()))
                return response
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    else:
        form = AuthenticationForm(request)
        
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def edit_mood(request, id):
    # Get mood entry based on id
    mood = MoodEntry.objects.get(pk = id)

    # Set mood entry as an instance of the form
    form = MoodEntryForm(request.POST or None, instance=mood)

    if form.is_valid() and request.method == "POST":
        # Save form and return to home page
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "edit_mood.html", context)

def delete_mood(request, id):
    # Get mood based on id
    mood = MoodEntry.objects.get(pk = id)
    # Delete mood
    mood.delete()
    # Return to home page
    return HttpResponseRedirect(reverse('main:show_main'))

@csrf_exempt
@require_POST
def add_mood_entry_ajax(request):
    mood = strip_tags(request.POST.get("mood")) # strip HTML tags!
    print(mood)
    feelings = strip_tags(request.POST.get("feelings")) # strip HTML tags!
    mood_intensity = request.POST.get("mood_intensity")
    user = request.user

    new_mood = MoodEntry(
        mood=mood, feelings=feelings,
        mood_intensity=mood_intensity,
        user=user
    )
    new_mood.save()

    return HttpResponse(b"CREATED", status=201)

@csrf_exempt
def create_mood_flutter(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        new_mood = MoodEntry.objects.create(
            user=request.user,
            mood=data["mood"],
            mood_intensity=int(data["mood_intensity"]),
            feelings=data["feelings"]
        )

        new_mood.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)