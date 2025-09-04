from django.db import models

from django.utils import timezone

# 1) Base model (timestamped)
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # BaseModel requirement
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# 2) Category & Priority (with proper plural names)
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"  # PDF asks to refactor pluralization

    def __str__(self):
        return self.name

class Priority(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Priority"
        verbose_name_plural = "Priorities"

    def __str__(self):
        return self.name

# 3) Common status choices (enum)
STATUS_CHOICES = [
    ("Pending", "Pending"),
    ("In Progress", "In Progress"),
    ("Completed", "Completed"),
]

# 4) Task model
class Task(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")
    deadline = models.DateTimeField(null=True, blank=True)
    priority = models.ForeignKey(Priority, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

# 5) SubTask model
class SubTask(BaseModel):
    parent_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="subtasks")
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")

    def __str__(self):
        return self.title

# 6) Note model
class Note(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="notes")
    content = models.TextField()

    def __str__(self):
        return f"Note for {self.task.title} @ {timezone.localtime(self.created_at).strftime('%Y-%m-%d %H:%M')}"
# Create your models here.
