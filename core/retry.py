import time
from functools import wraps
from typing import Callable


def retry(
        retries: int = 3,
        delay: float = 1,
        backoff: float = 1,
        exceptions: tuple[type[Exception], ...] = (Exception,),
):
    """Generic retry decorator.

    retries:
        Total number of attempts.

    delay:
        Initial delay between attempts.

    backoff:
        Multiplier for delay after each failure.

        backoff=1 -> 1s, 1s, 1s
        backoff=2 -> 1s, 2s, 4s
    """

    def decorator(func: Callable):

        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay

            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as error:
                    if attempt == retries:
                        raise

                    instance = args[0] if args else None

                    if instance and hasattr(instance, "_log"):
                        instance._log(
                            f"[RETRY] {func.__name__} "
                            f"attempt {attempt}/{retries} "
                            f"failed → {error}"
                        )

                    time.sleep(current_delay)
                    current_delay *= backoff

        return wrapper

    return decorator
