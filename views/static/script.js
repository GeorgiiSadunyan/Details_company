/**
 * Клиентская часть приложения для управления поставщиками
 * Паттерн MVC - это View, вся логика на стороне сервера (Controller)
 */

let currentPage = 1;
const pageSize = 10;

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    loadSuppliers(currentPage);
    setupEventListeners();
});

/**
 * Настройка обработчиков событий
 */
function setupEventListeners() {
    // Кнопка обновления
    document.getElementById('refreshBtn').addEventListener('click', function() {
        loadSuppliers(currentPage);
    });

    // Кнопка добавления
    document.getElementById('addBtn').addEventListener('click', function() {
        // TODO: будет реализовано в следующих пунктах ЛР
        alert('Функция добавления будет реализована в п.2 ЛР');
    });

    // Закрытие модального окна
    const modal = document.getElementById('detailsModal');
    const closeBtn = modal.querySelector('.close');
    
    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    // Закрытие по клику вне модального окна
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
}

/**
 * Загрузка списка поставщиков (краткая информация)
 * Реализация паттерна Observer - данные приходят через уведомление от Subject
 */
async function loadSuppliers(page) {
    const tableBody = document.getElementById('suppliersTableBody');
    const infoText = document.getElementById('infoText');
    
    // Показываем индикатор загрузки
    tableBody.innerHTML = '<tr><td colspan="3" class="loading">Загрузка данных</td></tr>';
    infoText.textContent = 'Загрузка...';

    try {
        // Запрос к контроллеру для получения данных
        const response = await fetch(`/api/suppliers?page=${page}&page_size=${pageSize}`);
        const data = await response.json();

        if (data.success) {
            displaySuppliers(data.items);
            displayPagination(data.page, data.total_pages);
            infoText.textContent = `Показано ${data.items.length} из ${data.total_count} поставщиков`;
        } else {
            showError(tableBody, data.error);
        }
    } catch (error) {
        showError(tableBody, 'Ошибка загрузки данных: ' + error.message);
    }
}

/**
 * Отображение списка поставщиков в таблице
 */
function displaySuppliers(suppliers) {
    const tableBody = document.getElementById('suppliersTableBody');
    
    if (suppliers.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="3" style="text-align: center;">Нет данных для отображения</td></tr>';
        return;
    }

    tableBody.innerHTML = suppliers.map(supplier => `
        <tr onclick="showDetails(${supplier.supplier_id})">
            <td>${supplier.supplier_id}</td>
            <td>${escapeHtml(supplier.name)}</td>
            <td class="action-buttons">
                <button class="btn btn-info" onclick="event.stopPropagation(); showDetails(${supplier.supplier_id})">
                    Подробнее
                </button>
            </td>
        </tr>
    `).join('');
}

/**
 * Показать полную информацию о поставщике в модальном окне
 * Паттерн Observer - при выборе элемента Subject уведомляет наблюдателей
 */
async function showDetails(supplierId) {
    const modal = document.getElementById('detailsModal');
    const detailsContent = document.getElementById('detailsContent');
    
    // Показываем модальное окно с индикатором загрузки
    modal.style.display = 'block';
    detailsContent.innerHTML = '<div class="loading">Загрузка информации</div>';

    try {
        // Запрос полной информации к контроллеру
        const response = await fetch(`/api/suppliers/${supplierId}`);
        const data = await response.json();

        if (data.success) {
            const supplier = data.supplier;
            detailsContent.innerHTML = `
                <div class="detail-item">
                    <span class="detail-label">ID:</span>
                    <span class="detail-value">${supplier.supplier_id}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Наименование:</span>
                    <span class="detail-value">${escapeHtml(supplier.name)}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Телефон:</span>
                    <span class="detail-value">${escapeHtml(supplier.phone)}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Адрес:</span>
                    <span class="detail-value">${supplier.address ? escapeHtml(supplier.address) : 'Не указан'}</span>
                </div>
            `;
        } else {
            detailsContent.innerHTML = `<div class="error-message">${data.error}</div>`;
        }
    } catch (error) {
        detailsContent.innerHTML = `<div class="error-message">Ошибка загрузки: ${error.message}</div>`;
    }
}

/**
 * Отображение пагинации
 */
function displayPagination(currentPageNum, totalPages) {
    const pagination = document.getElementById('pagination');
    
    if (totalPages <= 1) {
        pagination.innerHTML = '';
        return;
    }

    let html = '';
    
    // Кнопка "Назад"
    html += `<button ${currentPageNum <= 1 ? 'disabled' : ''} 
             onclick="changePage(${currentPageNum - 1})">← Назад</button>`;

    // Номера страниц
    for (let i = 1; i <= totalPages; i++) {
        // Показываем только некоторые страницы (чтобы не было слишком много кнопок)
        if (i === 1 || i === totalPages || (i >= currentPageNum - 2 && i <= currentPageNum + 2)) {
            html += `<button class="${i === currentPageNum ? 'active' : ''}" 
                     onclick="changePage(${i})">${i}</button>`;
        } else if (i === currentPageNum - 3 || i === currentPageNum + 3) {
            html += '<span>...</span>';
        }
    }

    // Кнопка "Вперед"
    html += `<button ${currentPageNum >= totalPages ? 'disabled' : ''} 
             onclick="changePage(${currentPageNum + 1})">Вперед →</button>`;

    pagination.innerHTML = html;
}

/**
 * Изменить текущую страницу
 */
function changePage(page) {
    currentPage = page;
    loadSuppliers(page);
}

/**
 * Показать ошибку
 */
function showError(element, message) {
    element.innerHTML = `<tr><td colspan="3"><div class="error-message">${escapeHtml(message)}</div></td></tr>`;
}

/**
 * Экранирование HTML для предотвращения XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}


