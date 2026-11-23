from django.shortcuts import redirect, render

from .forms import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            return redirect('register_done')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def register_done(request):
    return render(request, 'registration/register_done.html')