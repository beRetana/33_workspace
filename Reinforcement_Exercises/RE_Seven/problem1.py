
def partially_call(function, **kwargs):
    def f(*n):
        function(*n, **kwargs)
    return f
