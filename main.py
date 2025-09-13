from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class City(models.Model):
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Department(models.Model):
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

def new():
    print("hello!")
    
class Branch(models.Model):
    title = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='branches')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.city})"


class Vacancy(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='vacancies')
    branches = models.ManyToManyField(Branch, related_name='vacancies')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Button(models.Model):
    BUTTON_TYPES = [
        ("standard", "Standard Button"),
        ("inline", "Inline Button"),
        ("url", "URL Button"),
    ]
    button_type = models.CharField(choices=BUTTON_TYPES, max_length=100, default="standard")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey("content_type", "object_id")
    label = models.CharField(max_length=255)
    callback_data = models.CharField(max_length=64, blank=True)
    url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.label


class AdditionalButton(models.Model):
    back_button = models.CharField(max_length=255, default="Назад")
    extra_button = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.back_button} + {self.extra_button}"
class Keyboard(models.Model):
    title = models.CharField(max_length=255)
    buttons = models.ManyToManyField(Button)
    additional_buttons = models.ForeignKey(AdditionalButton, on_delete=models.CASCADE, max_length=255)
    row = models.PositiveIntegerField(default=0)
    column = models.PositiveIntegerField(default=0)
    is_inline = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Step(models.Model):
    step_num = models.CharField(max_length=255)
    image = models.FileField(upload_to="files/")
    message = models.TextField(blank=True, null=True)
    keyboard = models.ForeignKey(Keyboard,  null=True, blank=True, on_delete=models.CASCADE)
    next_step = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    is_entry_point = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.step_num

