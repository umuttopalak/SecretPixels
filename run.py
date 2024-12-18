from alembic import command
from alembic.config import Config as AlembicConfig

from app import app


def run_migrations():
    alembic_cfg = AlembicConfig("alembic.ini")
    command.upgrade(alembic_cfg, "head")

if __name__ == '__main__':
    run_migrations()
    debug = app.config.get("DEBUG", False)
    app.run(host='0.0.0.0', debug=debug)