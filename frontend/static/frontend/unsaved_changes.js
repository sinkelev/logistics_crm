document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    let formChanged = false;
    let pendingHref = null;

    // CSS класс для подсветки изменённых полей
    const CHANGED_CLASS = 'field-changed';

    // Создаём модалку и добавляем в body (скрыта по умолчанию)
    const modal = document.createElement('div');
    modal.id = 'unsaved-modal';
    modal.innerHTML = `
      <div class="unsaved-backdrop"></div>
      <div class="unsaved-dialog" role="dialog" aria-modal="true" aria-labelledby="unsaved-title">
        <h3 id="unsaved-title">Есть несохранённые изменения</h3>
        <p>У вас есть несохранённые изменения. Что вы хотите сделать?</p>
        <div class="unsaved-actions">
          <button type="button" class="btn btn-stay">Остаться</button>
          <button type="button" class="btn btn-leave">Уйти</button>
          <button type="button" class="btn btn-save">Сохранить</button>
        </div>
      </div>
    `;
    modal.style.display = 'none';
    document.body.appendChild(modal);

    const showModal = () => { modal.style.display = 'block'; document.body.classList.add('unsaved-modal-open'); };
    const hideModal = () => { modal.style.display = 'none'; document.body.classList.remove('unsaved-modal-open'); };

    // Helpers
    function markFieldChanged(el) {
        el.classList.add(CHANGED_CLASS);
    }
    function unmarkAllFields() {
        document.querySelectorAll('.' + CHANGED_CLASS).forEach(el => el.classList.remove(CHANGED_CLASS));
    }

    // Отслеживаем изменения в инпутах форм
    function bindChangeTracking() {
        forms.forEach(form => {
            const inputs = form.querySelectorAll('input, select, textarea');
            inputs.forEach(input => {
                // При изменении помечаем флаг и подсвечиваем поле
                const onChange = function() {
                    formChanged = true;
                    markFieldChanged(input);
                };
                input.addEventListener('change', onChange);
                input.addEventListener('input', onChange);
            });

            // Если форма отправляется — сбрасываем флаг и подсветку
            form.addEventListener('submit', function() {
                formChanged = false;
                pendingHref = null;
                unmarkAllFields();
            });
        });
    }

    // Обработка кликов по ссылкам внутри страницы
    document.addEventListener('click', function(e) {
        const target = e.target.closest('a');
        if (!target) return;

        const href = target.getAttribute('href');
        // Если ссылка якорная или пустая — пропускаем
        if (!href || href.startsWith('#') || href.startsWith('javascript:')) return;

        if (formChanged) {
            e.preventDefault();
            pendingHref = href;
            showModal();
        }
    });

    // Обработка "переход назад / закрытие вкладки" — стандартное предупреждение
    window.addEventListener('beforeunload', function(e) {
        if (formChanged) {
            // Современные браузеры игнорируют текст, но показывают стандартное предупреждение.
            e.preventDefault();
            e.returnValue = '';
            return '';
        }
    });

    // Кнопки модалки
    modal.querySelector('.btn-stay').addEventListener('click', function() {
        pendingHref = null;
        hideModal();
    });

    modal.querySelector('.btn-leave').addEventListener('click', function() {
        hideModal();
        // Сбрасываем флаг и подсветку, затем выполняем навигацию
        formChanged = false;
        unmarkAllFields();
        if (pendingHref) {
            window.location.href = pendingHref;
        }
    });

    // Кнопка "Сохранить" — попытаемся найти ближайшую форму и submit()
    modal.querySelector('.btn-save').addEventListener('click', function() {
        hideModal();
        // Попробуем отправить форму, если на странице одна — отправляем её.
        // Если несколько форм — отправим первую изменённую (с подсветкой).
        let targetForm = null;
        if (forms.length === 1) {
            targetForm = forms[0];
        } else {
            // ищем форму, содержащую изменённые поля
            for (const form of forms) {
                if (form.querySelector('.' + CHANGED_CLASS)) {
                    targetForm = form;
                    break;
                }
            }
            if (!targetForm && forms.length) targetForm = forms[0];
        }

        if (targetForm) {
            // создаём скрытую кнопку submit и кликаем по ней, чтобы избежать проблем с HTML5 validation
            const btn = document.createElement('button');
            btn.type = 'submit';
            btn.style.display = 'none';
            targetForm.appendChild(btn);
            btn.click();
            // флаг и подсветку сбросит обработчик submit формы
        } else {
            // если не нашлась форма — просто сбрасываем и, если есть pendingHref — уходим
            formChanged = false;
            unmarkAllFields();
            if (pendingHref) window.location.href = pendingHref;
        }
    });

    // Подсветка в CSS: добавим стиль в head (простая реализация)
    (function injectStyles() {
        const css = `
        .${CHANGED_CLASS} {
            outline: 2px dashed #f59e0b;
            background-color: #fffaf0;
        }
        #unsaved-modal {
            position: fixed;
            inset: 0;
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: center; /* Центрируем по осям */
            pointer-events: none;
        }
        #unsaved-modal .unsaved-backdrop {
            position: absolute;
            inset: 0;
            background: rgba(15,23,42,0.6);
            pointer-events: auto;
        }
        #unsaved-modal .unsaved-dialog {
            position: relative;
            z-index: 10000;
            background: #fff;
            color: #111827;
            padding: 20px;
            border-radius: 8px;
            max-width: 420px;
            width: 90%;
            box-shadow: 0 10px 30px rgba(2,6,23,0.4);
            pointer-events: auto;
            transform: translate(-50%, -50%); /* Дополнительно центрируем */
            left: 50%;
            top: 50%;
        }
        #unsaved-modal .unsaved-actions {
            display: flex;
            gap: 8px;
            margin-top: 12px;
            justify-content: flex-end;
        }
        #unsaved-modal .btn {
            padding: 8px 12px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }
        #unsaved-modal .btn-stay { background: #e5e7eb; color: #111827; }
        #unsaved-modal .btn-leave { background: #ef4444; color: white; }
        #unsaved-modal .btn-save { background: #2563eb; color: white; }
        body.unsaved-modal-open { overflow: hidden; }
        `;
        const style = document.createElement('style');
        style.appendChild(document.createTextNode(css));
        document.head.appendChild(style);
    })();

    bindChangeTracking();
});