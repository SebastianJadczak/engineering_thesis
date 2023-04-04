from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from main.forms.register_form import RegisterFormNewUser
from main.models import CategoryProduct, ProductShop


class MainView(ListView):
    template_name = 'index.html'
    model = CategoryProduct

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_product'] = self.model.get_all_category()
        context['all_products_with_promotion'] = ProductShop.get_all_products_with_promotion()
        return context


class SpecificProductCategory(DetailView):
    template_name = 'detail_category.html'
    model = CategoryProduct

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.kwargs['slug'])
        context['category_product'] = CategoryProduct.objects.all()
        context['product_with_category'] = self.model.get_category_after_slug(slug=self.kwargs['slug'])
        return context


class RegisterUserFormViews(View):
    """Rejestracja użytkownika. """
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
