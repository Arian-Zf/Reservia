from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

INPUT = (
    "w-full rounded-xl border border-rose-100 bg-white/80 px-4 py-3 text-plum-900 "
    "placeholder:text-plum-900/40 outline-none transition focus:border-rose-400 focus:ring-4 focus:ring-rose-100"
)


class StyledAuthForm(AuthenticationForm):
    error_messages = {
        "invalid_login": "نام کاربری یا رمز عبور اشتباه است.",
        "inactive": "این حساب غیرفعال است.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "نام کاربری"
        self.fields["password"].label = "رمز عبور"
        for f in self.fields.values():
            f.widget.attrs["class"] = INPUT
        self.fields["username"].widget.attrs.update(autocomplete="username", autofocus=True)
        self.fields["password"].widget.attrs["autocomplete"] = "current-password"


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label="نام", max_length=50)

    class Meta:
        model = get_user_model()
        fields = ("first_name", "username")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "نام کاربری"
        self.fields["username"].help_text = ""
        self.fields["password1"].label = "رمز عبور"
        self.fields["password2"].label = "تکرار رمز عبور"
        self.fields["password2"].help_text = ""
        for f in self.fields.values():
            f.widget.attrs["class"] = INPUT
        self.fields["first_name"].widget.attrs.update(autocomplete="given-name", autofocus=True)
        self.fields["username"].widget.attrs["autocomplete"] = "username"
        self.fields["password1"].widget.attrs["autocomplete"] = "new-password"
        self.fields["password2"].widget.attrs["autocomplete"] = "new-password"
