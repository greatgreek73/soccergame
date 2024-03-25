import scipy.stats as stats
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Player, Club
from faker import Faker
from django.contrib import messages
from .forms import UserRegisterForm, CreateClubForm, GeneratePlayerForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .match_engine.engine import simulate_match

fake = Faker()

STATS = [
    'strength', 'stamina', 'pace', 'marking', 'tackling', 'work_rate',
    'positioning', 'passing', 'crossing', 'dribbling', 'ball_control',
    'heading', 'finishing', 'long_range', 'vision', 'handling', 'reflexes',
    'aerial', 'jumping', 'command', 'throwing', 'kicking'
]

def get_main_stats(position):
    if position == 'Goalkeeper':
        return ['reflexes', 'aerial', 'kicking']
    elif position == 'Right Back':
        return ['pace', 'stamina', 'tackling']
    elif position == 'Left Back':
        return ['pace', 'stamina', 'tackling']
    elif position == 'Center Back':
        return ['strength', 'marking', 'heading']
    elif position == 'Right Midfielder':
        return ['pace', 'dribbling', 'passing']
    elif position == 'Central Midfielder':
        return ['stamina', 'positioning', 'tackling']
    elif position == 'Left Midfielder':
        return ['pace', 'dribbling', 'passing']
    elif position == 'Attacking Midfielder':
        return ['dribbling', 'vision', 'long_range']
    elif position == 'Center Forward':
        return ['strength', 'finishing', 'heading']

def index(request):
    return render(request, 'index.html')

def generate_player(request):
    if request.method == 'POST':
        form = GeneratePlayerForm(request.POST)
        if form.is_valid():
            position = form.cleaned_data['position']
            Player.objects.create(
                first_name=fake.first_name_male(),
                last_name=fake.last_name_male(),
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
    club = get_object_or_404(Club, id=club_id)
    context = {
        'club': club,
        'form': GeneratePlayerForm()
    }
    return render(request, 'club_detail.html', context)

def create_club(request):
    if request.method == 'POST':
        form = CreateClubForm(request.POST)
        if form.is_valid():
            existing_club = Club.objects.filter(user=request.user).first()
            if existing_club:
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
            player_class = int(form.cleaned_data['player_class'])  # Преобразуем строку в целое число

            # Определяем среднее значение для выбранного класса
            class_means = {1: 60, 2: 50, 3: 40, 4: 35}
            mean_value = class_means[player_class]

            # Распределение 600 очков между 15 характеристиками
            total_points = 600
            main_stats = get_main_stats(position)
            secondary_stats = [stat for stat in STATS if stat not in main_stats]

            # Выделяем больше очков для основных характеристик
            points_for_main_stats = total_points * 0.5
            points_per_main_stat = points_for_main_stats / len(main_stats)

            # Оставшиеся очки распределяются равномерно между второстепенными характеристиками
            points_for_secondary_stats = total_points * 0.5
            points_per_secondary_stat = points_for_secondary_stats / len(secondary_stats)

            # Создаем словарь для присваивания характеристик игроку
            player_stats = {}
            for stat in STATS:
                if stat in main_stats:
                    player_stats[stat] = round(points_per_main_stat + points_per_secondary_stat)
                else:
                    player_stats[stat] = round(points_per_secondary_stat)

            # Обработка специальных случаев для вратарей
            if position == 'Goalkeeper':
                player_stats['reflexes'] = round(points_per_main_stat + points_per_secondary_stat)
                player_stats['aerial'] = round(points_per_main_stat + points_per_secondary_stat)
                player_stats['kicking'] = round(points_per_main_stat + points_per_secondary_stat)

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
            }

            print(f"Club country: {club.country}")
            locale = country_to_locale.get(club.country, 'en_US')
            print(f"Using locale: {locale}")

            fake = Faker(locale)

            while True:
                first_name = fake.first_name_male()
                last_name = fake.last_name_male()

                if not Player.objects.filter(first_name=first_name, last_name=last_name).exists():
                    break

            player = Player.objects.create(
                first_name=first_name,
                last_name=last_name,
                age=17,
                club=club,
                nationality=club.country,
                position=position,
                player_class=player_class,
                **player_stats
            )

            return redirect('club_detail', club_id=club.id)
    else:
        form = GeneratePlayerForm()

    context = {'form': form}
    return render(request, 'generate_player.html', context)

def player_detail(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    context = {
        'player': player
    }
    return render(request, 'player_detail.html', context)

def start_match(request, club_id):
    club1 = get_object_or_404(Club, id=club_id)
    opponent_club_id = request.GET.get('opponent_club_id')
    if opponent_club_id:
        try:
            club2 = get_object_or_404(Club, id=opponent_club_id)
        except Club.DoesNotExist:
            return render(request, 'error.html', {'error': 'Invalid opponent club'})

        all_players1 = Player.objects.filter(club=club1)
        all_players2 = Player.objects.filter(club=club2)

        winner, loser = simulate_match(all_players1, all_players2, club1, club2)

        winner_players = winner.players
        loser_players = loser.players

        context = {
            'club1': club1,
            'club2': club2,
            'winner_club': winner.club,
            'loser_club': loser.club,
            'winner_players': winner_players,
            'loser_players': loser_players,
        }

        return render(request, 'match.html', context)
    else:
        other_clubs = Club.objects.exclude(id=club_id)
        context = {
            'club': club1,
            'other_clubs': other_clubs,
        }
        return render(request, 'select_opponent.html', context)