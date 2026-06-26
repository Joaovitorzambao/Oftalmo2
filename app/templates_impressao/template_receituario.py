from datetime import datetime

def gerar_header(nm_paciente, nr_cpf, dt_nascimento):
    """Gera o HTML do header que será repetido em cada página"""
    return f"""
    <div class="page-header">
        <p><span>Para:</span> <span class="patient-name"><strong>{nm_paciente}</strong></span></p>
        <div class="patient-info">
            <span><strong>CPF: {nr_cpf}</strong></span>
            <span><strong>Data Nascimento: {dt_nascimento}</strong></span>
        </div>
    </div>
    """

def gerar_footer(data_formatada):
    """Gera o HTML do footer que será repetido em cada página"""
    return f"""
    <div class="page-footer">
        <p><strong>Curitiba, {data_formatada}</strong></p>
        <br>
        <p><strong>IRINEU ANTUNES NETO - CRM:5199 RQE:2694</strong></p>
    </div>
    """

def gerar_estrutura_pagina(conteudo_items, nm_paciente, nr_cpf, dt_nascimento, data_formatada):

    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
@page {{
    size: A5;
    margin-top: 4cm;
    margin-bottom: 3cm;
    margin-left: 1cm;
    margin-right: 1cm;
}}

body {{
    font-family: Arial;
    margin: 0;
    line-height: 1.5
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

.med-item {{
    margin-bottom: 10px;
    page-break-inside: avoid;
}}
</style>
</head>

<body>

<div class="header">
    <p><strong>{nm_paciente}</strong></p>
    <p>CPF: {nr_cpf} | Nascimento: {dt_nascimento}</p>
</div>

<div class="content">
    {conteudo_items}
</div>

<div class="footer">
    Curitiba, {data_formatada}
</div>

</body>
</html>
"""
    
    return template

def processar_item_receita(item):
    """
    Processa um item individual da receita
    Retorna HTML formatado para o item
    """
    import re

    lines = item.split("\n")
    uso_line = ""
    medicamento_line = ""
    quantidade_line = ""
    instrucoes_lines = []
    found_medicamento = False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("USO:") or stripped.startswith("=> USO"):
            uso_line = stripped.replace("=> ", "").strip()
        elif (
            ":" in stripped
            and not stripped.startswith("USO:")
            and not stripped.startswith("=> USO")
            and not found_medicamento
        ):
            parts = stripped.split(":", 1)
            if len(parts) == 2:
                medicamento_line = parts[0].strip() + ":"
                rest = parts[1].strip()
                if rest:
                    if re.match(
                        r"^(Pingar|Tomar|Aplicar|Ingerir|Usar|Colocar|Instilar)",
                        rest,
                        re.IGNORECASE,
                    ):
                        instrucoes_lines.append(rest)
                    else:
                        quantidade_line = rest
                found_medicamento = True
        elif found_medicamento or medicamento_line:
            instrucoes_lines.append(stripped)

    if quantidade_line and medicamento_line:
        quantidade_match = re.match(r"^([0-9]+[A-Za-z]*)\s*(.*)$", quantidade_line)
        if quantidade_match:
            quantidade = quantidade_match.group(1)
            restante = quantidade_match.group(2).strip()

            if quantidade.isdigit() and restante:
                partes_restante = restante.split(" ", 1)
                primeira_palavra = partes_restante[0]
                if (
                    primeira_palavra.isalpha()
                    and primeira_palavra.isupper()
                    and len(primeira_palavra) <= 4
                ):
                    quantidade = f"{quantidade}{primeira_palavra}"
                    restante = partes_restante[1].strip() if len(partes_restante) > 1 else ""

            if restante and re.match(
                r"^(Pingar|Tomar|Aplicar|Ingerir|Usar|Colocar|Instilar)",
                restante,
                re.IGNORECASE,
            ):
                instrucoes_lines.insert(0, restante)
                restante = ""

            medicamento_line = f"{medicamento_line} {quantidade}".strip()
            if restante:
                instrucoes_lines.insert(0, restante)
        else:
            medicamento_line = f"{medicamento_line} {quantidade_line}".strip()

    instrucoes_html = []
    for instr in instrucoes_lines:
        sentences = [s.strip() for s in re.split(r"(?<=\.)\s*", instr) if s.strip()]
        instrucoes_html.extend(sentences)
    instrucoes_line = "<br>".join(instrucoes_html)

    blocos = []
    if uso_line:
        blocos.append(f'- <span class="uso-linha">{uso_line}</span>')
    if medicamento_line:
        blocos.append(f'<span class="medicamento-linha">{medicamento_line}</span>')
    if instrucoes_line:
        blocos.append(f'<span class="instrucoes-linha">{instrucoes_line}</span>')

    if not blocos:
        return ""

    return f'<div class="med-item">{"<br>".join(blocos)}</div>'