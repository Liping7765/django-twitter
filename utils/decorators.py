from rest_framework.response import Response
from rest_framework import status
from functools import wraps


def required_params(request_attr='query_params', params=None):
    """
    when we call @required_params(params=['some_param']),
    this 'required_params' function should return 'decorator' function，
    this argument of 'decorator' function is function 'view_func' which is wrapped by @required_params
    """

    if params is None:
        params = []

    def decorator(view_func):
        """
        wraps function will pass arguments to _wrapped_view,
        in this case, instance means 'self' in view_func
        """
        @wraps(view_func)
        def _wrapped_view(instance,request,*arg,**kwargs):
            data = getattr(request,request_attr)
            missing_params =[
                param
                for param in params
                if param not in data
            ]

            if missing_params:
                params_str = ','.join(missing_params)
                return Response({
                    'message': u'missing {} in request'.format(params_str),
                    'success': False,
                }, status=status.HTTP_400_BAD_REQUEST)

            # once it passed the params requirements, call view_func
            return view_func(instance,request,*arg,**kwargs)
        return _wrapped_view
    return decorator