document.addEventListener('DOMContentLoaded', function() {
    // Function to fetch dashboard stats and update UI
    function fetchDashboardStats() {
        fetch('/api/tickets/stats/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'same-origin'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Update the dashboard cards with the retrieved data
            document.querySelector('.summary-card:nth-child(1) .count').textContent = data.total_tickets;
            document.querySelector('.summary-card:nth-child(2) .count').textContent = data.open_tickets;
            document.querySelector('.summary-card:nth-child(3) .count').textContent = data.closed_today_tickets;
            document.querySelector('.summary-card:nth-child(4) .count').textContent = data.high_priority_open_tickets;
        })
        .catch(error => {
            console.error('Error fetching dashboard stats:', error);
        });
    }

    // Function to fetch tickets and update the table
    function fetchTickets(viewType = 'all') {
        let url = '/api/tickets/';
        
        // Add query parameters based on the view type
        if (viewType === 'open') {
            url += '?status=Open&status=In%20Progress&status=New&status=Pending%20Customer';
        }
        
        fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'same-origin'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            updateTicketTable(data);
        })
        .catch(error => {
            console.error('Error fetching tickets:', error);
        });
    }

    // Function to update the ticket table with fetched data
    function updateTicketTable(tickets) {
        const tableBody = document.querySelector('.ticket-table tbody');
        
        // Clear existing table rows
        tableBody.innerHTML = '';
        
        if (tickets.length === 0) {
            // If no tickets, show a message
            const emptyRow = document.createElement('tr');
            emptyRow.innerHTML = `
                <td colspan="6" class="text-center fst-italic py-4">
                    No tickets found.
                </td>
            `;
            tableBody.appendChild(emptyRow);
        } else {
            // Add rows for each ticket
            tickets.forEach(ticket => {
                const row = document.createElement('tr');
                
                // Format the date
                const updatedDate = new Date(ticket.last_updated);
                const formattedDate = updatedDate.toISOString().slice(0, 16).replace('T', ' ');
                
                // Get badge classes based on status and priority
                const statusClass = getStatusBadgeClass(ticket.status);
                const priorityClass = getPriorityBadgeClass(ticket.priority);
                
                row.innerHTML = `
                    <th scope="row">${ticket.ticket_id}</th>
                    <td>${truncateText(ticket.subject, 50)}</td>
                    <td>
                        <span class="badge ${statusClass}">${ticket.status}</span>
                    </td>
                    <td>
                        <span class="badge ${priorityClass}">${ticket.priority}</span>
                    </td>
                    <td>${formattedDate}</td>
                    <td>
                        <a href="/ticket/${ticket.ticket_id}/" class="btn btn-sm btn-outline-primary">View</a>
                    </td>
                `;
                
                tableBody.appendChild(row);
            });
        }
    }

    // Helper function to truncate text
    function truncateText(text, maxLength) {
        return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
    }

    // Helper function to get status badge class
    function getStatusBadgeClass(status) {
        switch (status) {
            case 'Open':
                return 'bg-status-open';
            case 'In Progress':
                return 'bg-status-progress';
            case 'New':
                return 'bg-status-new';
            case 'Closed':
                return 'bg-status-closed';
            case 'Pending Customer':
                return 'bg-status-pending';
            default:
                return 'bg-secondary';
        }
    }

    // Helper function to get priority badge class
    function getPriorityBadgeClass(priority) {
        switch (priority) {
            case 'High':
                return 'bg-priority-high';
            case 'Medium':
                return 'bg-priority-medium';
            case 'Low':
                return 'bg-priority-low';
            default:
                return 'bg-secondary';
        }
    }

    // Function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Add event listeners for tab navigation
    const tabs = document.querySelectorAll('.nav-tabs .nav-link');
    tabs.forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Extract view type from the URL
            const url = new URL(this.href);
            const viewType = url.searchParams.get('view') || 'all';
            
            // Update active tab state
            tabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            
            // Fetch tickets based on the selected view
            fetchTickets(viewType);
            
            // Update the browser URL without reloading the page
            history.pushState({}, '', this.href);
        });
    });

    // Initial data load
    fetchDashboardStats();
    
    // Get the current view type from URL or default to 'all'
    const urlParams = new URLSearchParams(window.location.search);
    const currentView = urlParams.get('view') || 'all';
    fetchTickets(currentView);

    // Auto-refresh stats every 60 seconds
    setInterval(fetchDashboardStats, 60000);
});