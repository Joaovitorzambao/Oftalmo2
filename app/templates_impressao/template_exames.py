from datetime import datetime


def gerar_header_exames(nm_paciente, ds_convenio, nr_cpf, dt_nascimento):
    return f"""
    <div class="header-content">
        <h3>Solicitação de Exames</h3>

        <p><strong>{nm_paciente}</strong></p>
        <p>Convênio: {ds_convenio}</p>
        <p>CPF: {nr_cpf}</p>
        <p>Data Nascimento: {dt_nascimento}</p>

        <hr style="margin:10px 0;">
    </div>
    """


def gerar_footer_exames(data_formatada):
    return f"""
    <div class="footer-content">
        <p><strong>Curitiba, {data_formatada}</strong></p>
        <p><strong>IRINEU ANTUNES NETO - CRM:5199 RQE:2694</strong></p>
    </div>
    """


def gerar_estrutura_pagina_exames(
    conteudo_exames,
    nm_paciente,
    ds_convenio,
    nr_cpf,
    dt_nascimento,
    data_formatada
):

    return f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">

<style>
@page {{
    size: A5;
    margin-top: 4cm;
    margin-bottom: 2cm;
    margin-left: 1cm;
    margin-right: 1cm;
}}

body {{
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    line-height: 1.5;
}}

/* CONTEÚDO PRINCIPAL */
.content {{
    width: 100%;
}}

/* ESTILOS */
h3 {{
    margin: 0 0 10px 0;
}}

p {{
    margin: 4px 0;
}}

.exam-item {{
    margin-bottom: 10px;
    line-height: 1.6;
}}

.assinatura {{
    margin-top: 40px;
    text-align: center;
    font-size: 12px;
}}
</style>

</head>
<body>

<div class="content">

    <h3>Solicitação de Exames</h3>

    <p><strong>{nm_paciente}</strong></p>
    <p>Convênio: {ds_convenio}</p>
    <p>CPF: {nr_cpf}</p>
    <p>Data Nascimento: {dt_nascimento}</p>

    <hr style="margin:10px 0;">

    {conteudo_exames}

    <div class="assinatura">
        <p><strong>Curitiba, {data_formatada}</strong></p>
        <p><strong>IRINEU ANTUNES NETO - CRM:5199 RQE:2694</strong></p>
    </div>

</div>

</body>
</html>
"""


def processar_lista_exames(exames_texto):
    linhas = [linha.strip() for linha in exames_texto.split('\n') if linha.strip()]
    
    exames_processados = []
    
    for linha in linhas:
        if linha.lower() in ["não informado", "- não informado", "nao informado"]:
            continue
        
        exames_processados.append(f'<div class="exam-item">- {linha}</div>')
    
    return "".join(exames_processados)