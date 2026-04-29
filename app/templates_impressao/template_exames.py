from datetime import datetime

def gerar_header_exames(nm_paciente, ds_convenio, nr_cpf, dt_nascimento):
    """Gera o HTML do header para exames"""
    return f"""
    <div class="page-header">
        <h3 style="margin: 0 0 10px 0;">SOLICITAÇÃO EXAMES</h3>
        <p><span>Para:</span> <span class="patient-name"><strong>{nm_paciente}</strong></span></p>
        <p><strong>Convênio: {ds_convenio}</strong></p>
        <div class="patient-info">
            <span><strong>CPF: {nr_cpf}</strong></span>
            <span><strong>Data Nascimento: {dt_nascimento}</strong></span>
        </div>
        <h4 style="margin: 10px 0 5px 0;">EXAMES:</h4>
        <hr style="margin: 0; border: 0; border-top: 1px solid #C0C0C0;">
    </div>
    """

def gerar_footer_exames(data_formatada):
    """Gera o HTML do footer para exames"""
    return f"""
    <div class="page-footer">
        <p><strong>Curitiba, {data_formatada}</strong></p>
        <br>
        <p><strong>IRINEU ANTUNES NETO - CRM:5199 RQE:2694</strong></p>
    </div>
    """

def gerar_estrutura_pagina_exames(conteudo_exames, nm_paciente, ds_convenio, nr_cpf, dt_nascimento, data_formatada):

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
    height: 3cm;
    width: 100%;
}}

.footer {{
    position: fixed;
    bottom: 0;
    height: 1cm;
    width: 100%;
    text-align: center;
}}

.content {{
    margin-top: 3cm;
    margin-bottom: 1cm;
}}

.exam-item {{
    margin-bottom: 5px;
    page-break-inside: avoid;
}}
</style>
</head>

<body>

<div class="header">
    <h3>Solicitação de Exames</h3>
    <p><strong>{nm_paciente}</strong></p>
    <p>Convênio: {ds_convenio}</p>
    <p>CPF: {nr_cpf} | Nascimento: {dt_nascimento}</p>
</div>

<div class="content">
    {conteudo_exames}
</div>

<div class="footer">
    Curitiba, {data_formatada}
</div>

</body>
</html>
"""
    
    return template

def processar_lista_exames(exames_texto):
    """
    Processa a lista de exames e retorna HTML formatado
    """
    linhas = [linha.strip() for linha in exames_texto.split('\n') if linha.strip()]
    exames_processados = []
    for linha in linhas:
        if ' - ' in linha:
            partes = linha.split(' - ', 1)
            exames_processados.append(f'<div class="exam-item">- {partes[1].strip()}</div>')
        else:
            exames_processados.append(f'<div class="exam-item">- {linha}</div>')
    return "".join(exames_processados)