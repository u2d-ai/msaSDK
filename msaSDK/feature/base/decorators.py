
from functools import wraps

from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse

from msaSDK.feature.base.manager import MSAManager


def msa_switch_active(name, redirect_to=None, default=None, msa_manager=None):

    if not msa_manager:
        msa_manager = MSAManager()

    def deco_inner(func):

        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if msa_manager.active(name, request):
                return func(request, *args, **kwargs)
            elif redirect_to:
                return RedirectResponse(url=redirect_to)
            elif default:
                return RedirectResponse(url=redirect_to)
            else:
                raise HTTPException(status_code=404, detail='MSASwitch %s not active' % name)

        return wrapper

    return deco_inner