// Fetch and display accounts from backend
function loadAccounts() {
    fetch('/accounts')
        .then(res => res.json())
        .then(accounts => {
            const tableBody = document.querySelector('#accountsTable tbody');
            tableBody.innerHTML = '';
            Object.entries(accounts).forEach(([accNo, data]) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${data.name}</td>
                    <td>${accNo}</td>
                    <td>${data.balance}</td>
                `;
                tableBody.appendChild(row);
            });
        });
}

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('accountForm');
    loadAccounts();
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const name = document.getElementById('accountName').value.trim();
        const number = document.getElementById('accountNumber').value.trim();
        const balance = document.getElementById('balance').value.trim();

        if (name && number && balance) {
            fetch('/accounts', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    accountName: name,
                    accountNumber: number,
                    balance: balance
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    loadAccounts();
                    form.reset();
                }
            });
        }
    });
});
