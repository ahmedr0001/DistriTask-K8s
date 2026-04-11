from celery import shared_task
from .models import Task
from django.utils import timezone

@shared_task
def check_deadlines():
    print('Checking deadlines for all tasks...')
    now = timezone.now()

    # Get tasks that are overdue but not marked as delayed
    tasks = Task.objects.filter(deadline_reached=False, deadline__lte=now)

    if not tasks.exists():
        print('No active task reach to deadline tasks found.')
        print('#'*50)
        print('#'*50)
        return

    # Loop through each overdue task and update its status
    for task in tasks:
        task.status = 'delayed'  # Update task status
        task.deadline_reached = True  # Mark deadline as reached
        task.save()  # Save changes to the database
        print(f"Task '{task.title}' deadline reached. Status updated to 'Delayed'.")

    print(f"{tasks.count()} tasks marked as 'Delayed'.")
