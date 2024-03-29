from django.db import models


class Todo(models.Model):
    title = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title