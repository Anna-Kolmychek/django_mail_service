from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import inlineformset_factory
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from mailings.forms import MailingForm, ClientForm
from mailings.models import Mailing, Client


class MailingListView(ListView):
    model = Mailing

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(owner=self.request.user).all()
        else:
            queryset = Mailing.objects.none()
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
        return reverse('mailings:update', args=(self.object.pk,))

    def test_func(self):
        pk = self.kwargs.get('pk')
        is_owner = Mailing.objects.get(pk=pk).owner == self.request.user
        return is_owner

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ClientFormest = inlineformset_factory(Mailing, Client, form=ClientForm, can_delete=True, extra=1)
        if self.request.method == 'POST':
            formset = ClientFormest(self.request.POST, instance=self.object)
        else:
            formset = ClientFormest(instance=self.object)

        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


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
