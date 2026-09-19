"""Strict JSON encoding for result files: numpy scalars become numbers, anything else fails.

Replaces `default=str`, which silently turned unexpected objects into strings that the
aggregation then skipped or mis-read. Moves into odca.experiment at N6.
"""


def numpy_default(value):
    """`json.dump(..., default=numpy_default)`: convert numpy scalars, reject everything else.

    Args:
        value: the object json could not encode.
    """
    if hasattr(value, "item") and callable(value.item):
        return value.item()
    raise TypeError(f"not JSON-serialisable in a result file: {type(value).__name__}")
