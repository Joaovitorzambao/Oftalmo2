from datetime import datetime
import re
from app.templates_impressao.template_receituario import (
    gerar_estrutura_pagina,
    processar_item_receita
)
from app.templates_impressao.template_exames import (
    gerar_estrutura_pagina_exames,
    processar_lista_exames
)

def format_value(value, is_axis=False):
        if not value or value == "":
            return ""
        try:
            num = float(value)
            if is_axis:
                return f"{int(num)}°"
            formatted = f"{num:+.2f}".replace('.', ',')
            return formatted
        except (ValueError, TypeError):
            return value

def retornar_html_oculos(nr_atendimento, vl_od_pl_ard_esf, vl_od_pl_ard_cil, vl_od_pl_ard_eixo, vl_oe_pl_ard_esf, vl_oe_pl_ard_cil, vl_oe_pl_ard_eixo, adicao, observacao, nm_paciente, dt_nascimento, nr_cpf, dt_atendimento, tipo="dinamica"):
    print(dt_atendimento)
    if dt_atendimento:
        try:
            dia, mes, ano = dt_atendimento.split('/')
            meses = {
                '01': "Janeiro", '02': "Fevereiro", '03': "Março", '04': "Abril", 
                '05': "Maio", '06': "Junho", '07': "Julho", '08': "Agosto", 
                '09': "Setembro", '10': "Outubro", '11': "Novembro", '12': "Dezembro"
            }
            data_formatada = f"{dia} de {meses.get(mes, mes)} de {ano}"
        except:
            data_formatada = dt_atendimento
    else:
        from datetime import datetime
        data_formatada = datetime.now().strftime("%d de %B de %Y")

    data_nascimento_formatada = formatar_data(dt_nascimento)
    tipo_refracao = "Dinâmica" if tipo == "dinamica" else "Estática"

    od_esf = format_value(vl_od_pl_ard_esf)
    od_cil = format_value(vl_od_pl_ard_cil)
    od_eixo = format_value(vl_od_pl_ard_eixo, True)
    oe_esf = format_value(vl_oe_pl_ard_esf)
    oe_cil = format_value(vl_oe_pl_ard_cil)
    oe_eixo = format_value(vl_oe_pl_ard_eixo, True)
    adicao_fmt = format_value(adicao) if adicao else ""

    if observacao:
        # Substituir " - " por uma quebra de linha HTML
        observacao_formatada = observacao.replace(" - ", "<br>- ")
    else:
        observacao_formatada = ""

    IMPRESSAO_OCULOS = f"""
<!DOCTYPE html>
<html lang="pt-BR">
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
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    font-size: 16px;
}}

.header {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 3cm;
    text-align: center;
}}

.content {{
    margin-top: 3cm;
    margin-bottom: 1cm;
    padding: 0 5px;
}}

.content h2 {{
    font-size: 17px;
    text-align: center;
    margin-bottom: 20px;
}}

.patient {{
    margin-bottom: 20px;
    font-size: 15px;
}}

.patient span {{
    font-weight: bold;
}}

.table {{
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
}}

.table th, .table td {{
    border: 1px solid black;
    padding: 6px;
    text-align: center;
    font-size: 15px;
}}

.observations {{
    margin-bottom: 20px;
}}

.adicao {{
    margin-bottom: 10px;
    border: 1px solid #000;
    padding: 8px;
}}

.footer {{
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 1cm;
    text-align: center;
    font-size: 13px;
}}

.data-footer {{
    font-weight: bold;
    font-size: 13px;
}}

.medico-footer {{
    font-weight: bold;
    font-size: 14px;
}}
</style>
</head>

<body>

<div class="header">
    <!-- Se quiser colocar logo depois -->
</div>

<div class="content">

    <h2 style="font-style: italic;">PRESCRIÇÃO DE ÓCULOS</h2>

    <div class="patient">
        <p><span>Para:</span> {nm_paciente}</p>
        <p><strong>CPF:</strong> {nr_cpf}</p>
        <p><strong>Data Nascimento:</strong> {data_nascimento_formatada}</p>
    </div>

    <table class="table">
        <thead>
            <tr>
                <th></th>
                <th>ESFÉRICA</th>
                <th>CILÍNDRICA</th>
                <th>EIXO</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>OD</td>
                <td>{od_esf}</td>
                <td>{od_cil}</td>
                <td>{od_eixo}</td>
            </tr>
            <tr>
                <td>OE</td>
                <td>{oe_esf}</td>
                <td>{oe_cil}</td>
                <td>{oe_eixo}</td>
            </tr>
        </tbody>
    </table>

    <div class="observations">
        {f'<p class="adicao">Adição: <span>{adicao_fmt}</span></p>' if tipo == "dinamica" else ''}
        
        <p><strong>Observações:</strong></p>
        <div>
            {observacao_formatada}
        </div>
    </div>

</div>

<div class="footer">
    <p class="data-footer">Curitiba, {data_formatada}</p>
    <p class="medico-footer">IRINEU ANTUNES NETO - CRM:5199 RQE:2694</p>
</div>

</body>
</html>
"""
    return IMPRESSAO_OCULOS


def retornar_html_receita(receita, nm_paciente, dt_nascimento, nr_cpf, nr_copias=1):
    """
    Gera HTML de receita usando template modular
    """
    from datetime import datetime
    
    # Dividir a receita em itens individuais
    itens_receita = [item.strip() for item in receita.split('\n\n') if item.strip()]
    
    # Formatar dados - CORRIGIR AQUI
    data_atual = datetime.now()
    data_formatada = data_atual.strftime("%d de %B de %Y")
    
    # Formatar data de nascimento
    data_nascimento_formatada = formatar_data(dt_nascimento)
    
    # Processar cada item da receita
    formatted_items = []
    for item in itens_receita:
        item_html = processar_item_receita(item)
        if item_html:
            formatted_items.append(item_html)
    
    # Juntar todos os itens
    conteudo_medicamentos = "".join(formatted_items)
    
    # Gerar HTML usando o template modular
    html_receita = gerar_estrutura_pagina(
        conteudo_medicamentos,
        nm_paciente,
        nr_cpf,
        data_nascimento_formatada,
        data_formatada
    )
    
    # Tratar múltiplas cópias se necessário
    if nr_copias > 1:
        copias_html = []
        for i in range(nr_copias):
            if i > 0:
                copias_html.append('<div style="page-break-before: always;"></div>')
            copias_html.append(html_receita)
        return "".join(copias_html)
    
    return html_receita


def retornar_html_exames(exames, nm_paciente, ds_convenio, dt_nascimento, nr_cpf):
    """
    Gera HTML de exames usando template modular
    """
    # Formatar dados
    data_atual = datetime.now()
    data_formatada = data_atual.strftime("%d de %B de %Y")
    data_nascimento_formatada = formatar_data(dt_nascimento)
    
    # Processar lista de exames
    conteudo_exames = processar_lista_exames(exames)
    
    # Gerar HTML usando o template modular
    html_exames = gerar_estrutura_pagina_exames(
        conteudo_exames,
        nm_paciente,
        ds_convenio,
        nr_cpf,
        data_nascimento_formatada,
        data_formatada
    )
    
    return html_exames



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
