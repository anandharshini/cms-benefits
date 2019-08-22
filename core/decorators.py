from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings

def is_broker(self):
    print(self.user_type, 'inside')
    if str(self.user_type) == 'Broker':
        return True
    else:
        return False
rec_login_required = user_passes_test(lambda u: True if u.is_broker else False, login_url=settings.PREFIX_URL)
def broker_login_required(view_func):
    print('inside dec 1', view_func)
    decorated_view_func = login_required(rec_login_required(view_func), login_url=settings.PREFIX_URL)
    print('inside dec 2', view_func)
    return decorated_view_func

# def user_is_entry_author(function):
#     def wrap(request, *args, **kwargs):
#         entry = Entry.objects.get(pk=kwargs['entry_id'])
#         if entry.created_by == request.user:
#             return function(request, *args, **kwargs)
#         else:
#             raise PermissionDenied
#     wrap.__doc__ = function.__doc__
#     wrap.__name__ = function.__name__
#     return wrap    