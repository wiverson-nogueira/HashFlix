from django.shortcuts import render, redirect, reverse
from .models import Filme, Usuario
from .forms import CriarContaForm, FormHomepage
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class Homepage(FormView):
    template_name = "homepage.html"
    form_class = FormHomepage

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('filme:homefilmes') # Redirecionamento para homefilmes [appname:url] -> filme/urls.py
        else:
            return super().get(request, *args, **kwargs) # Redirecionamento para o template_name = homepage

    def get_success_url(self):
        email = self.request.POST.get("email")
        usuarios = Usuario.objects.filter(email=email)
        if usuarios:
            return reverse('filme:login')
        else:
            return reverse('filme:criarconta')

class Homefilmes(LoginRequiredMixin, ListView):
    template_name = "homefilmes.html"
    model = Filme #object_list


class Detalhesfilme(LoginRequiredMixin, DetailView):
    template_name = "detalhesfilme.html"
    model = Filme #object

    def get(self, request, *args, **kwargs):
        filme = self.get_object()
        filme.visualizacoes += 1
        filme.save()
        usuario = request.user
        usuario.filmes_vistos.add(filme)
        return super().get(request, *args, **kwargs) # Redirecionamento para o template_name = detalhesfilme

    def get_context_data(self, **kwargs):
        context = super(Detalhesfilme, self).get_context_data(**kwargs)
        filmes_relacionados = Filme.objects.filter(categoria=self.get_object().categoria)[0:5]
        context["filmes_relacionados"] = filmes_relacionados
        return context


class Pesquisafilme(LoginRequiredMixin, ListView):
    template_name = "pesquisa.html"
    model = Filme

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            object_list = Filme.objects.filter(titulo__icontains=termo_pesquisa)
            return object_list
        else:
            return None

class Paginaperfil(LoginRequiredMixin, UpdateView):
    template_name = "editarperfil.html"
    model = Usuario
    fields = ['first_name', 'last_name', 'email']

    def get_success_url(self):
        return reverse('filme:homefilmes')

class Criarconta(FormView):
    template_name = "criarconta.html"
    form_class = CriarContaForm

    # Edita a função para após validação dos campos, salvar a alteração no BD
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    # Retorna um LINK como resposta, utilizar o REVERSE
    def get_success_url(self):
        return reverse('filme:login')

#FunctionBaseView - FBV

# def homepage(request):
#    return render(request, "homepage.html")

# def homefilmes(request):
#     context = {}
#     lista_filmes = Filme.objects.all()
#     context['lista_filmes'] = lista_filmes
#     return render(request, "homefilmes.html", context)