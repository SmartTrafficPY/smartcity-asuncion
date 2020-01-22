from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from psycopg2 import connect, sql


def get_connection(host, port, database, user, password):
    return connect(host=host, port=port, dbname=database, user=user, password=password)


def initialize_db(
    host, port, database, user, password, admin_database=None, admin_user=None, admin_password=None, region=None
):
    admin_database = admin_database or "postgres"
    admin_user = admin_user or "postgres"
    if admin_password is None:
        admin_password = admin_password or input(f"password for admin user '{admin_user}': ")

    with get_connection(host, port, admin_database, admin_user, admin_password) as connection:
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(
                sql.SQL("SELECT 1 FROM pg_catalog.pg_database WHERE datname = {}").format(sql.Literal(database))
            )
            exists = cursor.fetchone()
            if not exists:
                cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database)))

            cursor.execute(sql.SQL("SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = {}").format(sql.Literal(user)))
            exists = cursor.fetchone()
            if not exists:
                cursor.execute(
                    sql.SQL("CREATE ROLE {u} LOGIN PASSWORD {p}").format(
                        u=sql.Identifier(user), p=sql.Literal(password)
                    )
                )
            else:
                cursor.execute(
                    sql.SQL("ALTER ROLE {u} WITH PASSWORD {p};\n" "ALTER ROLE {u} WITH LOGIN").format(
                        u=sql.Identifier(user), p=sql.Literal(password)
                    )
                )

            cursor.execute(
                sql.SQL("ALTER DATABASE {d} OWNER TO {u}").format(d=sql.Identifier(database), u=sql.Identifier(user))
            )
            cursor.execute(
                sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {d} TO {u}").format(
                    d=sql.Identifier(database), u=sql.Identifier(user)
                )
            )
        connection.commit()

    with get_connection(host, port, database, admin_user, admin_password) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql.SQL("CREATE EXTENSION IF NOT EXISTS postgis"))
        connection.commit()


class Command(BaseCommand):
    help = "Create database and role, install postgis extensions"

    # def add_arguments(self, parser):
    #     parser.add_argument('--destroy', default=None)

    def handle(self, *args, **options):
        engine = settings.DATABASES["default"]["ENGINE"]
        database = settings.DATABASES["default"]["NAME"]

        if engine != "django.contrib.gis.db.backends.postgis":
            raise CommandError(f"Don't know how to createdb for engine '{engine}'")

        initialize_db(
            settings.DATABASES["default"]["HOST"],
            settings.DATABASES["default"]["PORT"],
            database,
            settings.DATABASES["default"]["USER"],
            settings.DATABASES["default"].get("PASSWORD"),
        )

        self.stdout.write(self.style.SUCCESS(f"Successfully created database {database}"))
