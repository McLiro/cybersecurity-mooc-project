from functools import wraps
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Board

def require_ownership(view_func):
    """Only allow the board's owner to access the view."""
    @wraps(view_func)
    def wrapper(request, pk, *args, **kwargs):
        board = get_object_or_404(Board, pk=pk)
        if board.owner != request.user:
            messages.error(request, "You don't own this board.")
            return redirect('home')
        return view_func(request, board, *args, **kwargs)
    return wrapper

def require_authorization(view_func):
    """Only allow whitelisted users to access the view."""
    @wraps(view_func)
    def wrapper(request, pk, *args, **kwargs):
        board = get_object_or_404(Board, pk=pk)
        if board.owner == request.user:
            return view_func(request, board, *args, **kwargs)
        if not board.is_private:
            return view_func(request, board, *args, **kwargs)
        if request.user in board.users.all():
            return view_func(request, board, *args, **kwargs)
        return redirect('home')
    return wrapper
