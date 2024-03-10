from django.views.generic.base import View, TemplateResponseMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout 
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from .forms import RegistrationForm


class UserLoginView(LoginView):
	template_name = 'users/login.html'


class UserLogout(LoginRequiredMixin, View):
    
    def post(self, request):
        logout(request)
        return redirect('articles:list')


class RegistrationView(TemplateResponseMixin, View):
	template_name = 'users/registration.html'

	def get(self, request):
		form = RegistrationForm()
		context = {
			'form': form
		}
		return self.render_to_response(context)

	def post(self, request):
		form = RegistrationForm(data=request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.set_password(form.cleaned_data['password'])
			user.save()
			login(request, user)
			return redirect('articles:list')
		context = {
			'form': form
		}
		return self.render_to_response(context)
