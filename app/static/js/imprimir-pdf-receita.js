const flashMessageDiv = () => document.getElementById("flash-message");

const exibirMensagem = (mensagem, tipo = "success") => {
    const target = flashMessageDiv();
    if (!target) return;

    target.style.display = "block";
    target.textContent = mensagem;

    if (tipo === "success") {
        target.style.backgroundColor = "#d4edda";
        target.style.color = "#155724";
    } else {
        target.style.backgroundColor = "#f8d7da";
        target.style.color = "#721c24";
    }

    setTimeout(() => {
        target.style.opacity = "0";
        setTimeout(() => {
            target.style.display = "none";
            target.style.opacity = "1";
        }, 1000);
    }, 3000);
};

window.capturarValoresReceita = () => {
    let receita = '';

    const activeTab = document.querySelector('.receita-tab.active');
    const activeTabId = activeTab ? activeTab.dataset.tab : 'receita1';
    const textareaReceita = document.getElementById(activeTabId === 'receita1' ? 'receita' : 'receita2');
    const nmPessoaFisica = document.getElementById("nm_paciente")?.textContent?.trim() || '';
    const elementoPaciente = document.getElementById("nm_paciente");
    const dataNascimento = elementoPaciente?.dataset?.nascimento || '';
    const dataCpf = elementoPaciente?.dataset?.cpf || '';

    if (textareaReceita && textareaReceita.offsetParent !== null) {
        receita = textareaReceita.value.trim();
    }

    console.log('Capturando valores de receita', { activeTabId, receita, nmPessoaFisica, dataNascimento, dataCpf });

    return {
        receita,
        nm_pessoa_fisica: nmPessoaFisica,
        data_nascimento: dataNascimento,
        data_cpf: dataCpf
    };
};

window.enviarDadosReceita = async (dados) => {
    let previewWindow = window.printPreviewWindow;

    try {
        const qtdCopiasInput = document.getElementById('qtd-copias');
        const nr_copias = qtdCopiasInput ? parseInt(qtdCopiasInput.value) || 1 : 1;

        const dadosCompletos = {
            ...dados,
            nr_copias: nr_copias
        };

        console.log('Enviando dados para impressão de receita:', dadosCompletos);

        if (!previewWindow || previewWindow.closed) {
            previewWindow = window.open('about:blank', '_blank');
            window.printPreviewWindow = previewWindow;
        }

        if (!previewWindow) {
            exibirMensagem('Não foi possível abrir a pré-visualização. Verifique se o bloqueador de janelas pop-up está ativado.', 'error');
            return;
        }

        previewWindow.focus();

        const response = await fetch('/gerar-pdf-receita', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dadosCompletos),
        });

        console.log('Resposta do servidor de receita', response.status, response.statusText);

        if (response.ok) {
            const contentType = response.headers.get('Content-Type') || '';

            if (contentType.includes('application/pdf')) {
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                previewWindow.document.open();
                previewWindow.document.write(`
                    <html>
                    <head>
                        <title>Visualização de PDF</title>
                        <style>html, body {margin:0; height:100%; overflow:hidden;}</style>
                    </head>
                    <body>
                        <embed src="${url}" type="application/pdf" width="100%" height="100%" />
                        <script>
                            window.onload = function() {
                                window.focus();
                                setTimeout(function() { window.print(); }, 500);
                            };
                        <\/script>
                    </body>
                    </html>
                `);
                previewWindow.document.close();
                window.printPreviewWindow = null;
                setTimeout(() => URL.revokeObjectURL(url), 30000);
            } else {
                const htmlContent = await response.text();
                previewWindow.document.open();
                previewWindow.document.write(htmlContent);
                previewWindow.document.close();
                window.printPreviewWindow = null;
                previewWindow.focus();
            }

            exibirMensagem('Documento preparado para impressão!', 'success');
        } else {
            const status = `${response.status} ${response.statusText}`;
            const errorText = await response.text();
            console.error('Erro na resposta de receita:', status, errorText);
            const errorHtml = `
                <html>
                    <head>
                        <title>Erro ao gerar PDF da Receita</title>
                        <style>
                            body { font-family: Arial, sans-serif; padding: 24px; color: #333; }
                            h1 { color: #d32f2f; }
                            pre { white-space: pre-wrap; word-break: break-word; background: #f4f4f4; padding: 16px; border-radius: 8px; }
                        </style>
                    </head>
                    <body>
                        <h1>Erro ao gerar PDF da Receita</h1>
                        <p>O servidor retornou um erro ao tentar gerar o PDF.</p>
                        <p>Status: ${status}</p>
                        <pre>${errorText}</pre>
                    </body>
                </html>
            `;
            previewWindow.document.open();
            previewWindow.document.write(errorHtml);
            previewWindow.document.close();
            window.printPreviewWindow = null;
            return;
        }
    } catch (error) {
        console.error('Erro ao enviar dados de receita:', error);
        const errorHtml = `
            <html>
                <head>
                    <title>Erro ao gerar PDF da Receita</title>
                    <style>
                        body { font-family: Arial, sans-serif; padding: 24px; color: #333; }
                        h1 { color: #d32f2f; }
                        pre { white-space: pre-wrap; word-break: break-word; background: #f4f4f4; padding: 16px; border-radius: 8px; }
                    </style>
                </head>
                <body>
                    <h1>Erro ao gerar PDF da Receita</h1>
                    <p>Ocorreu um erro ao tentar gerar o PDF.</p>
                    <pre>${error.message}</pre>
                </body>
            </html>
        `;
        if (previewWindow && !previewWindow.closed) {
            previewWindow.document.open();
            previewWindow.document.write(errorHtml);
            previewWindow.document.close();
        }
        window.printPreviewWindow = null;
        exibirMensagem('Erro ao processar a solicitação', 'error');
    }
};

const botaoReceita = document.getElementById('botao-receita');
if (botaoReceita) {
    botaoReceita.addEventListener('click', () => {
        const dados = window.capturarValoresReceita();
        window.enviarDadosReceita(dados);
    });
}
