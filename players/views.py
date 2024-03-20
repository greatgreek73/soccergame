from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Player, Club
from faker import Faker
from django.contrib import messages
from .forms import UserRegisterForm, CreateClubForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# fake = Faker()

def index(request):
    return render(request, 'index.html')

def generate_player(request):
    if request.method == 'POST':
        Player.objects.create(
            name=f"{fake.last_name_male()} {fake.first_name_male()}",
            age=17
        )
        return HttpResponseRedirect('/generate/')
    return render(request, 'generate_player.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Check if the user has a club
            try:
                club = Club.objects.get(user=user)
                return redirect('club_detail', club_id=club.id)
            except Club.DoesNotExist:
                return redirect('create_club')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

@login_required
def home(request):
    try:
        club = Club.objects.get(user=request.user)
        return redirect('club_detail', club_id=club.id)
    except Club.DoesNotExist:
        return redirect('create_club')

def club_detail(request, club_id):
    club = Club.objects.get(id=club_id)
    context = {
        'club': club
    }
    return render(request, 'club_detail.html', context)

def create_club(request):
    if request.method == 'POST':
        form = CreateClubForm(request.POST)
        if form.is_valid():
            # Check if the user already has a club
            existing_club = Club.objects.filter(user=request.user).first()
            if existing_club:
                # If the club already exists, redirect to the club page
                return redirect('club_detail', club_id=existing_club.id)
            
            new_club = Club.objects.create(
                user=request.user,
                name=form.cleaned_data['name'],
                country=form.cleaned_data['country']
            )
            return redirect('club_detail', club_id=new_club.id)
    else:
        form = CreateClubForm()
    return render(request, 'create_club.html', {'form': form})

def generate_player_for_club(request, club_id):
    try:
        club = Club.objects.get(id=club_id)
    except Club.DoesNotExist:
        return redirect('home')

    if club.user != request.user:
        return redirect('home')

    # Dictionary for mapping countries to Faker locales
    country_to_locale = {
    'USA': 'en_US',
    'Russia': 'ru_RU',
    'China': 'zh_CN',
    'Belgium': 'nl_BE',
    'New Zealand': 'en_NZ',
    'Austria': 'de_AT',
    'Brazil': 'pt_BR',
    'Greece': 'el_GR',
    'Argentina': 'es_AR',
    'Italy': 'it_IT',
    'Germany': 'de_DE',
    # Add more countries as needed
}

    print(f"Club country: {club.country}")
    # Set Faker locale based on the club's country
    locale = country_to_locale.get(club.country, 'en_US')  # 'en_US' will be used as default
    print(f"Using locale: {locale}")
    
    fake = Faker(locale)

    Player.objects.create(
        name=f"{fake.last_name_male()} {fake.first_name_male()}",
        age=17,
        club=club,
        nationality=club.country  # Set player nationality based on club's country
    )
    return redirect('club_detail', club_id=club.id)

def player_detail(request, player_id):
    player = Player.objects.get(id=player_id)
    context = {
        'player': player
    }
    return render(request, 'player_detail.html', context)