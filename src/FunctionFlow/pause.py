def pause(seconds):
    """A decorator that pauses the execution of a function for a specified number of seconds."""
    import time
    def decorator(func):
        def wrapper(*args, **kwargs):
            time.sleep(seconds)
            return func(*args, **kwargs)
        return wrapper
    return decorator