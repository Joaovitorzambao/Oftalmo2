import { fetchAndPrint } from './print-utils.js';

function positiveSimbol(val) {
    return ((typeof val == 'string') ? Number(val) : val) > 0 ? '+' : '';
}

window.capturarValoresOculos = () => {
    let tipo = '';
    let valores = {};
    let adicao = '';
    let observacao = '';

    const nmPessoaFisica = document.getElementById("nm_paciente").textContent.trim();
    const elementoPaciente = document.getElementById("nm_paciente");
    const dataNascimento = elementoPaciente.dataset.nascimento;
    const dataCpf = elementoPaciente.dataset.cpf;

    const camposDinamicos = document.querySelectorAll('.dinamica');
    const camposEstaticos = document.querySelectorAll('.estatica');

    if (camposDinamicos[0]?.offsetParent !== null) {
        tipo = 'dinamica';
        valores = extrairValores('.dinamica');
        const campoAdicao = document.querySelector('.adicao');
        if (campoAdicao) {
            adicao = campoAdicao.value.trim() || 'Não informado';
        }
    } else if (camposEstaticos[0]?.offsetParent !== null) {
        tipo = 'estatica';
        valores = extrairValores('.estatica');
    }

    const campoObservacao = document.querySelector('.ds_observacao_refracao');
    if (campoObservacao) {
        observacao = campoObservacao.value.trim() || 'Não informado';
    }

    return { tipo, valores, adicao, observacao, nmPessoaFisica, dataNascimento, dataCpf };
};

document.addEventListener('DOMContentLoaded', () => {
    const flashMessageDiv = document.getElementById("flash-message");

    const exibirMensagem = (mensagem, tipo = "success") => {
        if (!flashMessageDiv) return;
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

    window.extrairValores = (classe) => {
        const campos = document.querySelectorAll(`${classe} input`);
        const dados = {};

        campos.forEach((campo) => {
            dados[campo.name] = campo.value || null;
        });

        const elementoData = document.getElementById('data-agenda-display');
        dados['dt_atendimento'] = elementoData ? elementoData.textContent.trim() : null;
        return dados;
    };

    window.enviarDados = async (dados) => {
        try {
            await fetchAndPrint('/gerar-pdf-oculos', dados);
        } catch (erro) {
            console.error('Erro ao enviar dados:', erro);
            exibirMensagem("Erro ao gerar o documento para impressão.", "error");
        }
    };

    const botao = document.getElementById('botao-oculos');
    if (botao) {
        botao.addEventListener('click', () => {
            window.enviarDados(window.capturarValoresOculos());
        });
    }
});
