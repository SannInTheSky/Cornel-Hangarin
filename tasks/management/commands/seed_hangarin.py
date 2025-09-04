from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random

from tasks.models import Task, SubTask, Note, Category, Priority


class Command(BaseCommand):
    help = "Seed Hangarin with fake data (Tasks, SubTasks, Notes)"

    def add_arguments(self, parser):
        parser.add_argument("--tasks", type=int, default=10, help="Number of tasks to create")

    def handle(self, *args, **options):
        fake = Faker()
        categories = list(Category.objects.all())
        priorities = list(Priority.objects.all())

        if not categories or not priorities:
            self.stdout.write(self.style.ERROR("⚠️ Please add Categories and Priorities first in Admin."))
            return

        tasks_to_create = []
        for _ in range(options["tasks"]):
            deadline = timezone.make_aware(fake.date_time_this_month())
            t = Task(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
                deadline=deadline,
                priority=random.choice(priorities),
                category=random.choice(categories),
            )
            tasks_to_create.append(t)

        created_tasks = Task.objects.bulk_create(tasks_to_create)

        # SubTasks and Notes
        subtasks = []
        notes = []
        for task in created_tasks:
            for _ in range(random.randint(1, 3)):
                subtasks.append(SubTask(
                    parent_task=task,
                    title=fake.sentence(nb_words=5),
                    status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
                ))
            for _ in range(random.randint(0, 2)):
                notes.append(Note(
                    task=task,
                    content=fake.paragraph(nb_sentences=2),
                ))

        SubTask.objects.bulk_create(subtasks)
        Note.objects.bulk_create(notes)

        self.stdout.write(self.style.SUCCESS(
            f"✅ Seeded {len(created_tasks)} tasks, {len(subtasks)} subtasks, {len(notes)} notes."
        ))
