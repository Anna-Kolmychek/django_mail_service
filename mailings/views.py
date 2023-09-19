from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from mailings.forms import MailingForm
from mailings.models import Mailing


class MailingListView(ListView):
    model = Mailing

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user).all()
        return queryset


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm

    def get_success_url(self):
        return reverse('mailings:detail', args=(self.object.pk,))

    def form_valid(self, form):
        new_mailing = form.save(commit=False)
        new_mailing.owner = self.request.user
        new_mailing.save()

        return super().form_valid(form)


class MailingUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm

    def get_success_url(self):
        return reverse('mailings:detail', args=(self.object.pk,))

    def test_func(self):
        pk = self.kwargs.get('pk')
        is_owner = Mailing.objects.get(pk=pk).owner == self.request.user
        return is_owner


class MailingDetailView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    model = Mailing

    def test_func(self):
        pk = self.kwargs.get('pk')
        is_owner = Mailing.objects.get(pk=pk).owner == self.request.user
        return is_owner


class MailingDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailings:list')

    def test_func(self):
        pk = self.kwargs.get('pk')
        is_owner = Mailing.objects.get(pk=pk).owner == self.request.user
        return is_owner
