from app.oracledb.oracle_connection import OracleConnection

#PRODUCAO
oraconn = OracleConnection('ghrprontuario', 'Xy7#kT2@', '10.250.250.2', '1521', 'dbprod.oftalmocuritiba.com.br')
#HOMOLOG
#oraconn = OracleConnection('tasy', 'aloisk', '10.250.250.2', '1521', 'dbhomol.oftalmocuritiba.com.br') 
#TESTEGHR
#oraconn = OracleConnection('demo', 'aloisktasy7818', '192.168.10.19', '1521', 'dbteste')


def get_refracoes_por_consultas(seq_consultas, connection=None):
    """Retorna refrações indexadas por nr_seq_consulta (registro mais recente)."""
    if not seq_consultas:
        return {}

    conn = connection or oraconn
    seq_list = ','.join(str(s) for s in seq_consultas)
    query = f"""
    SELECT
        nr_seq_consulta,
        vl_od_pl_ard_esf,
        vl_od_pl_ard_cil,
        vl_od_pl_ard_eixo,
        vl_oe_pl_ard_esf,
        vl_oe_pl_ard_cil,
        vl_oe_pl_ard_eixo,
        vl_adicao,
        vl_od_pl_are_esf,
        vl_od_pl_are_cil,
        vl_od_pl_are_eixo,
        vl_oe_pl_are_esf,
        vl_oe_pl_are_cil,
        vl_oe_pl_are_eixo,
        ds_observacao
    FROM (
        SELECT
            ofr.nr_seq_consulta,
            ofr.vl_od_pl_ard_esf,
            ofr.vl_od_pl_ard_cil,
            ofr.vl_od_pl_ard_eixo,
            ofr.vl_oe_pl_ard_esf,
            ofr.vl_oe_pl_ard_cil,
            ofr.vl_oe_pl_ard_eixo,
            ofr.vl_adicao,
            ofr.vl_od_pl_are_esf,
            ofr.vl_od_pl_are_cil,
            ofr.vl_od_pl_are_eixo,
            ofr.vl_oe_pl_are_esf,
            ofr.vl_oe_pl_are_cil,
            ofr.vl_oe_pl_are_eixo,
            ofr.ds_observacao,
            ROW_NUMBER() OVER (
                PARTITION BY ofr.nr_seq_consulta
                ORDER BY ofr.dt_atualizacao_nrec DESC NULLS LAST
            ) AS rn
        FROM oft_refracao ofr
        WHERE ofr.nr_seq_consulta IN ({seq_list})
    )
    WHERE rn = 1
    """

    results = conn.execute_select(query)
    refracoes = {}
    for row in results:
        nr_seq = row[0]
        refracoes[nr_seq] = row[1:]
    return refracoes


def get_ds_oculos(nr_atendimento):
    query = """
    SELECT ds_orientacao
    FROM oft_oculos 
    WHERE nr_seq_consulta = (SELECT nr_sequencia FROM oft_consulta WHERE nr_atendimento = :nr_atendimento AND ROWNUM = 1)
    """

    result = oraconn.execute_select(query, {'nr_atendimento': nr_atendimento})

    if not result:
        return ""
    
    ds_oculos = result[0][0]

    return ds_oculos

def get_ultima_orientacao_oculos(nr_atendimento):
    query = """
    SELECT ds_orientacao
    FROM oft_oculos oo
    JOIN oft_consulta oc ON oc.nr_sequencia = oo.nr_seq_consulta
    WHERE oc.cd_pessoa_fisica = (
        SELECT cd_pessoa_fisica
        FROM atendimento_paciente
        WHERE nr_atendimento = :nr_atendimento
    )
    AND oc.nr_atendimento != :nr_atendimento
    AND oo.ds_orientacao IS NOT NULL
    ORDER BY oo.dt_atualizacao DESC
    """

    result = oraconn.execute_select(query, {'nr_atendimento': nr_atendimento})

    if not result:
        return ""
    
    ds_orientacao = result[0][0]

    return ds_orientacao if ds_orientacao else ""