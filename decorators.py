# decorators.py
from flask import session, redirect, url_for, flash
from functools import wraps

def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if session.get('role') != role:
                flash('You do not have permission to access this page.')
                return redirect(url_for('login'))
            return func(*args, **kwargs)
        return wrapper
    return decorator