/**
 * Универсальная форма для добавления и редактирования поставщика
 * Паттерн MVC - View, контроллеры определяют режим работы
 */

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('supplierForm');
    const submitBtn = document.getElementById('submitBtn');
    const cancelBtn = document.getElementById('cancelBtn');
    const formMessage = document.getElementById('formMessage');
    const loadingMessage = document.getElementById('loadingMessage');
    const errorMessage = document.getElementById('errorMessage');

    // Элементы для динамического изменения
    const pageTitle = document.getElementById('pageTitle');
    const formTitle = document.getElementById('formTitle');
    const formSubtitle = document.getElementById('formSubtitle');

    // Поля формы
    const supplierIdInput = document.getElementById('supplierId');
    const formModeInput = document.getElementById('formMode');
    const nameInput = document.getElementById('name');
    const phoneInput = document.getElementById('phone');
    const addressInput = document.getElementById('address');

    // Элементы для отображения ошибок
    const nameError = document.getElementById('nameError');
    const phoneError = document.getElementById('phoneError');
    const addressError = document.getElementById('addressError');

    // Получаем параметры из URL
    const urlParams = new URLSearchParams(window.location.search);
    const mode = urlParams.get('mode'); // 'add' или 'edit'
    const supplierId = urlParams.get('id'); // только для режима edit

    // Инициализация формы в зависимости от режима
    initializeForm(mode, supplierId);

    /**
     * Инициализация формы
     */
    function initializeForm(mode, id) {
        formModeInput.value = mode;

        if (mode === 'add') {
            // Режим добавления
            pageTitle.textContent = 'Добавить поставщика';
            formTitle.textContent = 'Добавление нового поставщика';
            formSubtitle.textContent = 'Заполните все обязательные поля';
            submitBtn.textContent = 'Добавить поставщика';
            
            // Форма пустая, сразу показываем
            form.style.display = 'block';
            
        } else if (mode === 'edit') {
            // Режим редактирования
            if (!id) {
                showError('Не указан ID поставщика для редактирования');
                return;
            }
            
            pageTitle.textContent = 'Редактировать поставщика';
            formTitle.textContent = 'Редактирование поставщика';
            formSubtitle.textContent = 'Измените необходимые поля';
            submitBtn.textContent = 'Сохранить изменения';
            
            // Загружаем данные через контроллер
            loadSupplierData(id);
            
        } else {
            showError('Некорректный режим работы формы');
        }
    }

    /**
     * Загрузка данных поставщика (только для режима edit)
     */
    async function loadSupplierData(id) {
        loadingMessage.style.display = 'block';
        form.style.display = 'none';

        try {
            const response = await fetch(`/api/suppliers/${id}`);
            const result = await response.json();

            if (result.success) {
                // Заполняем форму данными
                const supplier = result.supplier;
                supplierIdInput.value = supplier.supplier_id;
                nameInput.value = supplier.name;
                phoneInput.value = supplier.phone;
                addressInput.value = supplier.address || '';

                // Показываем форму
                loadingMessage.style.display = 'none';
                form.style.display = 'block';
            } else {
                showError(result.error || 'Ошибка при загрузке данных');
            }
        } catch (error) {
            showError('Ошибка соединения с сервером: ' + error.message);
        }
    }

    /**
     * Показать ошибку загрузки
     */
    function showError(message) {
        loadingMessage.style.display = 'none';
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
    }

    /**
     * Валидация на стороне клиента
     */
    function validateForm() {
        let isValid = true;
        clearErrors();

        // Валидация имени
        const name = nameInput.value.trim();
        if (!name) {
            showFieldError(nameInput, nameError, 'Поле обязательно для заполнения');
            isValid = false;
        } else if (name.length > 100) {
            showFieldError(nameInput, nameError, 'Максимум 100 символов');
            isValid = false;
        } else if (!/^(?=.*[a-zA-Zа-яА-ЯёЁ])[a-zA-Zа-яА-ЯёЁ0-9\s\-]+$/.test(name)) {
            showFieldError(nameInput, nameError, 'Только буквы, цифры, пробелы и дефисы');
            isValid = false;
        }

        // Валидация телефона
        const phone = phoneInput.value.trim();
        if (!phone) {
            showFieldError(phoneInput, phoneError, 'Поле обязательно для заполнения');
            isValid = false;
        } else if (!/^[\+]?[78]?[\s\-]?[\(]?\d{3}[\)]?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$/.test(phone)) {
            showFieldError(phoneInput, phoneError, 'Неверный формат телефона');
            isValid = false;
        }

        // Валидация адреса
        const address = addressInput.value.trim();
        if (address && address.length > 200) {
            showFieldError(addressInput, addressError, 'Максимум 200 символов');
            isValid = false;
        }

        return isValid;
    }

    /**
     * Показать ошибку для конкретного поля
     */
    function showFieldError(input, errorElement, message) {
        input.classList.add('error');
        errorElement.textContent = message;
        errorElement.classList.add('visible');
    }

    /**
     * Очистить все ошибки
     */
    function clearErrors() {
        [nameInput, phoneInput, addressInput].forEach(input => {
            input.classList.remove('error');
        });
        [nameError, phoneError, addressError].forEach(error => {
            error.textContent = '';
            error.classList.remove('visible');
        });
        formMessage.style.display = 'none';
        formMessage.className = '';
    }

    /**
     * Отправка формы
     */
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Клиентская валидация
        if (!validateForm()) {
            return;
        }

        // Отключаем кнопку и показываем загрузку
        submitBtn.disabled = true;
        submitBtn.classList.add('loading');

        const mode = formModeInput.value;
        const formData = {
            name: nameInput.value.trim(),
            phone: phoneInput.value.trim(),
            address: addressInput.value.trim() || null
        };

        try {
            let response, messageType;

            if (mode === 'add') {
                // Добавление через POST
                response = await fetch('/api/suppliers/add', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(formData)
                });
                messageType = 'supplier_added';
                
            } else if (mode === 'edit') {
                // Редактирование через PUT
                formData.supplier_id = parseInt(supplierIdInput.value);
                response = await fetch('/api/suppliers/edit', {
                    method: 'PUT',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(formData)
                });
                messageType = 'supplier_updated';
            }

            const result = await response.json();

            if (result.success) {
                // Успех
                const successMessage = mode === 'add' 
                    ? 'Поставщик успешно добавлен!'
                    : 'Поставщик успешно обновлен!';
                
                formMessage.textContent = result.message || successMessage;
                formMessage.className = 'success';

                // Уведомляем родительское окно
                if (window.opener && !window.opener.closed) {
                    window.opener.postMessage({
                        type: messageType,
                        supplier_id: result.supplier_id || formData.supplier_id
                    }, '*');
                }

                // Закрываем окно через 2 секунды
                setTimeout(() => {
                    window.close();
                }, 2000);
                
            } else {
                // Ошибка валидации
                formMessage.textContent = result.error || 'Ошибка при сохранении данных';
                formMessage.className = 'error';

                // Показываем ошибки для полей
                if (result.validation_errors) {
                    if (result.validation_errors.name) {
                        showFieldError(nameInput, nameError, result.validation_errors.name);
                    }
                    if (result.validation_errors.phone) {
                        showFieldError(phoneInput, phoneError, result.validation_errors.phone);
                    }
                    if (result.validation_errors.address) {
                        showFieldError(addressInput, addressError, result.validation_errors.address);
                    }
                }
            }
        } catch (error) {
            formMessage.textContent = 'Ошибка соединения с сервером: ' + error.message;
            formMessage.className = 'error';
        } finally {
            // Включаем кнопку обратно
            submitBtn.disabled = false;
            submitBtn.classList.remove('loading');
        }
    });

    /**
     * Кнопка отмены
     */
    cancelBtn.addEventListener('click', function() {
        if (confirm('Вы уверены? Все несохраненные изменения будут потеряны.')) {
            window.close();
        }
    });

    /**
     * Очистка ошибок при вводе
     */
    nameInput.addEventListener('input', function() {
        nameInput.classList.remove('error');
        nameError.classList.remove('visible');
    });

    phoneInput.addEventListener('input', function() {
        phoneInput.classList.remove('error');
        phoneError.classList.remove('visible');
    });

    addressInput.addEventListener('input', function() {
        addressInput.classList.remove('error');
        addressError.classList.remove('visible');
    });

    /**
     * Автоформатирование телефона
     */
    phoneInput.addEventListener('blur', function() {
        let phone = phoneInput.value.replace(/\D/g, '');
        if (phone.length === 11 && phone[0] === '8') {
            phone = '7' + phone.substr(1);
        }
        if (phone.length === 11 && phone[0] === '7') {
            phoneInput.value = `+7 (${phone.substr(1, 3)}) ${phone.substr(4, 3)}-${phone.substr(7, 2)}-${phone.substr(9, 2)}`;
        }
    });
});

