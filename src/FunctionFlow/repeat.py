def repeat(times):
    """A decorator that repeats the execution of a function a specified number of times."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                func(*args, **kwargs)
        return wrapper
    return decorator