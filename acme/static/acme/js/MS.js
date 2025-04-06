document.addEventListener('DOMContentLoaded', function() {
    const machineGrid = document.getElementById('machineGrid');
    const historyBody = document.querySelector('.history-table tbody');
    const filter = document.getElementById('machineFilter');
    let selectedMachine = ''; // Track current filter selection

    // Machine template
    function createMachineCard(machine) {
        return `
            <div class="col-md-4 machine-card" data-machine="${machine.name}">
                <div class="machine-card-inner">
                    <div class="d-flex justify-content-between align-items-center">
                        <h3>${machine.name}</h3>
                        <span class="status-indicator status-${machine.status}"></span>
                    </div>
                    <div class="machine-details mt-3">
                        <p><i class="fas fa-microchip"></i> ${machine.model}</p>
                        <p><i class="fas fa-calendar-alt"></i> Last Maintenance: ${machine.last_maintenance}</p>
                        <p><i class="fas fa-chart-line"></i> Uptime: ${machine.uptime}%</p>
                    </div>
                </div>
            </div>
        `;
    }

    // History row template
    function createHistoryRow(event) {
        return `
            <tr>
                <td>${new Date(event.timestamp).toLocaleString()}</td>
                <td>${event.machine}</td>
                <td>
                    <span class="status-indicator status-${event.status}"></span>
                    ${event.status_display}
                </td>
                <td>${event.description}</td>
            </tr>
        `;
    }

    async function fetchData() {
        try {
            const response = await fetch('/api/machine-status/');
            const data = await response.json();

            // Update existing cards
            data.machines.forEach(machine => {
                const existingCard = machineGrid.querySelector(`[data-machine="${machine.name}"]`);
                if (existingCard) {
                    // Update card content
                    existingCard.querySelector('.status-indicator').className = `status-indicator status-${machine.status}`;
                    existingCard.querySelector('.machine-details').innerHTML = `
                        <p><i class="fas fa-microchip"></i> ${machine.model}</p>
                        <p><i class="fas fa-calendar-alt"></i> Last Maintenance: ${machine.last_maintenance}</p>
                        <p><i class="fas fa-chart-line"></i> Uptime: ${machine.uptime}%</p>
                    `;
                } else {
                    // Add new machine card
                    machineGrid.insertAdjacentHTML('beforeend', createMachineCard(machine));
                }
            });

            // Preserve filter selection in UI
            filter.value = selectedMachine;
            applyFilter();

            // Update history
            historyBody.innerHTML = data.history.map(createHistoryRow).join('');

        } catch (error) {
            console.error('Error:', error);
            setTimeout(fetchData, 5000);
        }
    }

    function applyFilter() {
        document.querySelectorAll('.machine-card').forEach(card => {
            card.style.display = selectedMachine && card.dataset.machine !== selectedMachine ? 'none' : 'block';
        });
    }

    function setupFilter() {
        filter.addEventListener('change', function() {
            selectedMachine = this.value;
            localStorage.setItem('selectedMachine', selectedMachine); // Persist selection
            applyFilter();
        });
        
        // Restore previous selection
        const storedSelection = localStorage.getItem('selectedMachine');
        if (storedSelection) {
            selectedMachine = storedSelection;
            filter.value = storedSelection;
        }
    }

    // Initial setup
    setupFilter();
    fetchData();
    setInterval(fetchData, 60000);

    // Refresh every 60 seconds / this can be change maybe to 30s ???? idk
    const pollInterval = 60000;
    let updateTimer = setInterval(fetchData, pollInterval);

    window.addEventListener('beforeunload', () => {
        clearInterval(updateTimer);
    });
});