document.addEventListener('DOMContentLoaded', () => {
    const flashMessageDiv = document.getElementById("flash-message");

    const exibirMensagem = (mensagem, tipo = "success") => {
        flashMessageDiv.style.display = "block";
        flashMessageDiv.textContent = mensagem;

        if (tipo === "success") {
            flashMessageDiv.style.backgroundColor = "#d4edda";
            flashMessageDiv.style.color = "#155724";
        } else {
            flashMessageDiv.style.backgroundColor = "#f8d7da";
            flashMessageDiv.style.color = "#721c24";
        }
        setTimeout(() => {
            flashMessageDiv.style.opacity = "0";
            setTimeout(() => {
                flashMessageDiv.style.display = "none"; 
                flashMessageDiv.style.opacity = "1";
            }, 1000);
        }, 3000);
    };
        
    window.capturarValoresResumo = () => {
        const elementoAtendimento = document.getElementById("nr_atendimento");
        if (!elementoAtendimento) {
            console.error("Elemento nr_atendimento não encontrado");
            return { nrAtendimento: null };
        }
        const nrAtendimento = elementoAtendimento.textContent;
        return { nrAtendimento };
    };

    window.enviarDadosResumo = async (dados) => {
        try {
            const previewWindow = window.open('', '_blank');
            if (!previewWindow) {
                alert('Não foi possível abrir a pré-visualização. Verifique se o bloqueador de janelas pop-up está ativado.');
                return;
            }

            const response = await fetch('/gerar-pdf-resumo', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dados),
            });

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
                    setTimeout(() => URL.revokeObjectURL(url), 30000);
                } else {
                    const htmlContent = await response.text();
                    previewWindow.document.open();
                    previewWindow.document.write(htmlContent);
                    previewWindow.document.close();
                    previewWindow.focus();
                }
            } else {
                previewWindow.close();
                console.error('Erro ao gerar o PDF:', response);
                exibirMensagem("Erro ao gerar o PDF.", "error");
            }
        } catch (erro) {
            console.error('Erro ao enviar dados:', erro);
            exibirMensagem("Erro ao gerar o resumo.", "error");
        }
    };

    const botaoResumo = document.getElementById('botao-resumo');
    if (botaoResumo) {
        botaoResumo.addEventListener('click', () => {
            const dados = window.capturarValoresResumo();
            window.enviarDadosResumo(dados);
        });
    }
});