import { exibirMensagem } from './flash_messages.js';

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

    window.capturarValoresReceita = () => {
        let receita = '';
        
        // Capturar apenas da aba ativa
        const activeTab = document.querySelector('.receita-tab.active');
        const activeTabId = activeTab ? activeTab.dataset.tab : 'receita1';
        
        const textareaReceita = document.getElementById(activeTabId === 'receita1' ? 'receita' : 'receita2');
        const nmPessoaFisica = document.getElementById("nm_paciente").textContent.trim();
        const elementoPaciente = document.getElementById("nm_paciente");
        const dataNascimento = elementoPaciente.dataset.nascimento;
        const dataCpf = elementoPaciente.dataset.cpf;

        if (textareaReceita && textareaReceita.offsetParent !== null) {
            receita = textareaReceita.value.trim();
        }

        // Retornar com os nomes padronizados
        return { 
            receita, 
            nm_pessoa_fisica: nmPessoaFisica,  // ← Padronizado
            data_nascimento: dataNascimento,    // ← Padronizado
            data_cpf: dataCpf                   // ← Padronizado
        };
    };

    window.enviarDadosReceita = async (dados) => {
        try {
            const qtdCopiasInput = document.getElementById('qtd-copias');
            const nr_copias = qtdCopiasInput ? parseInt(qtdCopiasInput.value) || 1 : 1;

            const dadosCompletos = {
                ...dados,
                nr_copias: nr_copias
            };

            console.log('Enviando dados para impressão:', dadosCompletos);

            const previewWindow = window.open('', '_blank');
            if (!previewWindow) {
                exibirMensagem('Não foi possível abrir a pré-visualização. Verifique se o bloqueador de janelas pop-up está ativado.', 'error');
                return;
            }

            const response = await fetch('/gerar-pdf-receita', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dadosCompletos),
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

                exibirMensagem('Documento preparado para impressão!', 'success');
            } else {
                previewWindow.close();
                const errorText = await response.text();
                console.error('Erro na resposta:', errorText);
                exibirMensagem('Erro ao gerar o PDF da receita', 'error');
            }
                const errorText = await response.text();
                console.error('Erro na resposta:', errorText);
                exibirMensagem('Erro ao gerar o PDF da receita', 'error');
            }
        } catch (error) {
            console.error('Erro ao enviar dados:', error);
            exibirMensagem('Erro ao processar a solicitação', 'error');
        }
    };

    const botaoReceita = document.getElementById('botao-receita');
    botaoReceita.addEventListener('click', () => {
        const dados = window.capturarValoresReceita();

        window.enviarDadosReceita(dados);
    });
});