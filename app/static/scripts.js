// Function to show the success alert
function showAlert(message) {
    const alertBox = document.getElementById('alertBox');
    alertBox.innerText = message;
    alertBox.style.display = 'block';
    setTimeout(() => {
        alertBox.style.display = 'none';
    }, 3000);
}

// Create Program Form Submission
document.getElementById('createProgramForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('programName').value;
    const response = await fetch('/programs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name })
    });
    const result = await response.json();
    showAlert(result.message || result.error);
    document.getElementById('programName').value = ''; // Clear the input
    await loadPrograms(); // Reload programs list
});

// Register Client Form Submission
document.getElementById('registerClientForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('clientName').value;
    const clientId = document.getElementById('clientId').value;
    const response = await fetch('/clients', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, client_id: clientId })
    });
    const result = await response.json();
    showAlert(result.message || result.error);
    document.getElementById('clientName').value = '';
    document.getElementById('clientId').value = '';
});

// Enroll Client in Program Form Submission
document.getElementById('enrollClientForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const client_id = document.getElementById('clientIdEnroll').value;
    const program = document.getElementById('programNameEnroll').value;
    const response = await fetch('/clients/enroll', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ client_id, program })
    });
    const result = await response.json();
    showAlert(result.message || result.error);
    document.getElementById('clientIdEnroll').value = '';
    document.getElementById('programNameEnroll').value = '';
});

// View Client Profile Form Submission
document.getElementById('viewClientForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const clientId = document.getElementById('viewClientId').value;
    const response = await fetch(`/clients/${clientId}`);
    const result = await response.json();
    const profileDiv = document.getElementById('clientProfile');
    if (result.error) {
        showAlert(result.error);
        profileDiv.innerHTML = '';
    } else {
        profileDiv.innerHTML = `
            <h3>Client Profile</h3>
            <p><strong>ID:</strong> ${result.client_id}</p>
            <p><strong>Name:</strong> ${result.name}</p>
            <p><strong>Programs:</strong> ${result.programs.join(', ') || 'None'}</p>
        `;
    }
    document.getElementById('viewClientId').value = '';
});

// Load Programs
async function loadPrograms() {
    const response = await fetch('/programs');
    const data = await response.json();
    const programsList = document.getElementById('programsList');
    programsList.innerHTML = '';

    if (data.programs && data.programs.length > 0) {
        data.programs.forEach(program => {
            const li = document.createElement('li');
            li.textContent = program;
            programsList.appendChild(li);
        });
    } else {
        programsList.innerHTML = '<li>No programs available yet.</li>';
    }
}

// Load programs on page load
window.onload = loadPrograms;
