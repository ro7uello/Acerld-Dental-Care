document.addEventListener('DOMContentLoaded', function() {
    const addProfitForm = document.getElementById('addProfitForm');
    const dailyProfitSpan = document.getElementById('dailyProfit');
    const monthlyProfitSpan = document.getElementById('monthlyProfit');
    const yearlyProfitSpan = document.getElementById('yearlyProfit');
    const profitsTableBody = document.querySelector('#profitsTable tbody');
    const profitDateInput = document.getElementById('profitDate');

    const today = new Date().toLocaleDateString('en-CA', { timeZone: 'Asia/Manila' }); // 'YYYY-MM-DD' format
    profitDateInput.value = today;

    function convertToLocalTime(dateString) {
        const utcDate = new Date(dateString);
        return utcDate.toLocaleString('en-PH', {
            timeZone: 'Asia/Manila',
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
        });
    }

    function loadProfitData() {
        fetch('/api/profit-data/')
            .then(response => response.json())
            .then(data => {
                console.log('Profit Data:', data);  // Debugging line
                dailyProfitSpan.textContent = `₱${Number(data.daily).toFixed(2)}`;
                monthlyProfitSpan.textContent = `₱${Number(data.monthly).toFixed(2)}`;
                yearlyProfitSpan.textContent = `₱${Number(data.yearly).toFixed(2)}`;
            })
            .catch(error => console.error('Error loading profit data:', error));
    }

    function loadProfitRecords() {
        fetch('/api/profit-records/')
            .then(response => response.json())
            .then(data => {
                console.log('Profit Records:', data);  // Debugging line
                profitsTableBody.innerHTML = '';
                data.records.forEach(record => {
                    const localDate = convertToLocalTime(record.date);
                    const newRow = document.createElement('tr');
                    newRow.innerHTML = `
                        <td>${localDate}</td>
                        <td>₱${Number(record.amount).toFixed(2)}</td>
                        <td><button class="delete-btn" data-id="${record.id}">Delete</button></td>
                    `;
                    profitsTableBody.appendChild(newRow);
                });
            })
            .catch(error => console.error('Error loading profit records:', error));
    }

    addProfitForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const profitDate = document.getElementById('profitDate').value;
        const profitAmount = document.getElementById('profitAmount').value;

        fetch('/add-profit/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({
                profitDate: profitDate,
                profitAmount: profitAmount
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Add Profit Response:', data);  // Debugging line
            if (data.status === 'success') {
                loadProfitData();
                loadProfitRecords();
                addProfitForm.reset();
                profitDateInput.value = today; // Reset the date input to the current date
            } else {
                alert('Failed to add profit');
            }
        })
        .catch(error => console.error('Error adding profit:', error));
    });

    loadProfitData();
    loadProfitRecords();
});