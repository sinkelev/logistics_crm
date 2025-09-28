from django import forms
from .models import User

class DriverForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "phone", "email"]
        labels = {
            "username": "Логин",
            "first_name": "Имя",
            "last_name": "Фамилия",
            "phone": "Телефон",
            "email": "Email",
        }

    def save(self, commit=True):
        driver = super().save(commit=False)
        driver.role = "driver"
        if commit:
            driver.set_password(User.objects.make_random_password())
            driver.save()
        return driver