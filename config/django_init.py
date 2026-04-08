"""
Django 4.2 + Python 3.14 Compatibility Fixes
This module applies necessary patches for compatibility between Django 4.2 and Python 3.14.
Must be imported as early as possible.
"""

import sys

def apply_python314_django42_fixes():
    """Apply all necessary fixes for Python 3.14 + Django 4.2 compatibility."""

    if sys.version_info < (3, 14):
        # No fixes needed for Python < 3.14
        return

    print(f"[DJANGO_INIT] Python version detected: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print(f"[DJANGO_INIT] Applying Python 3.14 + Django 4.2 compatibility patches...")

    try:
        # This is the ROOT CAUSE of the issue:
        # In Python 3.14, copy.copy() fails on Django Context objects because:
        # 1. Context.__copy__() tries to call super().__copy__()
        # 2. super().__copy__() calls object.__copy__()
        # 3. object doesn't have __copy__, so it tries __dict__
        # 4. super() proxy objects can't have __dict__ modified
        
        # SOLUTION: Completely replace Context.__copy__ with a working version
        
        from django.template.context import Context
        from copy import copy as copy_obj
        
        def new_context_copy(self):
            """
            Working Context.__copy__ for Python 3.14.
            Directly creates a duplicate without calling super().
            """
            # Create new instance WITHOUT calling __init__
            duplicate = self.__class__.__new__(self.__class__)
            # Copy the dicts list
            duplicate.dicts = list(self.dicts)
            return duplicate
        
        # Replace the method
        Context.__copy__ = new_context_copy
        print("[DJANGO_INIT] ✓ Patched Context.__copy__ successfully")
        
        # Also patch copy.copy to handle Context safely
        import copy as copy_module
        _original_copy = copy_module.copy
        
        def patched_copy(x):
            """Patched copy that handles Django Context specially."""
            if isinstance(x, Context):
                return new_context_copy(x)
            else:
                return _original_copy(x)
        
        copy_module.copy = patched_copy
        print("[DJANGO_INIT] ✓ Patched copy.copy successfully")
        
    except Exception as e:
        print(f"[DJANGO_INIT] ✗ ERROR: {e}")
        import traceback
        traceback.print_exc()


# Apply fixes immediately on import
apply_python314_django42_fixes()
print("[DJANGO_INIT] All patches applied successfully!")

