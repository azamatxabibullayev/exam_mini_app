from django.contrib.auth import get_user_model

User = get_user_model()


def get_full_name(backend, details, response, *args, **kwargs):
    full_name = details.get('fullname') or details.get('name') or ''
    if not full_name:
        first = details.get('first_name', '') or response.get('given_name', '')
        last = details.get('last_name', '') or response.get('family_name', '')
        full_name = f"{first} {last}".strip()
    details['full_name'] = full_name
    return {'details': details}


def assign_user_fields(backend, details, user=None, *args, **kwargs):
    if not user:
        return {}
    changed = False
    email = details.get('email')
    if email and not getattr(user, 'email', None):
        user.email = email
        changed = True
    full_name = details.get('full_name') or details.get('name')
    if full_name and getattr(user, 'full_name', '') != full_name:
        user.full_name = full_name
        changed = True
    if changed:
        user.save()
    return {'user': user}


def create_or_update_user(backend, details, response, uid=None, user=None, *args, **kwargs):
    if user:
        return {'user': user}

    email = details.get('email') or response.get('email')
    full_name = details.get('full_name') or response.get('name') or ''
    if not email:
        return {}

    try:
        user = User.objects.get(email=email)
        updated = False
        if full_name and getattr(user, 'full_name', '') != full_name:
            user.full_name = full_name
            updated = True
        if updated:
            user.save()
    except User.DoesNotExist:
        user = User.objects.create_user(email=email, password=None, full_name=full_name)
        user.set_unusable_password()
        user.save()

    return {'user': user}
