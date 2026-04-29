from datetime import datetime


def retornar_html_resumo(nm_paciente, idade_paciente, profissao, convenio, sexo, cpf, nascimento, consultas):

    dt_nascimento = formatar_data(nascimento)

    consultas_html = ""
    for consulta in consultas:
        consultas_html += f"""
        <div class="consultation">
            <h3>Consulta - {consulta.get('data_consulta', 'N/A')}</h3>
            <p><strong>Status:</strong> {consulta.get('status_consulta', 'N/A')}</p>
            <div><strong>Atendimento:</strong> {consulta.get('nr_atendimento', 'N/A')}</div>
            <div><strong>Médico:</strong> {consulta.get('medico', 'N/A')}</div>
            <div><strong>Queixa:</strong> {consulta.get('queixa', 'N/A')}</div>
            <div><strong>Diagnóstico:</strong> {consulta.get('diagnostico', 'N/A')}</div>
        </div>
        """

    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
@page {{
    size: A5;
    margin-top: 2cm;
    margin-bottom: 3cm;
    margin-left: 1cm;
    margin-right: 1cm;
}}

body {{
    font-family: Arial;
    margin: 0;
}}

.header {{
    position: fixed;
    top: 0;
    width: 100%;
    height: 3cm;
    text-align: center;
}}

.footer {{
    position: fixed;
    bottom: 0;
    width: 100%;
    height: 1cm;
    text-align: center;
    font-size: 12px;
}}

.content {{
    margin-top: 3cm;
    margin-bottom: 1cm;
}}

.consultation {{
    border: 1px solid #ccc;
    padding: 10px;
    margin-bottom: 10px;
    page-break-inside: avoid;
}}
</style>
</head>

<body>

<div class="header">
    <h2>Resumo do Prontuário</h2>
</div>

<div class="content">
    <p><strong>Paciente:</strong> {nm_paciente}</p>
    <p><strong>CPF:</strong> {cpf}</p>
    <p><strong>Nascimento:</strong> {dt_nascimento}</p>

    {consultas_html}
</div>

<div class="footer">
    Documento gerado automaticamente
</div>

</body>
</html>
"""



def formatar_data(data_iso):
    """Formata uma data para o formato brasileiro DD/MM/AAAA.

    Args:
        data_iso: A data no formato ISO 8601 (AAAA-MM-DD HH:MM:SS), datetime, ou DD/MM/YYYY

    Returns:
        Uma string com a data formatada para o Brasil.
    """
    if data_iso is None:
        return "Não informado"

    # Se já é um objeto datetime, apenas formata
    if isinstance(data_iso, datetime):
        data_formatada = data_iso.strftime('%d/%m/%Y')
        return data_formatada
    
    # Se for string, tentar diferentes formatos
    if isinstance(data_iso, str):
        # Se já está no formato DD/MM/YYYY, retornar direto
        if '/' in data_iso and len(data_iso) == 10:
            try:
                # Validar se é uma data válida
                datetime.strptime(data_iso, '%d/%m/%Y')
                return data_iso
            except ValueError:
                pass
        
        # Tentar formato completo: YYYY-MM-DD HH:MM:SS
        try:
            data = datetime.strptime(data_iso, '%Y-%m-%d %H:%M:%S')
            data_formatada = data.strftime('%d/%m/%Y')
            return data_formatada
        except ValueError:
            pass
        
        # Tentar formato simples: YYYY-MM-DD
        try:
            data = datetime.strptime(data_iso, '%Y-%m-%d')
            data_formatada = data.strftime('%d/%m/%Y')
            return data_formatada
        except ValueError:
            pass
    
    # Se nenhum formato funcionou, retornar a string original
    return str(data_iso)

