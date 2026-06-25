import locale


def _tem_valor(*vals):
    return any(v is not None and str(v).strip() != '' for v in vals)


def _fmt_num(val):
    if not _tem_valor(val):
        return None
    return locale.format_string('%+0.2f', float(val))


def formatar_texto_oculos(
    esf_od=None, cil_od=None, eixo_od=None,
    esf_oe=None, cil_oe=None, eixo_oe=None,
    adicao=None, observacao=None,
):
    """Formata string de óculos/refrção igual ao frontend (oculos.js)."""
    if not _tem_valor(esf_od, cil_od, eixo_od, esf_oe, cil_oe, eixo_oe, adicao, observacao):
        return ''

    partes = ['Óculos:']

    if _tem_valor(esf_od, cil_od, eixo_od):
        od = ' OD:'
        v = _fmt_num(esf_od)
        if v:
            od += f' {v}'
        v = _fmt_num(cil_od)
        if v:
            od += f' / {v}'
        if _tem_valor(eixo_od):
            od += f' x {eixo_od}°'
        partes.append(od)

    if _tem_valor(esf_oe, cil_oe, eixo_oe):
        oe = ' OE:'
        v = _fmt_num(esf_oe)
        if v:
            oe += f' {v}'
        v = _fmt_num(cil_oe)
        if v:
            oe += f' / {v}'
        if _tem_valor(eixo_oe):
            oe += f' x {eixo_oe}°'
        partes.append(oe)

    if _tem_valor(adicao):
        partes.append(f' A={_fmt_num(adicao)}')

    texto = ''.join(partes)
    if _tem_valor(observacao):
        texto += f'\nOBS: {observacao}'
    return texto


def formatar_refracao_registro(dados, ds_oculos_fallback=None):
    """Formata refração a partir dos campos dinâmica/estática de oft_refracao."""
    if not dados:
        return ds_oculos_fallback or ''

    if isinstance(dados, dict):
        d = dados
    else:
        d = {
            'vl_od_pl_ard_esf': dados[0],
            'vl_od_pl_ard_cil': dados[1],
            'vl_od_pl_ard_eixo': dados[2],
            'vl_oe_pl_ard_esf': dados[3],
            'vl_oe_pl_ard_cil': dados[4],
            'vl_oe_pl_ard_eixo': dados[5],
            'vl_adicao': dados[6],
            'vl_od_pl_are_esf': dados[7] if len(dados) > 7 else None,
            'vl_od_pl_are_cil': dados[8] if len(dados) > 8 else None,
            'vl_od_pl_are_eixo': dados[9] if len(dados) > 9 else None,
            'vl_oe_pl_are_esf': dados[10] if len(dados) > 10 else None,
            'vl_oe_pl_are_cil': dados[11] if len(dados) > 11 else None,
            'vl_oe_pl_are_eixo': dados[12] if len(dados) > 12 else None,
            'ds_observacao': dados[13] if len(dados) > 13 else None,
        }

    tem_estatica = _tem_valor(
        d.get('vl_od_pl_are_esf'), d.get('vl_od_pl_are_cil'), d.get('vl_od_pl_are_eixo'),
        d.get('vl_oe_pl_are_esf'), d.get('vl_oe_pl_are_cil'), d.get('vl_oe_pl_are_eixo'),
    )
    tem_dinamica = _tem_valor(
        d.get('vl_od_pl_ard_esf'), d.get('vl_od_pl_ard_cil'), d.get('vl_od_pl_ard_eixo'),
        d.get('vl_oe_pl_ard_esf'), d.get('vl_oe_pl_ard_cil'), d.get('vl_oe_pl_ard_eixo'),
    )

    if tem_estatica:
        texto = formatar_texto_oculos(
            d.get('vl_od_pl_are_esf'), d.get('vl_od_pl_are_cil'), d.get('vl_od_pl_are_eixo'),
            d.get('vl_oe_pl_are_esf'), d.get('vl_oe_pl_are_cil'), d.get('vl_oe_pl_are_eixo'),
            d.get('vl_adicao'), d.get('ds_observacao'),
        )
    elif tem_dinamica:
        texto = formatar_texto_oculos(
            d.get('vl_od_pl_ard_esf'), d.get('vl_od_pl_ard_cil'), d.get('vl_od_pl_ard_eixo'),
            d.get('vl_oe_pl_ard_esf'), d.get('vl_oe_pl_ard_cil'), d.get('vl_oe_pl_ard_eixo'),
            d.get('vl_adicao'), d.get('ds_observacao'),
        )
    else:
        texto = ''

    return texto or ds_oculos_fallback or ''
