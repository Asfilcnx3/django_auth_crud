from django.shortcuts import redirect
from functools import wraps

def logout_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('create_task')
        return view_func(request, *args, **kwargs)
    return _wrapped_view