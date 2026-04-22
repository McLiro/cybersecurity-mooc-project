from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from .models import Board
from .forms import BoardForm, NoticeForm

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
    """Home page showing user's boards and public boards."""
    user_boards = Board.objects.filter(owner=request.user)
    public_boards = Board.objects.filter(is_private=False).exclude(owner=request.user)
    context = {
        'user_boards': user_boards,
        'public_boards': public_boards,
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
def view_board(request, pk):
    """Detailed view for a single board and its notices."""
    board = get_object_or_404(Board, pk=pk)
    if board.is_private:
        if board.owner != request.user and request.user not in board.users.all():
            return redirect('home')
    notices = board.notices.all()
    return render(request, 'notices/view_board.html', {'board': board, 'notices': notices})

@login_required
def create_notice(request, pk):
    """Page for creating new notices."""
    board = get_object_or_404(Board, pk=pk)

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