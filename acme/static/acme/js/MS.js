// document.addEventListener('DOMContentLoaded', function() {
//     const machineGrid = document.getElementById('machineGrid');
//     const historyBody = document.querySelector('.history-table tbody');
//     const filter = document.getElementById('machineFilter');
//     let selectedMachine = ''; // Track current filter selection
//     let machines = []; // Store the machines data

//     // Machine card template
//     function createMachineCard(machine) {
//         return `
//             <div class="col-md-4 machine-card" data-machine="${machine.name}">
//                 <div class="machine-card-inner">
//                     <div class="d-flex justify-content-between align-items-center">
//                         <h3>${machine.name}</h3>
//                         <span class="status-indicator status-${machine.status}"></span>
//                     </div>
//                     <div class="machine-details mt-3">
//                         <p><i class="fas fa-microchip"></i> ${machine.model}</p>
//                         <p><i class="fas fa-calendar-alt"></i> Last Maintenance: ${machine.last_maintenance}</p>
//                         <p><i class="fas fa-chart-line"></i> Uptime: ${machine.uptime}%</p>
//                     </div>
//                 </div>
//             </div>
//         `;
//     }

//     // History row template
//     function createHistoryRow(event) {
//         return `
//             <tr>
//                 <td>${new Date(event.timestamp).toLocaleString()}</td>
//                 <td>${event.machine}</td>
//                 <td>
//                     <span class="status-indicator status-${event.status}"></span>
//                     ${event.status_display}
//                 </td>
//                 <td>${event.description}</td>
//             </tr>
//         `;
//     }

//     // Fetch machine data from the API
//     async function fetchData() {
//         try {
//             const response = await fetch('/get_machine_status/');
//             console.log(response);
//             const data = await response.json();
//             machines = data.machines;

//             // Update machine cards and history
//             updateMachineCards();
//             updateHistory(data.history);

//             // Preserve filter selection in UI
//             filter.value = selectedMachine;
//             applyFilter();

//         } catch (error) {
//             console.error('Error:', error);
//             setTimeout(fetchData, 5000); // Retry after 5 seconds
//         }
//     }

//     // Update the machine cards on the page
//     function updateMachineCards() {
//         machineGrid.innerHTML = ''; // Clear previous cards
//         machines.forEach(machine => {
//             machineGrid.insertAdjacentHTML('beforeend', createMachineCard(machine));
//         });
//     }

//     // Update the maintenance history table
//     function updateHistory(history) {
//         historyBody.innerHTML = history.map(createHistoryRow).join('');
//     }

//     // Apply filter to machine cards
//     function applyFilter() {
//         document.querySelectorAll('.machine-card').forEach(card => {
//             card.style.display = selectedMachine && card.dataset.machine !== selectedMachine ? 'none' : 'block';
//         });
//     }

//     // Set up machine filter (with persistence)
//     function setupFilter() {
//         filter.addEventListener('change', function() {
//             selectedMachine = this.value;
//             localStorage.setItem('selectedMachine', selectedMachine); // Persist filter selection
//             applyFilter();
//         });

//         // Restore previous selection from localStorage
//         const storedSelection = localStorage.getItem('selectedMachine');
//         if (storedSelection) {
//             selectedMachine = storedSelection;
//             filter.value = storedSelection;
//         }
//     }

//     // Initial setup
//     setupFilter();
//     fetchData();
//     setInterval(fetchData, 60000); // Refresh data every 60 seconds

//     // Refresh the filter-based machine cards when the selection changes
//     filter.addEventListener('change', function() {
//         selectedMachine = this.value;
//         applyFilter();
//     });
// });
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
        grid.innerHTML = ''; // Clear existing content

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

    // Fetch machine data when the page loads
    fetchMachineData();

    // Optionally: Set up a polling mechanism to refresh the data periodically (every 60 seconds)
    setInterval(fetchMachineData, 60000);
});
