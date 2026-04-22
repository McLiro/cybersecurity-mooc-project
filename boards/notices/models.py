from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Board(models.Model):
    name = models.CharField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards')
    users = models.ManyToManyField(User)
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (Owner: {self.owner.username}, Private: {self.is_private})"

class Notice(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='notices')
    title = models.CharField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (Board: {self.board.name})"
