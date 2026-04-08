"""
Django 4.2 + Python 3.14 Compatibility Fixes
This module applies necessary patches for compatibility between Django 4.2 and Python 3.14.
Must be imported as early as possible.
"""

import sys
import copy as copy_module

def apply_python314_django42_fixes():
    """Apply all necessary fixes for Python 3.14 + Django 4.2 compatibility."""

    if sys.version_info < (3, 14):
        # No fixes needed for Python < 3.14
        return

    try:
        # Fix 1: Patch the copy module's _reconstruct function
        # Django's Context.__copy__ fails because super().__copy__() doesn't
        # properly handle Context's dicts attribute in Python 3.14

        from django.template.context import Context

        # Store the original __copy__ method
        _original_context_copy = Context.__copy__

        def _patched_context_copy(self):
            """Patched Context.__copy__ for Python 3.14 compatibility."""
            try:
                # Try the original method first
                return _original_context_copy(self)
            except (AttributeError, TypeError):
                # Fallback: manually copy the context
                from copy import copy as copy_single
                duplicate = self.__class__.__new__(self.__class__)
                duplicate.dicts = copy_single(self.dicts)
                return duplicate

        # Apply the patch
        Context.__copy__ = _patched_context_copy

        # Fix 2: Patch the copy.deepcopy function to handle Context better
        _original_deepcopy = copy_module.deepcopy

        def _patched_deepcopy(x, memo=None, _nil=[]):
            """Patched deepcopy that handles Django Context in Python 3.14."""
            if isinstance(x, Context):
                # For Context objects, do shallow copy of dicts list
                if memo is None:
                    memo = {}

                from copy import deepcopy as orig_deepcopy
                duplicate = x.__copy__()

                # Deepcopy the dicts contents
                duplicate.dicts = [orig_deepcopy(d, memo) for d in x.dicts]
                memo[id(x)] = duplicate
                return duplicate
            else:
                # Use original deepcopy for everything else
                return _original_deepcopy(x, memo, _nil)

        copy_module.deepcopy = _patched_deepcopy

        print("[PATCH] Applied Django 4.2 + Python 3.14 compatibility fixes")

    except Exception as e:
        print(f"[WARNING] Could not apply all compatibility fixes: {e}")
        print(f"[WARNING] Attempting partial fix...")

        try:
            from django.template.context import Context

            def _context_copy_fallback(self):
                """Fallback context copy that avoids problematic super() call."""
                duplicate = self.__class__.__new__(self.__class__)
                duplicate.dicts = list(self.dicts)
                return duplicate

            Context.__copy__ = _context_copy_fallback
            print("[PATCH] Applied fallback Context.__copy__ fix")
        except Exception as e2:
            print(f"[ERROR] Fallback fix also failed: {e2}")


# Apply fixes immediately when module is imported
apply_python314_django42_fixes()
