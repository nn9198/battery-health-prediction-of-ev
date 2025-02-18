from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import logout as auth_logout
import numpy as np
import joblib
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm





def home(request):
    return render(request, 'users/home.html')

@login_required(login_url='users-register')


def index(request):
    return render(request, 'app/index.html')

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality

class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})

from .forms import UserPredictDataForm
from .models import UserPredictModel

Model1 = joblib.load('C:/Users/chait/Music/ITPML36 DONE/Deployment/users/EVBATTERY.pkl')
def model(request):
    if request.method == "POST":
        form = UserPredictDataForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print("Form data:", data)  # Debug: Check the form data

            int_features = [
                data['Current'],
                data['Voltage'],
                data['Speed'],
                data['Temperature'],
                data['Range'],
                data['SOC'],
    
            ]
            print("Int features:", int_features)  # Debug: Check the features

            final_features = np.array(int_features, dtype=object)
            print("Final features:", final_features)  # Debug: Check the final features array

            prediction = Model1.predict([final_features])
            output = prediction[0]
            print("Prediction output:", output)  # Debug: Check the prediction output

            UserPredictModel1 = UserPredictModel(
                Current=data['Current'],
                Voltage=data['Voltage'],
                Speed=data['Speed'],
                Temperature=data['Temperature'],
                Range=data['Range'],
                SOC=data['SOC'],
                Label=prediction
            )
            UserPredictModel1.save()

            categories = ['Current', 'Voltage', 'Speed', 'Temperature', 'Range', 'SOC','Remaining_range']
            a = int_features + [output]

            plt.figure(figsize=(8, 6))
            sns.lineplot(x=categories, y=a, marker='o', color='red')

            plt.xlabel('Categories')
            plt.ylabel('Values')
            plt.title(f"['Battery Prediction'] : {a}")

            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)

            plot_base64 = base64.b64encode(buffer.read()).decode('utf-8')

            return render(request, 'App/result.html', {"prediction_text": f'The Battery Remaining Usage Prediction is {output}', 'plot_base64': plot_base64})
        else:
            print("Form is not valid")  # Debug: Check if the form is not valid
            print("Form errors:", form.errors)  # Debug: Print form errors
    else:
        form = UserPredictDataForm()
    return render(request, 'App/model.html', {'form': form})







 


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO
from django.shortcuts import render




def Basic_report(request):
    return render(request,'app/report.html')




def model_db(request):
    data = UserPredictModel.objects.all()
    return render(request, 'app/model_db.html', {'data': data})





def logout_view(request):  
    auth_logout(request)
    return redirect('/')


