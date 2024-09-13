# cuentas/context_processors.py
def user_role(request):
    if request.user.is_authenticated:
        return {'myRole': request.user.role}
    return {'myRole': None}