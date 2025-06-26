# p4m/core/utils.py

def close_to(a, b, eps=1e-12):
    """Return True if a and b are within eps under their norm()."""
    try:
        return (a - b).norm() < eps
    except AttributeError:
        # Fallback to built-in abs if .norm() is not available
        return abs(a - b) < eps
