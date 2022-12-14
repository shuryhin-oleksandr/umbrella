from datetime import date

from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

from umbrella.contracts.models import Contract
from umbrella.core.models import CustomModel
from umbrella.tasks.choices import (
    ProgressChoices,
    RepeatsChoices,
    PeriodChoices,
    BeforeAfterChoices,
    StatusChoices,
)

User = get_user_model()


class Task(CustomModel):
    EDITABLE_FIELDS = [
        "title",
        "assignees",
        "due_date",
        "progress",
        "notes",
        "reminder_number",
        "reminder_period",
        "reminder_before_or_after",
        "reminder_repeats",
        "reminder_until",
    ]

    # Common data
    title = models.CharField(max_length=500, validators=[MinLengthValidator(5)])
    assignees = models.ManyToManyField(User, related_name="tasks", blank=True)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    progress = models.CharField(
        max_length=32,
        choices=ProgressChoices.choices,
        default=ProgressChoices.NOT_STARTED,
    )
    notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=32, choices=StatusChoices.choices, default=StatusChoices.OVERDUE
    )

    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name="tasks")
    # TODO: Add Clause Types and convert current field to ChoiceField
    contract_clause_type = models.TextField()
    contract_business_intelligence_type = models.TextField()
    link_to_contract_text = models.TextField()

    reminder_number = models.PositiveIntegerField(default=1)
    reminder_period = models.CharField(
        max_length=32, choices=PeriodChoices.choices, default=PeriodChoices.DAYS
    )
    reminder_before_or_after = models.CharField(
        max_length=32, choices=BeforeAfterChoices.choices, default=BeforeAfterChoices.BEFORE
    )
    reminder_repeats = models.CharField(
        max_length=32, choices=RepeatsChoices.choices, default=RepeatsChoices.NEVER
    )
    reminder_until = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.status = self.get_status()
        super().save(*args, **kwargs)

    def get_status(self):
        if not self.due_date:
            return StatusChoices.OVERDUE
        elif not self.due_date and self.progress == ProgressChoices.COMPLETED:
            return StatusChoices.DONE

        date_diff = self.now_and_due_date_diff()
        if date_diff < 0 and self.progress == ProgressChoices.COMPLETED:
            return StatusChoices.DONE
        elif date_diff < 0:
            return StatusChoices.OVERDUE
        elif date_diff == 0:
            return StatusChoices.DUE_TODAY
        elif date_diff <= 7:
            return StatusChoices.DUE_IN_A_WEEK
        elif date_diff <= 31:
            return StatusChoices.DUE_IN_A_MONTH
        elif date_diff > 31:
            return StatusChoices.NOT_DUE_SOON

    def now_and_due_date_diff(self):
        today = date.today()
        date_diff = self.due_date - today
        return date_diff.days


class Subtask(CustomModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="subtasks")
    title = models.CharField(max_length=128)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Comment(CustomModel):
    message = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return self.message
