// Sample users data plesss don't mind these names and pass
const users = [
    {
        id: 1,
        name: "Seán O'Sullivan",
        role: "Production Manager",
        email: "sean.osullivan@acme.com",
        dateJoined: "2018-05-15",
        salary: 65000,
        password: "temp123",
        profilePic: "profile-placeholder.jpg"
    },
    {
        id: 2,
        name: "Niamh Murphy",
        role: "Quality Assurance",
        email: "niamh.murphy@acme.com",
        dateJoined: "2019-02-01",
        salary: 58000,
        password: "temp123",
        profilePic: "profile-placeholder.jpg"
    },
    {
        id: 3,
        name: "Cian Walsh",
        role: "Automation Engineer",
        email: "cian.walsh@acme.com",
        dateJoined: "2020-08-15",
        salary: 72000,
        password: "temp123",
        profilePic: "profile-placeholder.jpg"
    },
    {
        id: 4,
        name: "Aoife Ryan",
        role: "Maintenance Technician",
        email: "aoife.ryan@acme.com",
        dateJoined: "2021-04-22",
        salary: 48000,
        password: "temp123",
        profilePic: "profile-placeholder.jpg"
    },
    {
        id: 5,
        name: "Eoin Byrne",
        role: "Systems Operator",
        email: "eoin.byrne@acme.com",
        dateJoined: "2022-11-05",
        salary: 52000,
        password: "temp123",
        profilePic: "profile-placeholder.jpg"
    }
];

// Initialize the user list
function initUserList() {
    const userList = document.getElementById('userList');
    userList.innerHTML = users.map(user => `
        <a href="#" class="list-group-item list-group-item-action user-item" 
           data-user-id="${user.id}"
           onclick="selectUser(${user.id})">
            ${user.name} - ${user.role}
        </a>
    `).join('');
    
    // Select first user by default
    if(users.length > 0) selectUser(users[0].id);
}

// Handle user selection
function selectUser(userId) {
    const user = users.find(u => u.id === userId);
    if(!user) return;

    // Update form fields
    document.getElementById('fullName').value = user.name;
    document.getElementById('email').value = user.email;
    document.getElementById('password').value = user.password;
    document.getElementById('dateJoined').value = user.dateJoined;
    document.getElementById('salary').value = user.salary;
    document.getElementById('role').value = user.role;
    document.getElementById('profilePic').src = user.profilePic;

    // Update active state
    document.querySelectorAll('.user-item').forEach(item => {
        item.classList.remove('active');
        if(item.dataset.userId == userId) item.classList.add('active');
    });
}

// Handle profile picture upload
document.getElementById('profileUpload').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if(file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            document.getElementById('profilePic').src = event.target.result;
            // Here you would update the user's profilePic in your data/store
        };
        reader.readAsDataURL(file);
    }
});

// Handle form submission
document.getElementById('userForm').addEventListener('submit', function(e) {
    e.preventDefault();
    // Add your save logic here
    console.log('Saving user changes...');
});

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initUserList);