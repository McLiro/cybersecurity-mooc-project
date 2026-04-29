from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.db.models import Q
from .models import Board
from .forms import BoardForm, NoticeForm
from .decorators import require_authorization, require_ownership

def login(request):
    return render(request, 'accounts/login.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def home(request):
    """Home page showing user's boards and open boards."""
    user_boards = Board.objects.filter(owner=request.user)
    open_boards = Board.objects.filter(
        Q(is_private=False) & ~Q(owner=request.user)
        |
        Q(is_private=True, users=request.user)
    )
    context = {
        'user_boards': user_boards,
        'open_boards': open_boards,
    }
    return render(request, 'notices/home.html', context)

@login_required
def create_board(request):
    """Page for creating new boards."""
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user
            board.save()
            return redirect('home')
    else:
        form = BoardForm()
    return render(request, 'notices/create_board.html', {'form': form})

@login_required
@require_authorization
def view_board(request, board):
    """Detailed view for a single board and its notices."""
    notices = board.notices.all()
    return render(request, 'notices/view_board.html', {'board': board, 'notices': notices})

@login_required
@require_authorization
def create_notice(request, board):
    """Page for creating new notices."""
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.board = board
            notice.save()
            return redirect(view_board, pk=board.pk)
    else:
        form = NoticeForm()
    return render(request, 'notices/create_notice.html', {'form': form, 'board': board})

@login_required
@require_ownership
def whitelist_user(request, board):
    """Handles the whitelisting of new users."""
    if request.method == 'POST':
        username = request.POST.get('username')
        user = get_object_or_404(User, username=username)
        board.users.add(user)
        return redirect('view_board', pk=board.pk)
    return redirect('view_board', pk=board.pk)

@login_required
@require_ownership
def turn_public(request, board):
    """Turns a private board into a public one."""
    if request.method == 'POST':
        if request.POST.get('verification') == 'public':
            board.is_private = False
            board.save()
        return redirect('view_board', pk=board.pk)
    return redirect('view_board', pk=board.pk)

@login_required
@require_ownership
def turn_private(request, board):
    """Turns a public board into a private one."""
    if request.method == 'POST':
        if request.POST.get('verification') == 'private':
            board.is_private = True
            board.save()
        return redirect('view_board', pk=board.pk)
    return redirect('view_board', pk=board.pk)