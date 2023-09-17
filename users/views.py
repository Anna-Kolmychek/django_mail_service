import secrets
import string

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:register_begin')

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.is_active = False
        new_user.register_key = generate_random_str(8)
        new_user.save()
        send_mail(
            subject='Регистрация на почтовом сервисе',
            message='Вы начали регистрацию на почтовом сервисе.\n'
                    'Чтобы закончить регистрацию, пройдите по ссылке:\n'
                    f'{self.request.get_host()}/users/register_end?register_key={new_user.register_key}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email],
        )
        return super().form_valid(form)


def register_begin(request):
    return render(request, 'users/register_begin.html')


def register_end(request):
    register_key = request.GET.get('register_key')
    user = User.objects.filter(register_key=register_key).first()
    if user:
        user.is_active = True
        user.save()
        context = {'is_user_exist': True}
    else:
        context = {'is_user_exist': False}

    return render(request, 'users/register_end.html', context=context)


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def generate_random_str(len_str=8):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(secrets.choice(
        letters_and_digits) for _ in range(len_str))


