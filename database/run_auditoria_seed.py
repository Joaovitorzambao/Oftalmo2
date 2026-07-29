#!/usr/bin/env python3
"""
Executa o seed da tabela auditoria_acesso no PostgreSQL.

Uso na VM:
    python database/run_auditoria_seed.py

Ou diretamente com psql:
    psql -U postgres -d prontuario_oftalmo_prod -f database/seeds/001_auditoria_acesso.sql
"""
import sys
from pathlib import Path

try:
    import psycopg2
except ImportError:
    print("Instale psycopg2: pip install psycopg2-binary")
    sys.exit(1)

# Mesmas credenciais de app/auth.py
PG_CONFIG = {
    "user": "postgres",
    "password": "@GhrB$2024#",
    "database": "prontuario_oftalmo_prod",
    "host": "localhost",
    "port": 5432,
}

SEED_FILE = Path(__file__).parent / "seeds" / "001_auditoria_acesso.sql"


def main():
    if not SEED_FILE.exists():
        print(f"Arquivo não encontrado: {SEED_FILE}")
        sys.exit(1)

    sql = SEED_FILE.read_text(encoding="utf-8")
    print(f"Conectando em {PG_CONFIG['host']}:{PG_CONFIG['port']}/{PG_CONFIG['database']}...")

    conn = psycopg2.connect(**PG_CONFIG)
    conn.autocommit = True
    cursor = conn.cursor()

    try:
        cursor.execute(sql)
        print("Seed executado com sucesso!")
        print("Tabela: auditoria_acesso")
        print("Acesse: http://<seu-servidor>/auditoria")
    except Exception as e:
        print(f"Erro ao executar seed: {e}")
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()
