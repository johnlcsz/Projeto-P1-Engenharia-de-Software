const stars = document.querySelectorAll('.star')
const notaInput = document.getElementById('nota-input')

if (stars.length > 0) {
    let notaSelecionada = 0

    stars.forEach(star => {
        star.addEventListener('mouseover', () => {
            const val = parseInt(star.dataset.value)
            stars.forEach(s => {
                s.classList.toggle('on', parseInt(s.dataset.value) <= val)
            })
        })

        star.addEventListener('mouseout', () => {
            stars.forEach(s => {
                s.classList.toggle('on', parseInt(s.dataset.value) <= notaSelecionada)
            })
        })

        star.addEventListener('click', () => {
            const val = parseInt(star.dataset.value)
            if (notaSelecionada === val) {
                notaSelecionada = 0
                notaInput.value = 0
            } else {
                notaSelecionada = val
                notaInput.value = val
            }
            stars.forEach(s => {
                s.classList.toggle('on', parseInt(s.dataset.value) <= notaSelecionada)
            })
        })
    })
}

const btnCadastroDet = document.getElementById('btn-cadastro-det')

if (btnCadastroDet) {
    btnCadastroDet.addEventListener('click', () => {
        const modal = document.getElementById('modal-cadastro')
        if (modal) modal.classList.add('active')
    })
}