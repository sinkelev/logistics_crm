document.addEventListener('DOMContentLoaded', function() {
    const checkBtn = document.getElementById('check-delivery');
    const rpoField = document.getElementById('id_rpo_number');
    const deliveryDateField = document.getElementById('id_delivery_date');
    
    if (checkBtn && rpoField && deliveryDateField) {
        checkBtn.addEventListener('click', function() {
            const trackingNumber = rpoField.value.trim();
            if (!trackingNumber) {
                alert('Введите номер РПО');
                return;
            }
            
            const originalText = checkBtn.textContent;
            checkBtn.textContent = 'Проверяем...';
            checkBtn.disabled = true;
            
            fetch(`/api/check-delivery/?tracking_number=${encodeURIComponent(trackingNumber)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        if (data.delivery_date) {
                            deliveryDateField.value = data.delivery_date;
                            alert(`✅ ${data.message}`);
                        } else {
                            alert(`ℹ️ ${data.message}`);
                        }
                    } else {
                        alert(`❌ Ошибка: ${data.error}`);
                    }
                })
                .catch(error => {
                    alert('❌ Ошибка сети при проверке доставки');
                })
                .finally(() => {
                    checkBtn.textContent = originalText;
                    checkBtn.disabled = false;
                });
        });
    }
});