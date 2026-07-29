from datetime import datetime
from typing import Optional

from app.auth import get_db_connection


def obter_ip_cliente(request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    if request.client and request.client.host:
        return request.client.host
    return "desconhecido"


def obter_funcao_por_rota(path: str, metodo: str) -> str:
    path_lower = path.lower().rstrip("/") or "/"

    rotas_exatas = {
        "/": "Raiz",
        "/login": "Login",
        "/agenda": "Agenda",
        "/editar-exames": "Editar Exames",
        "/prontuario-especial": "Prontuário Especial",
        "/auditoria": "Auditoria",
    }
    if path_lower in rotas_exatas:
        return rotas_exatas[path_lower]

    prefixos = [
        ("/prontuario/", "Prontuário"),
        ("/api/prontuario", "API Prontuário"),
        ("/api/evolucao", "API Evolução"),
        ("/api/historico-paciente", "Histórico Paciente"),
        ("/api/exames", "API Exames"),
        ("/api/cirurgias", "API Cirurgias"),
        ("/gerar-pdf", "Geração PDF"),
        ("/salvar_rascunho", "Salvar Rascunho"),
        ("/salvar_liberar", "Salvar e Liberar"),
        ("/api/agenda", "API Agenda"),
        ("/get_agenda_data", "Dados Agenda"),
        ("/api/auditoria", "API Auditoria"),
    ]
    for prefixo, nome in prefixos:
        if path_lower.startswith(prefixo):
            if "/oculos" in path_lower:
                return "Óculos"
            if "/receituario" in path_lower:
                return "Receituário"
            if "/exames" in path_lower:
                return "Exames"
            if "/resumo" in path_lower:
                return "Resumo"
            return nome

    if path_lower.startswith("/api/"):
        return f"API {path_lower.split('/')[2] if len(path_lower.split('/')) > 2 else 'Geral'}"

    if metodo == "POST":
        return f"POST {path_lower}"
    return path_lower


async def registrar_acesso(
    ip_acesso: str,
    ds_rota: str,
    ds_metodo: str,
    ds_funcao: str,
    nr_status_http: int,
    vl_tempo_resposta_ms: int,
    nm_usuario: Optional[str] = None,
    cd_pessoa_fisica: Optional[int] = None,
    ds_user_agent: Optional[str] = None,
    ds_query_string: Optional[str] = None,
    ds_referer: Optional[str] = None,
):
    conn = await get_db_connection()
    try:
        await conn.execute(
            """
            INSERT INTO auditoria_acesso (
                ip_acesso, nm_usuario, cd_pessoa_fisica,
                ds_rota, ds_metodo, ds_funcao, ds_user_agent,
                nr_status_http, vl_tempo_resposta_ms,
                ds_query_string, ds_referer
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
            """,
            ip_acesso,
            nm_usuario,
            cd_pessoa_fisica,
            ds_rota[:500],
            ds_metodo[:10],
            (ds_funcao or "")[:200],
            ds_user_agent,
            nr_status_http,
            vl_tempo_resposta_ms,
            ds_query_string,
            ds_referer,
        )
    except Exception as e:
        print(f"Falha ao registrar auditoria: {e}")
    finally:
        await conn.close()


async def listar_auditoria(
    data_inicio: Optional[datetime] = None,
    data_fim: Optional[datetime] = None,
    ip_acesso: Optional[str] = None,
    nm_usuario: Optional[str] = None,
    ds_funcao: Optional[str] = None,
    ds_rota: Optional[str] = None,
    limite: int = 200,
    offset: int = 0,
):
    condicoes = ["1=1"]
    params = []
    idx = 1

    if data_inicio:
        condicoes.append(f"dt_acesso >= ${idx}")
        params.append(data_inicio)
        idx += 1
    if data_fim:
        condicoes.append(f"dt_acesso <= ${idx}")
        params.append(data_fim)
        idx += 1
    if ip_acesso:
        condicoes.append(f"ip_acesso ILIKE ${idx}")
        params.append(f"%{ip_acesso}%")
        idx += 1
    if nm_usuario:
        condicoes.append(f"nm_usuario ILIKE ${idx}")
        params.append(f"%{nm_usuario}%")
        idx += 1
    if ds_funcao:
        condicoes.append(f"ds_funcao ILIKE ${idx}")
        params.append(f"%{ds_funcao}%")
        idx += 1
    if ds_rota:
        condicoes.append(f"ds_rota ILIKE ${idx}")
        params.append(f"%{ds_rota}%")
        idx += 1

    where = " AND ".join(condicoes)

    conn = await get_db_connection()
    try:
        resumo = await conn.fetchrow(
            f"""
            SELECT
                COUNT(*) AS total_acessos,
                COUNT(DISTINCT ip_acesso) AS ips_distintos,
                COUNT(DISTINCT nm_usuario) FILTER (WHERE nm_usuario IS NOT NULL) AS usuarios_distintos,
                COUNT(*) FILTER (WHERE dt_acesso >= CURRENT_DATE) AS acessos_hoje,
                COUNT(DISTINCT ip_acesso) FILTER (WHERE dt_acesso >= CURRENT_DATE) AS ips_hoje
            FROM auditoria_acesso
            WHERE {where}
            """,
            *params,
        )

        por_ip = await conn.fetch(
            f"""
            SELECT ip_acesso, COUNT(*) AS total
            FROM auditoria_acesso
            WHERE {where}
            GROUP BY ip_acesso
            ORDER BY total DESC
            LIMIT 20
            """,
            *params,
        )

        por_funcao = await conn.fetch(
            f"""
            SELECT COALESCE(ds_funcao, 'N/A') AS ds_funcao, COUNT(*) AS total
            FROM auditoria_acesso
            WHERE {where}
            GROUP BY ds_funcao
            ORDER BY total DESC
            LIMIT 20
            """,
            *params,
        )

        por_usuario = await conn.fetch(
            f"""
            SELECT COALESCE(nm_usuario, 'Anônimo') AS nm_usuario, COUNT(*) AS total
            FROM auditoria_acesso
            WHERE {where}
            GROUP BY nm_usuario
            ORDER BY total DESC
            LIMIT 20
            """,
            *params,
        )

        registros = await conn.fetch(
            f"""
            SELECT
                cd_auditoria,
                dt_acesso,
                ip_acesso,
                nm_usuario,
                cd_pessoa_fisica,
                ds_rota,
                ds_metodo,
                ds_funcao,
                ds_user_agent,
                nr_status_http,
                vl_tempo_resposta_ms,
                ds_query_string,
                ds_referer
            FROM auditoria_acesso
            WHERE {where}
            ORDER BY dt_acesso DESC
            LIMIT ${idx} OFFSET ${idx + 1}
            """,
            *params,
            limite,
            offset,
        )

        total_filtrado = resumo["total_acessos"] if resumo else 0

        return {
            "resumo": {
                "total_acessos": total_filtrado,
                "ips_distintos": resumo["ips_distintos"] if resumo else 0,
                "usuarios_distintos": resumo["usuarios_distintos"] if resumo else 0,
                "acessos_hoje": resumo["acessos_hoje"] if resumo else 0,
                "ips_hoje": resumo["ips_hoje"] if resumo else 0,
            },
            "por_ip": [dict(r) for r in por_ip],
            "por_funcao": [dict(r) for r in por_funcao],
            "por_usuario": [dict(r) for r in por_usuario],
            "registros": [dict(r) for r in registros],
        }
    finally:
        await conn.close()
