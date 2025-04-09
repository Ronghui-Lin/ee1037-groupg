document.addEventListener('DOMContentLoaded', function() {
    const ticketId = document.getElementById('ticket-container').dataset.ticketId;
    const commentForm = document.getElementById('comment-form');
    const statusForm = document.getElementById('status-form');
    
    // Function to load ticket details
    function loadTicketDetails() {
        fetch(`/api/tickets/${ticketId}/`, {
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
            // Update ticket details
            document.getElementById('ticket-subject').textContent = data.subject;
            document.getElementById('ticket-description').textContent = data.description;
            document.getElementById('ticket-status').textContent = data.status;
            document.getElementById('ticket-priority').textContent = data.priority;
            document.getElementById('ticket-created-by').textContent = `${data.created_by.first_name} ${data.created_by.last_name}`;
            document.getElementById('ticket-created-at').textContent = formatDateTime(data.created_at);
            document.getElementById('ticket-last-updated').textContent = formatDateTime(data.last_updated);
            
            // Update status badge
            const statusBadge = document.getElementById('status-badge');
            statusBadge.className = `badge ${getStatusBadgeClass(data.status)}`;
            statusBadge.textContent = data.status;
            
            // Update priority badge
            const priorityBadge = document.getElementById('priority-badge');
            priorityBadge.className = `badge ${getPriorityBadgeClass(data.priority)}`;
            priorityBadge.textContent = data.priority;
            
            // Load comments
            loadComments();
            
            // Load attachments (if applicable)
            if (data.attachments && data.attachments.length > 0) {
                updateAttachmentsList(data.attachments);
            }
        })
        .catch(error => {
            console.error('Error loading ticket details:', error);
        });
    }
    
    // Function to load and display comments
    function loadComments() {
        fetch(`/api/tickets/${ticketId}/comments/`, {
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
            updateCommentsList(data);
        })
        .catch(error => {
            console.error('Error loading comments:', error);
        });
    }
    
    // Function to update the comments list
    function updateCommentsList(comments) {
        const commentsContainer = document.getElementById('comments-container');
        commentsContainer.innerHTML = '';
        
        if (comments.length === 0) {
            commentsContainer.innerHTML = `
                <div class="text-center py-4 text-white-50 fst-italic">
                    No comments yet.
                </div>
            `;
        } else {
            comments.forEach(comment => {
                const commentElement = document.createElement('div');
                commentElement.className = 'comment-item p-3 mb-3 border-bottom';
                
                commentElement.innerHTML = `
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <div class="comment-author fw-bold">
                            ${comment.author.first_name} ${comment.author.last_name}
                        </div>
                        <div class="comment-date text-white-50 small">
                            ${formatDateTime(comment.created_at)}
                        </div>
                    </div>
                    <div class="comment-content">
                        ${comment.content}
                    </div>
                `;
                
                commentsContainer.appendChild(commentElement);
            });
        }
    }
    
    // Function to update the attachments list
    function updateAttachmentsList(attachments) {
        const attachmentsContainer = document.getElementById('attachments-container');
        attachmentsContainer.innerHTML = '';
        
        if (attachments.length === 0) {
            attachmentsContainer.innerHTML = `
                <div class="text-center py-4 text-white-50 fst-italic">
                    No attachments.
                </div>
            `;
        } else {
            const attachmentsList = document.createElement('ul');
            attachmentsList.className = 'list-group';
            
            attachments.forEach(attachment => {
                const attachmentItem = document.createElement('li');
                attachmentItem.className = 'list-group-item d-flex justify-content-between align-items-center';
                
                attachmentItem.innerHTML = `
                    <div>
                        <i class="fas fa-paperclip me-2"></i>
                        ${attachment.filename}
                    </div>
                    <div>
                        <a href="${attachment.file}" class="btn btn-sm btn-outline-primary" target="_blank">
                            <i class="fas fa-download me-1"></i> Download
                        </a>
                    </div>
                `;
                
                attachmentsList.appendChild(attachmentItem);
            });
            
            attachmentsContainer.appendChild(attachmentsList);
        }
    }
    
    // Add event listener for comment form submission
    if (commentForm) {
        commentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const commentContent = document.getElementById('id_content').value;
            
            if (!commentContent.trim()) {
                // Don't submit empty comments
                return;
            }
            
            fetch(`/api/tickets/${ticketId}/comments/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    content: commentContent
                }),
                credentials: 'same-origin'
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(() => {
                // Clear the comment form
                document.getElementById('id_content').value = '';
                
                // Show success message
                showAlert('Comment added successfully.', 'success');
                
                // Reload comments to show the new one
                loadComments();
            })
            .catch(error => {
                console.error('Error adding comment:', error);
                showAlert('Failed to add comment. Please try again.', 'danger');
            });
        });
    }
    
    // Add event listener for status form submission
    if (statusForm) {
        statusForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const newStatus = document.getElementById('id_status').value;
            
            fetch(`/api/tickets/${ticketId}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    status: newStatus
                }),
                credentials: 'same-origin'
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(() => {
                // Show success message
                showAlert('Ticket status updated successfully.', 'success');
                
                // Reload ticket details to show the updated status
                loadTicketDetails();
            })
            .catch(error => {
                console.error('Error updating status:', error);
                showAlert('Failed to update status. Please try again.', 'danger');
            });
        });
    }
    
    // Helper function to format date/time
    function formatDateTime(dateTimeStr) {
        const date = new Date(dateTimeStr);
        return date.toLocaleString('en-US', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
        });
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
    
    // Function to show alerts/messages
    function showAlert(message, type) {
        const alertsContainer = document.getElementById('alerts-container');
        
        const alertElement = document.createElement('div');
        alertElement.className = `alert alert-${type} alert-dismissible fade show`;
        alertElement.role = 'alert';
        
        alertElement.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        alertsContainer.appendChild(alertElement);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            alertElement.classList.remove('show');
            setTimeout(() => {
                alertElement.remove();
            }, 150);
        }, 5000);
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
    
    // Load ticket details on page load
    loadTicketDetails();
});