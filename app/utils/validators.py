import re

def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    if re.match(pattern, email):
        return True, ""
    return False, "El correo electrónico no es válido."

def validate_password(password):
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres."
    if not re.search(r"[A-Z]", password):
        return False, "La contraseña debe incluir al menos una letra mayúscula."
    if not re.search(r"[a-z]", password):
        return False, "La contraseña debe incluir al menos una letra minúscula."
    if not re.search(r"[0-9]", password):
        return False, "La contraseña debe incluir al menos un número."
    return True, ""
