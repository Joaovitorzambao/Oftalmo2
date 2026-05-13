from app.oracledb.oracle_connection import OracleConnection

#PRODUCAO
oraconn = OracleConnection('ghrprontuario', 'Xy7#kT2@', '10.250.250.2', '1521', 'dbprod.oftalmocuritiba.com.br')
#HOMOLOG
#oraconn = OracleConnection('tasy', 'aloisk', '10.250.250.2', '1521', 'dbhomol.oftalmocuritiba.com.br') 
#TESTEGHR
#oraconn = OracleConnection('demo', 'aloisktasy7818', '192.168.10.19', '1521', 'dbteste')

def get_evolucao_data(nr_atendimento):
    """
    Fetch all evolution data for a specific appointment
    """
    query = """
    WITH ConsultaInfo AS (
        SELECT 
            nr_sequencia as nr_seq_consulta
        FROM oft_consulta 
        WHERE nr_atendimento = :nr_atendimento
    )
    SELECT 
        oa.ds_anamnese as queixa,
        ofr.vl_od_pl_ard_esf,
        ofr.vl_od_pl_ard_cil,
        ofr.vl_od_pl_ard_eixo,
        ofr.vl_oe_pl_ard_esf,
        ofr.vl_oe_pl_ard_cil,
        ofr.vl_oe_pl_ard_eixo,
        ofr.vl_adicao,
        ofr.ds_observacao as obs_refracao,
        oca.ds_observacao as acuidade,
        ot.ds_observacao as pressao,
        dm.ds_diagnostico,
        ofc.ds_conduta,
        pee.ds_solicitacao as exames,
        oo.ds_orientacao as oculos,
        ofr.vl_od_pl_are_esf,
        ofr.vl_od_pl_are_cil,
        ofr.vl_od_pl_are_eixo,
        ofr.vl_oe_pl_are_esf,
        ofr.vl_oe_pl_are_cil,
        ofr.vl_oe_pl_are_eixo
    FROM ConsultaInfo ci
    LEFT JOIN oft_anamnese oa ON oa.nr_seq_consulta = ci.nr_seq_consulta
    LEFT JOIN oft_refracao ofr ON ofr.nr_seq_consulta = ci.nr_seq_consulta
    LEFT JOIN oft_correcao_atual oca ON oca.nr_seq_consulta = ci.nr_seq_consulta
    LEFT JOIN oft_tonometria ot ON ot.nr_seq_consulta = ci.nr_seq_consulta
    LEFT JOIN diagnostico_medico dm ON dm.nr_atendimento = :nr_atendimento
    LEFT JOIN oft_conduta ofc ON ofc.nr_seq_consulta = ci.nr_seq_consulta
    LEFT JOIN pedido_exame_externo pee ON pee.nr_atendimento = :nr_atendimento
    LEFT JOIN oft_oculos oo ON oo.nr_seq_consulta = ci.nr_seq_consulta
    """
    
    result = oraconn.execute_select(query, {'nr_atendimento': nr_atendimento})
    
    if not result:
        return None

    # Convert the first row to a dictionary with all fields
    evolucao_data = {
        'queixa': result[0][0] or '',
        'vl_od_pl_ard_esf': result[0][1] or '',
        'vl_od_pl_ard_cil': result[0][2] or '',
        'vl_od_pl_ard_eixo': result[0][3] or '',
        'vl_oe_pl_ard_esf': result[0][4] or '',
        'vl_oe_pl_ard_cil': result[0][5] or '',
        'vl_oe_pl_ard_eixo': result[0][6] or '',
        'vl_adicao': result[0][7] or '',
        'obs_refracao': result[0][8] or '',
        'acuidade': result[0][9] or '',
        'pressao': result[0][10] or '',
        'diagnostico': result[0][11] or '',
        'conduta': result[0][12] or '',
        'exames': result[0][13] or '',
        'oculos': result[0][14] or '',
        'vl_od_pl_are_esf': result[0][15] or '',
        'vl_od_pl_are_cil': result[0][16] or '',
        'vl_od_pl_are_eixo': result[0][17] or '',
        'vl_oe_pl_are_esf': result[0][18] or '',
        'vl_oe_pl_are_cil': result[0][19] or '',
        'vl_oe_pl_are_eixo': result[0][20] or ''
    }

    return evolucao_data


def get_evolucao_data_with_fallback(nr_atendimento):
    """
    Fetch evolution data for a specific appointment.
    If refraction data is empty, fetch from patient's history.
    """
    # First, try to get data for current appointment
    evolucao_data = get_evolucao_data(nr_atendimento)
    
    if not evolucao_data:
        return None
    
    # Check if key refraction fields are empty
    has_refracao = any([
        evolucao_data.get('vl_od_pl_ard_esf'),
        evolucao_data.get('vl_od_pl_ard_cil'),
        evolucao_data.get('vl_od_pl_ard_eixo'),
        evolucao_data.get('vl_oe_pl_ard_esf'),
        evolucao_data.get('vl_oe_pl_ard_cil'),
        evolucao_data.get('vl_oe_pl_ard_eixo'),
        evolucao_data.get('vl_od_pl_are_esf'),
        evolucao_data.get('vl_od_pl_are_cil'),
        evolucao_data.get('vl_od_pl_are_eixo'),
        evolucao_data.get('vl_oe_pl_are_esf'),
        evolucao_data.get('vl_oe_pl_are_cil'),
        evolucao_data.get('vl_oe_pl_are_eixo'),
    ])
    
    # If no refraction data, fetch from patient history
    if not has_refracao:
        query = """
        SELECT 
            ofr.vl_od_pl_ard_esf,
            ofr.vl_od_pl_ard_cil,
            ofr.vl_od_pl_ard_eixo,
            ofr.vl_oe_pl_ard_esf,
            ofr.vl_oe_pl_ard_cil,
            ofr.vl_oe_pl_ard_eixo,
            ofr.vl_adicao,
            ofr.ds_observacao as obs_refracao,
            ofr.vl_od_pl_are_esf,
            ofr.vl_od_pl_are_cil,
            ofr.vl_od_pl_are_eixo,
            ofr.vl_oe_pl_are_esf,
            ofr.vl_oe_pl_are_cil,
            ofr.vl_oe_pl_are_eixo
        FROM oft_refracao ofr
        JOIN oft_consulta oc ON oc.nr_sequencia = ofr.nr_seq_consulta
        WHERE oc.cd_pessoa_fisica = (
            SELECT cd_pessoa_fisica
            FROM atendimento_paciente
            WHERE nr_atendimento = :nr_atendimento
        )
        AND oc.nr_atendimento != :nr_atendimento
        AND ofr.dt_atualizacao_nrec IS NOT NULL
        AND (
            ofr.vl_od_pl_ard_esf IS NOT NULL
            OR ofr.vl_od_pl_ard_cil IS NOT NULL
            OR ofr.vl_od_pl_ard_eixo IS NOT NULL
            OR ofr.vl_oe_pl_ard_esf IS NOT NULL
            OR ofr.vl_oe_pl_ard_cil IS NOT NULL
            OR ofr.vl_oe_pl_ard_eixo IS NOT NULL
            OR ofr.vl_od_pl_are_esf IS NOT NULL
            OR ofr.vl_od_pl_are_cil IS NOT NULL
            OR ofr.vl_od_pl_are_eixo IS NOT NULL
            OR ofr.vl_oe_pl_are_esf IS NOT NULL
            OR ofr.vl_oe_pl_are_cil IS NOT NULL
            OR ofr.vl_oe_pl_are_eixo IS NOT NULL
        )
        ORDER BY ofr.dt_atualizacao_nrec DESC
        """
        
        result = oraconn.execute_select(query, {'nr_atendimento': nr_atendimento})
        
        if result:
            # Update with historical data
            evolucao_data['vl_od_pl_ard_esf'] = result[0][0] or ''
            evolucao_data['vl_od_pl_ard_cil'] = result[0][1] or ''
            evolucao_data['vl_od_pl_ard_eixo'] = result[0][2] or ''
            evolucao_data['vl_oe_pl_ard_esf'] = result[0][3] or ''
            evolucao_data['vl_oe_pl_ard_cil'] = result[0][4] or ''
            evolucao_data['vl_oe_pl_ard_eixo'] = result[0][5] or ''
            evolucao_data['vl_adicao'] = result[0][6] or ''
            evolucao_data['obs_refracao'] = result[0][7] or ''
            evolucao_data['vl_od_pl_are_esf'] = result[0][8] or ''
            evolucao_data['vl_od_pl_are_cil'] = result[0][9] or ''
            evolucao_data['vl_od_pl_are_eixo'] = result[0][10] or ''
            evolucao_data['vl_oe_pl_are_esf'] = result[0][11] or ''
            evolucao_data['vl_oe_pl_are_cil'] = result[0][12] or ''
            evolucao_data['vl_oe_pl_are_eixo'] = result[0][13] or ''
    
    return evolucao_data