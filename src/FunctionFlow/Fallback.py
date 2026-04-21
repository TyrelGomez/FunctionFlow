def fallback(fallback_func):
    """A decorator that provides a fallback function to execute if the main function raises an exception."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"[FUNCTION-FLOW] An error occurred: {e}. Executing fallback function.")
                return fallback_func(*args, **kwargs)
        return wrapper
    return decorator