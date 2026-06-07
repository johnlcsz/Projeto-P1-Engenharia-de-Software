const btnExplorar = document.getElementById('btn-explorar')
const searchBar = document.getElementById('search-bar')
const searchFechar = document.getElementById('search-fechar')
const searchInput = document.getElementById('search-input')

if (btnExplorar) {
    btnExplorar.addEventListener('click', () => {
        btnExplorar.style.opacity = '0'
        btnExplorar.style.transition = 'opacity 0.2s ease'
        setTimeout(() => { btnExplorar.style.display = 'none' }, 200)
        searchBar.classList.add('ativa')
        setTimeout(() => searchInput.focus(), 400)
    })
}

if (searchFechar) {
    searchFechar.addEventListener('click', () => {
        searchBar.classList.remove('ativa')
        searchInput.value = ''
        setTimeout(() => {
            btnExplorar.style.display = 'block'
            btnExplorar.style.opacity = '0'
            setTimeout(() => { btnExplorar.style.opacity = '1' }, 50)
        }, 300)
    })
}

const modalLogin = document.getElementById("modal-login")
const modalCadastro = document.getElementById("modal-cadastro")
const btnLogin = document.getElementById("btn-login")
const btnCadastro = document.getElementById("btn-cadastro")
const closeLogin = document.getElementById("close-login")
const closeCadastro = document.getElementById("close-cadastro")
const irCadastro = document.getElementById("ir-cadastro")
const irLogin = document.getElementById("ir-login")

function abrirModal(modal) {
    modal.classList.add("active")
}

function fecharModal(modal) {
    modal.classList.remove("active")
}

if (btnLogin) {
    btnLogin.addEventListener("click", () => {
        abrirModal(modalLogin)
    })
}

if (btnCadastro) {
    btnCadastro.addEventListener("click", () => {
        abrirModal(modalCadastro)
    })
}

if (closeLogin) {
    closeLogin.addEventListener("click", () => {
        fecharModal(modalLogin)
    })
}

if (closeCadastro) {
    closeCadastro.addEventListener("click", () => {
        fecharModal(modalCadastro)
    })
}

if (irCadastro) {
    irCadastro.addEventListener("click", () => {
        fecharModal(modalLogin)
        abrirModal(modalCadastro)
    })
}

if (irLogin) {
    irLogin.addEventListener("click", () => {
        fecharModal(modalCadastro)
        abrirModal(modalLogin)
    })
}

window.addEventListener("click", (e) => {
    if (e.target === modalLogin) fecharModal(modalLogin)
    if (e.target === modalCadastro) fecharModal(modalCadastro)
})

document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
        fecharModal(modalLogin)
        fecharModal(modalCadastro)
    }
})

const urlParams = new URLSearchParams(window.location.search)
const modalParam = urlParams.get('modal')

if (modalParam === 'login' && modalLogin) {
    abrirModal(modalLogin)
}

if (modalParam === 'register' && modalCadastro) {
    abrirModal(modalCadastro)
}