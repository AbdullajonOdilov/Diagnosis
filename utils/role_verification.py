from fastapi import HTTPException


def role_verification(user, function):
    # allowed_functions_for_admins = []

    if user.role in ["admin", "super_admin"]:
        return True

    raise HTTPException(status_code=401, detail='Sizga ruhsat berilmagan!')

