document.addEventListener('DOMContentLoaded', () => {
    const sections = document.querySelectorAll('main > section');
    const navLinks = document.querySelectorAll('nav a');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            sections.forEach(section => {
                section.classList.add('hidden');
            });
            document.getElementById(targetId).classList.remove('hidden');
        });
    });

    const expenseForm = document.getElementById('expense-form');
    const expenseList = document.getElementById('expense-list');
    const expenses = [];

    expenseForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const description = document.getElementById('description').value;
        const amount = parseFloat(document.getElementById('amount').value);
        const category = document.getElementById('category').value;
        const date = document.getElementById('date').value;

        const expense = { description, amount, category, date };
        expenses.push(expense);
        addExpenseToList(expense);
        updateCharts();
    });

    function addExpenseToList(expense) {
        const li = document.createElement('li');
        li.textContent = `${expense.description}: $${expense.amount} (${expense.category} on ${expense.date})`;
        expenseList.appendChild(li);
    }

    function updateCharts() {
        const categories = {};
        expenses.forEach(expense => {
            if (!categories[expense.category]) {
                categories[expense.category] = 0;
            }
            categories[expense.category] += expense.amount;
        });

        const pieData = {
            labels: Object.keys(categories),
            datasets: [{
                data: Object.values(categories),
                backgroundColor: ['#ff6384', '#36a2eb', '#cc65fe', '#ffce56'],
            }]
        };

        const pieChart = new Chart(document.getElementById('pieChart').getContext('2d'), {
            type: 'pie',
            data: pieData,
        });

        const lineData = {
            labels: expenses.map(expense => expense.date),
            datasets: [{
                label: 'Expenses Over Time',
                data: expenses.map(expense => expense.amount),
                fill: false,
                borderColor: '#ff6384',
            }]
        };

        const lineChart = new Chart(document.getElementById('lineChart').getContext('2d'), {
            type: 'line',
            data: lineData,
        });
    }
});
