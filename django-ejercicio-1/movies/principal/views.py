from django.shortcuts import render, redirect
from principal.models import Usuario
from principal.forms import UserForm

# Create your views here.
def user_list(request):
    users = Usuario.objects.all()
    return render(request, "principal/user_list.html", {"users": users})

def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/user_list/')
    else:
        form = UserForm()

    return render(request, 'principal/register_user.html', {'form': form})