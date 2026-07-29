-- =============================================================================
-- Seed: Tabela de Auditoria e Acessos
-- Banco: prontuario_oftalmo_prod (PostgreSQL)
--
-- Executar na VM:
--   psql -U postgres -d prontuario_oftalmo_prod -f database/seeds/001_auditoria_acesso.sql
-- =============================================================================

BEGIN;

CREATE TABLE IF NOT EXISTS auditoria_acesso (
    cd_auditoria       BIGSERIAL PRIMARY KEY,
    dt_acesso          TIMESTAMP NOT NULL DEFAULT NOW(),
    ip_acesso          VARCHAR(45) NOT NULL,
    nm_usuario         VARCHAR(100),
    cd_pessoa_fisica   BIGINT,
    ds_rota            VARCHAR(500) NOT NULL,
    ds_metodo          VARCHAR(10) NOT NULL,
    ds_funcao          VARCHAR(200),
    ds_user_agent      TEXT,
    nr_status_http     INTEGER,
    vl_tempo_resposta_ms INTEGER,
    ds_query_string    TEXT,
    ds_referer         TEXT
);

CREATE INDEX IF NOT EXISTS idx_auditoria_dt_acesso
    ON auditoria_acesso (dt_acesso DESC);

CREATE INDEX IF NOT EXISTS idx_auditoria_ip
    ON auditoria_acesso (ip_acesso);

CREATE INDEX IF NOT EXISTS idx_auditoria_usuario
    ON auditoria_acesso (nm_usuario);

CREATE INDEX IF NOT EXISTS idx_auditoria_funcao
    ON auditoria_acesso (ds_funcao);

CREATE INDEX IF NOT EXISTS idx_auditoria_rota
    ON auditoria_acesso (ds_rota);

COMMENT ON TABLE auditoria_acesso IS 'Registro de auditoria e acessos ao sistema';
COMMENT ON COLUMN auditoria_acesso.ip_acesso IS 'Endereço IP do cliente (considera X-Forwarded-For)';
COMMENT ON COLUMN auditoria_acesso.ds_funcao IS 'Nome amigável da funcionalidade acessada';

-- Dados de exemplo (opcional — remova o bloco abaixo em produção se não quiser registros fictícios)
INSERT INTO auditoria_acesso (
    dt_acesso, ip_acesso, nm_usuario, cd_pessoa_fisica,
    ds_rota, ds_metodo, ds_funcao, ds_user_agent,
    nr_status_http, vl_tempo_resposta_ms, ds_query_string
) VALUES
    (NOW() - INTERVAL '2 days', '192.168.0.10', 'dr.silva', 1001,
     '/agenda', 'GET', 'Agenda', 'Mozilla/5.0', 200, 120, NULL),
    (NOW() - INTERVAL '2 days', '192.168.0.10', 'dr.silva', 1001,
     '/prontuario/723860', 'GET', 'Prontuário', 'Mozilla/5.0', 200, 340, 'cd_pessoa_fisica=12345'),
    (NOW() - INTERVAL '1 day', '192.168.0.22', 'dr.maria', 1002,
     '/login', 'POST', 'Login', 'Mozilla/5.0', 302, 85, NULL),
    (NOW() - INTERVAL '1 day', '192.168.0.22', 'dr.maria', 1002,
     '/agenda', 'GET', 'Agenda', 'Mozilla/5.0', 200, 95, NULL),
    (NOW() - INTERVAL '6 hours', '10.0.0.5', 'admin', 1003,
     '/editar-exames', 'GET', 'Editar Exames', 'Mozilla/5.0', 200, 210, NULL),
    (NOW() - INTERVAL '3 hours', '192.168.0.10', 'dr.silva', 1001,
     '/prontuario/730106/oculos', 'GET', 'Óculos', 'Mozilla/5.0', 200, 180, NULL),
    (NOW() - INTERVAL '1 hour', '192.168.0.55', NULL, NULL,
     '/login', 'GET', 'Login', 'Mozilla/5.0', 200, 45, NULL),
    (NOW() - INTERVAL '30 minutes', '192.168.0.22', 'dr.maria', 1002,
     '/api/historico-paciente/12345', 'GET', 'Histórico Paciente', 'Mozilla/5.0', 200, 520, NULL);

COMMIT;
