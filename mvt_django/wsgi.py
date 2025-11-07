import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mvt_django.settings')
application = get_wsgi_application()

# --- Ejecutar migraciones automáticamente en Render ---
try:
    from django.core.management import call_command
    call_command("migrate", interactive=False)
    print("✅ Migraciones aplicadas automáticamente en Render.")
except Exception as e:
    print(f"⚠️ Error aplicando migraciones automáticamente: {e}")

# --- Crear superusuario automáticamente (solo si no existe) ---
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()

    admin_username = "admin"
    admin_email = "admin@example.com"
    admin_password = "Admin2024"

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

# --- Cargar datos iniciales (fixtures/productos.json o fixtures/data.json) ---
try:
    from django.core.management import call_command
    # Si tu archivo se llama data.json, usa eso.
    call_command('loaddata', 'COTIFAC/fixtures/productos_utf8.json')
    print("✅ Datos iniciales cargados desde fixtures/data.json.")
except Exception as e:
    print(f"⚠️ Error cargando fixtures: {e}")
