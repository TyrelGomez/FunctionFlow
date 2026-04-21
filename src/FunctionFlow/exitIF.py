def exitFunctionIf(condition):
    """A decorator that exits the function if a specified condition is met."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if condition():
                print("[FUNCTION-FLOW] Exiting function due to condition.")
                return
            return func(*args, **kwargs)
        return wrapper
    return decorator