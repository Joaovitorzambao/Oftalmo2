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

window.capturarValoresExames = () => {
    const exames = document.getElementById('textarea-exames')?.value || 'Não informado';
    const nmPessoaFisica = document.getElementById("nm_paciente")?.textContent?.trim() || '';
    const convenio = document.getElementById("nm-convenio")?.textContent?.trim() || '';

    const elementoPaciente = document.getElementById("nm_paciente");
    const dataNascimento = elementoPaciente?.dataset?.nascimento || '';
    const dataCpf = elementoPaciente?.dataset?.cpf || '';

    console.log('Capturando valores de exames', { exames, nmPessoaFisica, convenio, dataNascimento, dataCpf });

    return { exames, nmPessoaFisica, convenio, dataNascimento, dataCpf };
};

window.enviarDadosExames = async (dados) => {
    console.log('Iniciando geração de PDF de exames', dados);
    let previewWindow = window.printPreviewWindow;
    if (!previewWindow || previewWindow.closed) {
        previewWindow = window.open('about:blank', '_blank');
        window.printPreviewWindow = previewWindow;
    }

    if (!previewWindow) {
        alert('Não foi possível abrir a pré-visualização. Verifique se o bloqueador de janelas pop-up está ativado.');
        return;
    }

    previewWindow.focus();

    try {
        const response = await fetch('/gerar-pdf-exames', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados),
        });

        console.log('Resposta do servidor de exames', response.status, response.statusText);

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
        } else {
            const status = `${response.status} ${response.statusText}`;
            const errorText = await response.text();
            console.error('Erro no servidor de exames', status, errorText);
            const errorHtml = `
                <html>
                    <head>
                        <title>Erro ao gerar PDF de Exames</title>
                        <style>
                            body { font-family: Arial, sans-serif; padding: 24px; color: #333; }
                            h1 { color: #d32f2f; }
                            pre { white-space: pre-wrap; word-break: break-word; background: #f4f4f4; padding: 16px; border-radius: 8px; }
                        </style>
                    </head>
                    <body>
                        <h1>Erro ao gerar PDF de Exames</h1>
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
        }
    } catch (erro) {
        console.error('Erro ao enviar dados de exames:', erro);
        const errorHtml = `
            <html>
                <head>
                    <title>Erro ao gerar PDF de Exames</title>
                    <style>
                        body { font-family: Arial, sans-serif; padding: 24px; color: #333; }
                        h1 { color: #d32f2f; }
                        pre { white-space: pre-wrap; word-break: break-word; background: #f4f4f4; padding: 16px; border-radius: 8px; }
                    </style>
                </head>
                <body>
                    <h1>Erro ao gerar PDF de Exames</h1>
                    <p>Ocorreu um erro ao tentar gerar o PDF.</p>
                    <pre>${erro.message}</pre>
                </body>
            </html>
        `;
        if (previewWindow && !previewWindow.closed) {
            previewWindow.document.open();
            previewWindow.document.write(errorHtml);
            previewWindow.document.close();
        }
        window.printPreviewWindow = null;
    }
};

const botaoExames = document.getElementById('botao-exames');
if (botaoExames) {
    botaoExames.addEventListener('click', () => {
        const dados = window.capturarValoresExames();
        window.enviarDadosExames(dados);
    });
}
