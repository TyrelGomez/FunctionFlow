def skipToFunction(condition, functionToSkipTo):
    """A decorator that skips to a specified function if a condition is met."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if condition():
                print(f"[FUNCTION-FLOW] Skipping to {functionToSkipTo.__name__} due to condition.")
                return functionToSkipTo(*args, **kwargs)
            return func(*args, **kwargs)
        return wrapper
    return decorator