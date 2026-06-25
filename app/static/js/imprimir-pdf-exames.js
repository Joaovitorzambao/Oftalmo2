import { fetchAndPrint } from './print-utils.js';

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

    return { exames, nmPessoaFisica, convenio, dataNascimento, dataCpf };
};

window.enviarDadosExames = async (dados) => {
    try {
        await fetchAndPrint('/gerar-pdf-exames', dados);
    } catch (erro) {
        console.error('Erro ao enviar dados de exames:', erro);
        exibirMensagem('Erro ao gerar documento para impressão', 'error');
    }
};

const botaoExames = document.getElementById('botao-exames');
if (botaoExames) {
    botaoExames.addEventListener('click', () => {
        window.enviarDadosExames(window.capturarValoresExames());
    });
}
