# org-repositorio-
Repositorio organización

## Bases de datos

La aplicación guarda el catálogo `ProductoRopa` en la base de datos elegida en el selector de la página. SQLite está disponible localmente por defecto. PostgreSQL y MySQL solo aparecen en el selector cuando su URL de conexión está configurada.

Copia `.env.example` a `.env` en la raíz del repositorio y reemplaza el valor de ejemplo por la URL de conexión de Neon. También se aceptan las variables `NEON_DATABASE_URL` y `DATABASE_URL` si tu proveedor ya las utiliza.

```env
DATABASE_POSTGRES_URL=postgresql://usuario:clave@servidor/base_de_datos?sslmode=require
DATABASE_MYSQL_URL=mysql://usuario:clave@servidor:3306/base_de_datos
```

Configura únicamente el motor que necesites y reemplaza los valores de ejemplo por los datos de tu proveedor. No publiques `.env` ni incluyas credenciales en el repositorio.

Antes de guardar registros, crea las tablas en cada motor configurado desde `src`:

```powershell
py manage.py migrate
py manage.py migrate --database=postgres
py manage.py migrate --database=mysql
```

Ejecuta solo el comando del motor que configuraste. Para Neon, desde `src`, usa `python manage.py migrate --database=postgres`. Si `postgres` no aparece entre los aliases, confirma que `.env` esté en la raíz, que la variable tenga una URL `postgresql://` válida y reinicia el servidor. Cada base mantiene sus propias tablas y registros; migrar crea la estructura, pero no copia los datos guardados en otro motor.
