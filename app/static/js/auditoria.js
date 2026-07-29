document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('filtros-form');
    const tbody = document.getElementById('tabela-body');
    const loading = document.getElementById('loading');
    const semDados = document.getElementById('sem-dados');
    const btnLimpar = document.getElementById('btn-limpar');
    const btnAnterior = document.getElementById('btn-anterior');
    const btnProximo = document.getElementById('btn-proximo');
    const infoPaginacao = document.getElementById('info-paginacao');

    let offset = 0;
    const limite = 100;

    async function carregarDados(resetOffset = true) {
        if (resetOffset) offset = 0;

        loading.style.display = 'block';
        semDados.style.display = 'none';
        tbody.innerHTML = '';

        const params = new URLSearchParams(new FormData(form));
        params.set('limite', limite);
        params.set('offset', offset);

        try {
            const response = await fetch(`/api/auditoria/logs?${params.toString()}`);
            if (!response.ok) throw new Error('Erro ao carregar logs');

            const data = await response.json();
            atualizarResumo(data.resumo);
            atualizarRanking('ranking-ip', data.por_ip, 'ip_acesso');
            atualizarRanking('ranking-funcao', data.por_funcao, 'ds_funcao');
            atualizarRanking('ranking-usuario', data.por_usuario, 'nm_usuario');
            renderizarTabela(data.registros);

            const total = data.resumo.total_acessos;
            infoPaginacao.textContent = `Exibindo ${offset + 1}–${Math.min(offset + limite, total)} de ${total}`;
            btnAnterior.disabled = offset === 0;
            btnProximo.disabled = offset + limite >= total;

            document.getElementById('ultima-atualizacao').textContent =
                `Atualizado às ${new Date().toLocaleTimeString('pt-BR')}`;
        } catch (err) {
            console.error(err);
            tbody.innerHTML = '<tr><td colspan="9" style="color:red;text-align:center">Erro ao carregar dados. Verifique se a tabela auditoria_acesso existe no PostgreSQL.</td></tr>';
        } finally {
            loading.style.display = 'none';
        }
    }

    function atualizarResumo(resumo) {
        document.getElementById('total-acessos').textContent = resumo.total_acessos.toLocaleString('pt-BR');
        document.getElementById('ips-distintos').textContent = resumo.ips_distintos.toLocaleString('pt-BR');
        document.getElementById('usuarios-distintos').textContent = resumo.usuarios_distintos.toLocaleString('pt-BR');
        document.getElementById('acessos-hoje').textContent = resumo.acessos_hoje.toLocaleString('pt-BR');
        document.getElementById('ips-hoje').textContent = resumo.ips_hoje.toLocaleString('pt-BR');
    }

    function atualizarRanking(elementId, items, campo) {
        const el = document.getElementById(elementId);
        if (!items || items.length === 0) {
            el.innerHTML = '<div class="sem-dados">Nenhum dado</div>';
            return;
        }
        el.innerHTML = items.map(item => `
            <div class="ranking-item">
                <span>${item[campo] || 'N/A'}</span>
                <span class="total">${item.total}</span>
            </div>
        `).join('');
    }

    function renderizarTabela(registros) {
        if (!registros || registros.length === 0) {
            semDados.style.display = 'block';
            return;
        }

        tbody.innerHTML = registros.map(r => {
            const dt = r.dt_acesso ? new Date(r.dt_acesso).toLocaleString('pt-BR') : '-';
            const metodo = (r.ds_metodo || 'GET').toUpperCase();
            const badgeClass = `badge badge-${metodo.toLowerCase()}`;
            const statusClass = r.nr_status_http < 400 ? 'status-ok' : 'status-erro';

            return `<tr>
                <td>${dt}</td>
                <td><strong>${r.ip_acesso || '-'}</strong></td>
                <td>${r.nm_usuario || '<em>—</em>'}</td>
                <td>${r.ds_funcao || '-'}</td>
                <td title="${r.ds_rota}">${truncar(r.ds_rota, 40)}</td>
                <td><span class="${badgeClass}">${metodo}</span></td>
                <td class="${statusClass}">${r.nr_status_http || '-'}</td>
                <td>${r.vl_tempo_resposta_ms != null ? r.vl_tempo_resposta_ms + ' ms' : '-'}</td>
                <td class="user-agent-cell" title="${r.ds_user_agent || ''}">${truncar(r.ds_user_agent, 30)}</td>
            </tr>`;
        }).join('');
    }

    function truncar(texto, max) {
        if (!texto) return '-';
        return texto.length > max ? texto.substring(0, max) + '…' : texto;
    }

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        carregarDados(true);
    });

    btnLimpar.addEventListener('click', () => {
        form.reset();
        carregarDados(true);
    });

    btnAnterior.addEventListener('click', () => {
        offset = Math.max(0, offset - limite);
        carregarDados(false);
    });

    btnProximo.addEventListener('click', () => {
        offset += limite;
        carregarDados(false);
    });

    carregarDados(true);
    setInterval(() => carregarDados(false), 60000);
});
