from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from main.forms.register_form import RegisterFormNewUser


class MainView(View):
    template_name = 'index.html'
    # model = Point

    def get(self, request, *args, **kwargs):
        # --------------------------------------
        # if (str(request.user) != 'AnonymousUser'):
        #     self.userRole = UserRole.objects.filter(user=request.user).first()
        # --------------------------------------
        # print(self.coordinates[0].country)
        return render(request, self.template_name)

    # todo: odblokować po dodaniu modeli i zamiany typu widoku na ListView
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # context['point_favorite'] = self.favorite_point
    #     # context['country'] = self.country
    #     # context['city'] = self.coordinates
    #     return context

class RegisterUserFormViews(View):
    """Rejestracja użytkownika"""
    form_class = RegisterFormNewUser
    template_name = 'registration/register.html'


    def get(self, request, *args, **kwargs):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('../')

        return render(request, self.template_name, {'form': form})