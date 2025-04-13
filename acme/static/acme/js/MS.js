document.addEventListener('DOMContentLoaded', function () {
    // Set up machine filter
    const filter = document.getElementById('machineFilter');
    const grid = document.getElementById('machineGrid');

    let machines = []; // Store machine data
    let selectedMachine = ''; // Track the selected filter value

    async function fetchMachineData() {
        try {
            const response = await fetch('/get_machine_status/'); // Replace with your API endpoint
            console.log(response);
            if (response.ok) {
                const data = await response.json();
                machines = data.machines; // Assume data.machines is the array of machines
                populateMachineGrid(machines); // Populate the grid with the fetched data
            } else {
                console.error('Failed to fetch machine data:', response.status);
            }
        } catch (error) {
            console.error('Error fetching machine data:', error);
        }
    }

    // Populate the machine grid with dynamic data
    function populateMachineGrid(machines) {
        grid.innerHTML = '';

        machines.forEach(machine => {
            const card = document.createElement('div');
            card.className = 'col-lg-3 col-md-6';

            card.innerHTML = `
                <div class="machine-card" data-machine="${machine.name}">
                    <div class="machine-card-inner">
                        <div class="d-flex justify-content-between align-items-center">
                            <h4 class="machine-title">${machine.name}</h4>
                            <span class="status-indicator status-${machine.status}"></span>
                        </div>
                        <div class="machine-details mt-3">
                            <p><i class="fas fa-microchip"></i> ${machine.model}</p>
                            <p><i class="fas fa-calendar-alt"></i> Last Maintenance: ${machine.last_maintenance}</p>
                            <p><i class="fas fa-chart-line"></i> Status: ${machine.status}</p>
                        </div>
                    </div>
                    <div class="card-footer text-center mt-3">
                        <a href="/machines/${machine.serial_number}/" class="btn btn-tech btn-sm">View Details</a>
                    </div>
                </div>
            `;

                        grid.appendChild(card);

            // Add click event to the entire card to navigate to the detail page
            const machineCard = card.querySelector('.machine-card');
            machineCard.addEventListener('click', function (e) {
                // Don't navigate if clicking on the button (it has its own link)
                if (e.target.tagName !== 'A' && e.target.tagName !== 'BUTTON') {
                    window.location.href = `/machines/${machine.serial_number}/`;
                }
            });
            machineCard.style.cursor = 'pointer';
        });
    }

    // Apply filter to the machine grid
    filter.addEventListener('change', function () {
        selectedMachine = this.value;
        if (selectedMachine) {
            const filteredMachines = machines.filter(machine => machine.name === selectedMachine);
            populateMachineGrid(filteredMachines);
        } else {
            populateMachineGrid(machines);
        }
    });

    fetchMachineData();

    setInterval(fetchMachineData, 60000);
});
