from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Player, Club
from faker import Faker
from django.contrib import messages
from .forms import UserRegisterForm, CreateClubForm, GeneratePlayerForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import random
from .match_engine.engine import simulate_match

fake = Faker()

def index(request):
    return render(request, 'index.html')

def generate_player(request):
    if request.method == 'POST':
        form = GeneratePlayerForm(request.POST)
        if form.is_valid():
            position = form.cleaned_data['position']
            Player.objects.create(
                name=f"{fake.last_name_male()} {fake.first_name_male()}",
                age=17,
                position=position
            )
            return HttpResponseRedirect('/generate/')
    else:
        form = GeneratePlayerForm()
    return render(request, 'generate_player.html', {'form': form})

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
        'club': club,
        'form': GeneratePlayerForm()
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

    if request.method == 'POST':
        form = GeneratePlayerForm(request.POST)
        if form.is_valid():
            position = form.cleaned_data['position']

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

            if position == 'Goalkeeper':
                player = Player.objects.create(
                    name=f"{fake.last_name_male()} {fake.first_name_male()}",
                    age=17,
                    club=club,
                    nationality=club.country,
                    position=position,
                    strength=random.randint(1, 20),
                    stamina=random.randint(1, 20),
                    pace=random.randint(1, 20),
                    handling=random.randint(1, 20),
                    reflexes=random.randint(1, 20),
                    positioning=random.randint(1, 20),
                    aerial=random.randint(1, 20),
                    jumping=random.randint(1, 20),
                    command=random.randint(1, 20),
                    throwing=random.randint(1, 20),
                    kicking=random.randint(1, 20)
                )
            else:
                player = Player.objects.create(
                    name=f"{fake.last_name_male()} {fake.first_name_male()}",
                    age=17,
                    club=club,
                    nationality=club.country,
                    position=position,
                    strength=random.randint(1, 20),
                    stamina=random.randint(1, 20),
                    pace=random.randint(1, 20),
                    marking=random.randint(1, 20),
                    tackling=random.randint(1, 20),
                    work_rate=random.randint(1, 20),
                    positioning=random.randint(1, 20),
                    passing=random.randint(1, 20),
                    crossing=random.randint(1, 20),
                    dribbling=random.randint(1, 20),
                    ball_control=random.randint(1, 20),
                    heading=random.randint(1, 20),
                    finishing=random.randint(1, 20),
                    long_range=random.randint(1, 20),
                    vision=random.randint(1, 20)
                )

            return redirect('club_detail', club_id=club.id)
    else:
        form = GeneratePlayerForm()

    context = {'form': form}
    return render(request, 'generate_player.html', context)

def player_detail(request, player_id):
    player = Player.objects.get(id=player_id)
    context = {
        'player': player
    }
    return render(request, 'player_detail.html', context)

def start_match(request, club_id):
    club1 = Club.objects.get(id=club_id)
    opponent_club_id = request.GET.get('opponent_club_id')
    if opponent_club_id:
        try:
            club2 = Club.objects.get(id=opponent_club_id)
        except Club.DoesNotExist:
            # Обработка случая, когда клуб-соперник не найден
            return render(request, 'error.html', {'error': 'Invalid opponent club'})

        players1 = Player.objects.filter(club=club1)
        players2 = Player.objects.filter(club=club2)

        winner, loser = simulate_match(players1, players2)

        context = {
            'club1': club1,
            'club2': club2,
            'winner': winner,
            'loser': loser,
            'winner_players': winner.players if winner else None,
            'loser_players': loser.players if loser else None,
        }

        return render(request, 'match.html', context)
    else:
        # Если club2_id не передан, отображаем форму выбора соперника
        other_clubs = Club.objects.exclude(id=club_id)
        context = {
            'club': club1,
            'other_clubs': other_clubs,
        }
        return render(request, 'select_opponent.html', context)