// Este arquivo cuida do visual e de como o site se comporta.
// Ele muda o tema, esconde o cabeçalho e ajuda a formatar datas.

// Obtém o botão principal responsável por trocar o tema da página.
const button = document.getElementById("theme-btn");

// Obtém o segundo botão que também pode trocar o tema.
const button2 = document.getElementById("theme-btn2");

// Obtém o ícone que muda entre sol e lua conforme o tema.
const icon = document.getElementById("theme-icon");

// Armazena a última posição da rolagem da página.
let lastScroll = 0;

// Seleciona o elemento <header> da página.
const header = document.querySelector("header");

// Função que verifica se o usuário está usando um dispositivo móvel.
const isMobileNavigation = () => {

    // Retorna true se a largura da tela for até 768px,
    // se o dispositivo possuir ponteiro de toque
    // ou se houver suporte para múltiplos toques.
    return window.matchMedia("(max-width: 768px)").matches ||
           window.matchMedia("(pointer: coarse)").matches ||
           navigator.maxTouchPoints > 0;
};

// Seleciona todos os links do menu mobile.
const mobileLinks = document.querySelectorAll(".mobile-nav-link");

// Percorre todos os links do menu mobile.
mobileLinks.forEach((link) => {

    // Adiciona um evento de clique para cada link.
    link.addEventListener("click", (event) => {

        // Se não estiver em um dispositivo móvel,
        // permite a navegação padrão.
        if (!isMobileNavigation()) return;

        // Obtém o endereço específico para dispositivos móveis.
        const mobileHref = link.dataset.mobileHref;

        // Se não existir um endereço alternativo, encerra a função.
        if (!mobileHref) return;

        // Impede a navegação padrão do navegador.
        event.preventDefault();

        // Redireciona para o endereço específico do dispositivo móvel.
        window.location.href = mobileHref;
    });
});

// Monitora a rolagem da página.
window.addEventListener("scroll", () => {

    // Guarda a posição atual da barra de rolagem.
    const currentScroll = window.scrollY;

    // Se estiver rolando para baixo e já passou de 60 pixels,
    // esconde o cabeçalho.
    if (currentScroll > lastScroll && currentScroll > 60) {
        header.classList.add("hide");
    } else {

        // Caso contrário, mostra novamente o cabeçalho.
        header.classList.remove("hide");
    }

    // Atualiza a última posição da rolagem.
    lastScroll = currentScroll;
});

// Função responsável por aplicar o tema claro ou escuro.
const setTheme = (dark) => {

    // Adiciona ou remove a classe do tema escuro.
    document.body.classList.toggle("dark-theme", dark);

    // Exibe o ícone de sol quando o tema estiver escuro.
    icon.classList.toggle("fa-sun", dark);

    // Exibe o ícone de lua quando o tema estiver claro.
    icon.classList.toggle("fa-moon", !dark);

    // Salva a preferência do usuário no navegador.
    localStorage.setItem("theme", dark ? "dark" : "light");
};

// Ao carregar a página, verifica o tema salvo
// e aplica automaticamente.
setTheme(localStorage.getItem("theme") === "dark");

// Verifica se o primeiro botão existe.
if (button) {

    // Ao clicar no botão, alterna entre tema claro e escuro.
    button.addEventListener("click", () => {

        setTheme(!document.body.classList.contains("dark-theme"));
    });
}

// Verifica se o segundo botão existe.
if (button2) {

    // Também alterna o tema ao ser clicado.
    button2.addEventListener("click", () => {

        setTheme(!document.body.classList.contains("dark-theme"));
    });
}

// Função que formata automaticamente uma data
// para o padrão DD/MM/AAAA.
function formatarData(input) {

    // Remove qualquer caractere que não seja número.
    let valor = input.value.replace(/\D/g, '');

    // Insere a primeira barra após o dia.
    if (valor.length > 2)
        valor = valor.slice(0, 2) + '/' + valor.slice(2);

    // Insere a segunda barra após o mês.
    if (valor.length > 5)
        valor = valor.slice(0, 5) + '/' + valor.slice(5);

    // Limita o campo a 10 caracteres (DD/MM/AAAA).
    input.value = valor.slice(0, 10);
}

// Função que garante que um campo sempre comece
// com um determinado prefixo.
function manterPrefixo(input, prefixo) {

    // Se o valor digitado não começar com o prefixo esperado.
    if (!input.value.startsWith(prefixo)) {

        // Recoloca automaticamente o prefixo.
        input.value = prefixo;
    }
}