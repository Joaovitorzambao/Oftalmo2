import { exibirMensagem } from './flash_messages.js';
import { fetchAndPrint } from './print-utils.js';

document.addEventListener('DOMContentLoaded', () => {
    window.capturarValoresReceita = () => {
        let receita = '';

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

        return {
            receita,
            nm_pessoa_fisica: nmPessoaFisica,
            data_nascimento: dataNascimento,
            data_cpf: dataCpf
        };
    };

    window.enviarDadosReceita = async (dados) => {
        try {
            const qtdCopiasInput = document.getElementById('qtd-copias');
            const nr_copias = qtdCopiasInput ? parseInt(qtdCopiasInput.value) || 1 : 1;

            await fetchAndPrint('/gerar-pdf-receita', { ...dados, nr_copias });
            exibirMensagem('Documento preparado para impressão!', 'success');
        } catch (error) {
            console.error('Erro ao enviar dados:', error);
            exibirMensagem('Erro ao gerar documento para impressão', 'error');
        }
    };

    const botaoReceita = document.getElementById('botao-receita');
    if (botaoReceita) {
        botaoReceita.addEventListener('click', () => {
            window.enviarDadosReceita(window.capturarValoresReceita());
        });
    }
});
