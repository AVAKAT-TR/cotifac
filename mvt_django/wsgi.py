import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mvt_django.settings')
application = get_wsgi_application()

# --- Auto aplicar migraciones en Render ---
try:
    from django.core.management import call_command
    call_command("migrate", interactive=False)
    print("✅ Migraciones aplicadas automáticamente en Render.")
except Exception as e:
    print(f"⚠️ Error aplicando migraciones automáticamente: {e}")

# --- Auto crear superusuario si no existe ---
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()

    admin_username = "admin"
    admin_email = "pablotr54k1@gmail.com"
    admin_password = "PJTR"  # 🔐 puedes cambiarlo

    if not User.objects.filter(username=admin_username).exists():
        User.objects.create_superuser(
            username=admin_username,
            email=admin_email,
            password=admin_password
        )
        print(f"✅ Superusuario '{admin_username}' creado automáticamente.")
    else:
        print(f"ℹ️ Superusuario '{admin_username}' ya existe.")
except Exception as e:
    print(f"⚠️ Error creando superusuario automáticamente: {e}")
