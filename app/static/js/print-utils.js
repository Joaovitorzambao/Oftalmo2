/**
 * Imprime HTML em iframe oculto na mesma página (sem abrir nova aba).
 * Comportamento equivalente ao window.print() do editar-exames.
 */
export function printHtmlInFrame(htmlContent) {
    return new Promise((resolve, reject) => {
        let frame = document.getElementById('iframe-impressao');
        if (!frame) {
            frame = document.createElement('iframe');
            frame.id = 'iframe-impressao';
            frame.setAttribute('title', 'Impressão');
            frame.style.cssText = 'position:fixed;width:0;height:0;border:0;visibility:hidden';
            document.body.appendChild(frame);
        }

        const blob = new Blob([htmlContent], { type: 'text/html;charset=utf-8' });
        const url = URL.createObjectURL(blob);

        frame.onload = () => {
            try {
                frame.contentWindow.focus();
                frame.contentWindow.print();
                resolve();
            } catch (err) {
                reject(err);
            } finally {
                setTimeout(() => URL.revokeObjectURL(url), 60000);
            }
        };

        frame.onerror = () => {
            URL.revokeObjectURL(url);
            reject(new Error('Erro ao carregar documento para impressão'));
        };

        frame.src = url;
    });
}

export async function fetchAndPrint(url, payload) {
    const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...payload, formato: 'html' }),
    });

    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText || `Erro ao gerar documento (${response.status})`);
    }

    const htmlContent = await response.text();
    await printHtmlInFrame(htmlContent);
}
