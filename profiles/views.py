from django.shortcuts import render
from profiles.models import Profile
from profiles.forms import ProfileForm
from django.contrib.auth.decorators import login_required


@login_required
def my_profile(request):
    profile = Profile.objects.get(user=request.user)
    profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    success = False

    if profile_form.is_valid():
        profile_form.save()
        success = True

    context = {
        'profile': profile,
        'profile_form': profile_form,
        'success': success,
    }

    return render(request, 'profiles/my_profile.html', context)