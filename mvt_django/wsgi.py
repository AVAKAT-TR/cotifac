import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mvt_django.settings')
application = get_wsgi_application()

# --- FIX: Aplicar migraciones automáticamente en Render ---
try:
    from django.core.management import call_command
    call_command("migrate", interactive=False)
    print("✅ Migraciones aplicadas automáticamente en Render.")
except Exception as e:
    print(f"⚠️ Error aplicando migraciones automáticamente: {e}")
