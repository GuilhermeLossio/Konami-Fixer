class DeckListEditor {
    constructor() {
        this.form = document.getElementById('deckForm');
        this.pdfViewer = document.getElementById('pdfViewer');
        this.toast = new bootstrap.Toast(document.getElementById('liveToast'));
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.updateSummary();
        // Configurar data atual como padrão
        document.getElementById('event_date').valueAsDate = new Date();
    }

    setupEventListeners() {
        // Atualizar PDF
        document.getElementById('btnAtualizar').addEventListener('click', () => {
            this.updatePDF();
        });

        // Limpar formulário
        document.getElementById('btnLimpar').addEventListener('click', () => {
            this.clearForm();
        });

        // Download do PDF
        document.getElementById('btnDownload').addEventListener('click', () => {
            this.downloadPDF();
        });

        // Atualizar summary quando quantidades mudam
        this.form.addEventListener('input', this.debounce(() => {
            this.updateSummary();
        }, 500));
    }

    async updatePDF() {
        const formData = new FormData(this.form);
        const fields = {};
        
        // Coletar dados básicos
        for (let [key, value] of formData.entries()) {
            if (value) fields[key] = value;
        }
        
        // Coletar cards do deck
        const deckData = this.collectDeckData();
        Object.assign(fields, deckData);

        try {
            const response = await fetch('/update_pdf', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ fields })
            });

            const result = await response.json();

            if (result.success) {
                this.pdfViewer.src = result.pdf_url;
                this.showToast('Deck List updated successfully!', 'success');
            } else {
                this.showToast('Error updating PDF: ' + result.error, 'danger');
            }
        } catch (error) {
            this.showToast('Connection error: ' + error, 'danger');
        }
    }

    collectDeckData() {
        const data = {};
        const sections = ['monster', 'spell', 'trap', 'side', 'extra'];
        
        sections.forEach(section => {
            const container = document.getElementById(`${section}-cards-container`);
            const rows = container.querySelectorAll('.card-row');
            
            rows.forEach((row, index) => {
                const qtyInput = row.querySelector('.card-qty');
                const nameInput = row.querySelector('.card-name');
                const qty = qtyInput.value.trim();
                const name = nameInput.value.trim();
                
                if (qty && name) {
                    data[`${section}_${index}_qty`] = qty;
                    data[`${section}_${index}_name`] = name;
                }
            });
        });
        
        return data;
    }

    updateSummary() {
        const monsterTotal = this.calculateTotal('monster');
        const spellTotal = this.calculateTotal('spell');
        const trapTotal = this.calculateTotal('trap');
        const sideTotal = this.calculateTotal('side');
        const extraTotal = this.calculateTotal('extra');
        const mainDeckTotal = monsterTotal + spellTotal + trapTotal;

        // Atualizar display
        document.getElementById('main-deck-total').textContent = mainDeckTotal;
        document.getElementById('monster-total').textContent = monsterTotal;
        document.getElementById('spell-total').textContent = spellTotal;
        document.getElementById('trap-total').textContent = trapTotal;
        document.getElementById('side-deck-total').textContent = sideTotal;
        document.getElementById('extra-deck-total').textContent = extraTotal;

        // Atualizar badges
        document.getElementById('monster-badge').textContent = monsterTotal;
        document.getElementById('spell-badge').textContent = spellTotal;
        document.getElementById('trap-badge').textContent = trapTotal;
        document.getElementById('side-badge').textContent = sideTotal;
        document.getElementById('extra-badge').textContent = extraTotal;
    }

    calculateTotal(type) {
        const container = document.getElementById(`${type}-cards-container`);
        const qtyInputs = container.querySelectorAll('.card-qty');
        let total = 0;
        
        qtyInputs.forEach(input => {
            const value = parseInt(input.value) || 0;
            total += value;
        });
        
        return total;
    }

    clearForm() {
        const modal = new bootstrap.Modal(document.getElementById('clearModal') || this.createClearModal());
        modal.show();
    }

    createClearModal() {
        const modalHTML = `
            <div class="modal fade" id="clearModal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Clear Form</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            Are you sure you want to clear all fields?
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                            <button type="button" class="btn btn-danger" id="confirmClear">Clear All</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        const modal = new bootstrap.Modal(document.getElementById('clearModal'));
        document.getElementById('confirmClear').addEventListener('click', () => {
            this.performClear();
            modal.hide();
        });
        
        return modal;
    }

    performClear() {
        this.form.reset();
        
        // Limpar cards (manter uma linha em cada seção)
        const containers = ['monster', 'spell', 'trap', 'side', 'extra'];
        containers.forEach(containerId => {
            const container = document.getElementById(`${containerId}-cards-container`);
            container.innerHTML = `
                <div class="card-row row g-2 align-items-center mb-2">
                    <div class="col-2">
                        <input type="number" class="form-control card-qty" placeholder="Qty" min="1" max="3">
                    </div>
                    <div class="col-9">
                        <input type="text" class="form-control card-name" placeholder="Card Name">
                    </div>
                    <div class="col-1">
                        <button type="button" class="btn btn-outline-danger btn-sm remove-card" onclick="removeCardRow(this)">
                            <i class="bi bi-x"></i>
                        </button>
                    </div>
                </div>
            `;
        });
        
        // Resetar data para hoje
        document.getElementById('event_date').valueAsDate = new Date();
        
        this.updateSummary();
        this.updatePDF();
        this.showToast('All fields cleared successfully!', 'info');
    }

    downloadPDF() {
        if (this.pdfViewer.src && !this.pdfViewer.src.includes('decklist.pdf')) {
            const link = document.createElement('a');
            link.href = this.pdfViewer.src;
            link.download = 'decklist_completed.pdf';
            link.click();
            this.showToast('Download started!', 'success');
        } else {
            this.showToast('Please fill out the form and update the PDF first!', 'warning');
        }
    }

    showToast(message, type = 'info') {
        const toast = document.getElementById('liveToast');
        const toastHeader = toast.querySelector('.toast-header');
        const toastBody = toast.querySelector('.toast-body');
        
        // Configurar ícone e cor baseado no tipo
        let icon = 'bi-info-circle-fill';
        let bgColor = 'text-primary';
        
        switch(type) {
            case 'success':
                icon = 'bi-check-circle-fill';
                bgColor = 'text-success';
                break;
            case 'danger':
                icon = 'bi-exclamation-circle-fill';
                bgColor = 'text-danger';
                break;
            case 'warning':
                icon = 'bi-exclamation-triangle-fill';
                bgColor = 'text-warning';
                break;
            case 'info':
                icon = 'bi-info-circle-fill';
                bgColor = 'text-info';
                break;
        }
        
        toastHeader.querySelector('i').className = `${icon} ${bgColor} me-2`;
        toastBody.textContent = message;
        
        this.toast.show();
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

// Funções globais para manipulação de cards
function addCardRow(type) {
    const container = document.getElementById(`${type}-cards-container`);
    const newRow = document.createElement('div');
    newRow.className = 'card-row row g-2 align-items-center mb-2';
    newRow.innerHTML = `
        <div class="col-2">
            <input type="number" class="form-control card-qty" placeholder="Qty" min="1" max="3">
        </div>
        <div class="col-9">
            <input type="text" class="form-control card-name" placeholder="Card Name">
        </div>
        <div class="col-1">
            <button type="button" class="btn btn-outline-danger btn-sm remove-card" onclick="removeCardRow(this)">
                <i class="bi bi-x"></i>
            </button>
        </div>
    `;
    container.appendChild(newRow);
    
    // Rolar para a nova linha
    newRow.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function removeCardRow(button) {
    const row = button.closest('.card-row');
    const container = row.parentElement;
    
    // Não remover se for a última linha
    if (container.querySelectorAll('.card-row').length > 1) {
        row.remove();
        // Atualizar summary após remover
        if (window.deckListEditor) {
            window.deckListEditor.updateSummary();
        }
    } else {
        // Se for a última linha, apenas limpar os campos
        row.querySelector('.card-qty').value = '';
        row.querySelector('.card-name').value = '';
    }
}

// CSS adicional para cores personalizadas
const style = document.createElement('style');
style.textContent = `
    .bg-purple { background-color: #6f42c1 !important; }
    .btn-outline-purple { 
        border-color: #6f42c1; 
        color: #6f42c1;
    }
    .btn-outline-purple:hover {
        background-color: #6f42c1;
        color: white;
    }
`;
document.head.appendChild(style);

// Inicializar quando o DOM carregar
document.addEventListener('DOMContentLoaded', () => {
    window.deckListEditor = new DeckListEditor();
});