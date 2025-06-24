// API endpoints
const API_BASE = 'http://localhost:5002/api';
const ENDPOINTS = {
    updates: `${API_BASE}/updates`,
    config: `${API_BASE}/config`
};

// Update status elements
const lastUpdateEl = document.getElementById('lastUpdate');
const nextUpdateEl = document.getElementById('nextUpdate');
const pendingUpdatesEl = document.getElementById('pendingUpdates');
const updateHistoryTable = document.getElementById('updateHistoryTable');

// Update control buttons
const checkUpdatesBtn = document.getElementById('checkUpdates');
const installUpdatesBtn = document.getElementById('installUpdates');
const scheduleUpdateBtn = document.getElementById('scheduleUpdate');

// Settings form
const updateSettingsForm = document.getElementById('updateSettingsForm');

// Fetch update status
async function fetchUpdateStatus() {
    try {
        const response = await fetch(ENDPOINTS.updates);
        const data = await response.json();
        
        lastUpdateEl.textContent = data.last_update;
        nextUpdateEl.textContent = data.next_update;
        pendingUpdatesEl.textContent = data.pending_updates.length > 0 
            ? `${data.pending_updates.length} updates available`
            : 'No pending updates';
        
        updateHistoryTable.innerHTML = data.update_history.map(update => `
            <tr>
                <td>${new Date(update.date).toLocaleString()}</td>
                <td>${update.type}</td>
                <td>
                    <span class="status-badge ${update.status.toLowerCase()}">
                        ${update.status}
                    </span>
                </td>
                <td>${update.details}</td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error fetching update status:', error);
        showNotification('Error fetching update status', 'error');
    }
}

// Check for updates
async function checkForUpdates() {
    try {
        checkUpdatesBtn.disabled = true;
        checkUpdatesBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Checking...';
        
        const response = await fetch(`${ENDPOINTS.updates}/check`, { method: 'POST' });
        const data = await response.json();
        
        showNotification(data.message, data.status);
        await fetchUpdateStatus();
    } catch (error) {
        console.error('Error checking for updates:', error);
        showNotification('Error checking for updates', 'error');
    } finally {
        checkUpdatesBtn.disabled = false;
        checkUpdatesBtn.innerHTML = '<i class="fas fa-sync"></i> Check for Updates';
    }
}

// Install updates
async function installUpdates() {
    try {
        installUpdatesBtn.disabled = true;
        installUpdatesBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Installing...';
        
        const response = await fetch(`${ENDPOINTS.updates}/install`, { method: 'POST' });
        const data = await response.json();
        
        showNotification(data.message, data.status);
        await fetchUpdateStatus();
    } catch (error) {
        console.error('Error installing updates:', error);
        showNotification('Error installing updates', 'error');
    } finally {
        installUpdatesBtn.disabled = false;
        installUpdatesBtn.innerHTML = '<i class="fas fa-download"></i> Install Updates';
    }
}

// Schedule update
async function scheduleUpdate() {
    const time = prompt('Enter update time (HH:MM):');
    if (!time) return;
    
    try {
        scheduleUpdateBtn.disabled = true;
        scheduleUpdateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Scheduling...';
        
        const response = await fetch(`${ENDPOINTS.updates}/schedule`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ time })
        });
        const data = await response.json();
        
        showNotification(data.message, data.status);
        await fetchUpdateStatus();
    } catch (error) {
        console.error('Error scheduling update:', error);
        showNotification('Error scheduling update', 'error');
    } finally {
        scheduleUpdateBtn.disabled = false;
        scheduleUpdateBtn.innerHTML = '<i class="fas fa-calendar-plus"></i> Schedule Update';
    }
}

// Save update settings
async function saveUpdateSettings(event) {
    event.preventDefault();
    
    const formData = new FormData(updateSettingsForm);
    const settings = {
        frequency: formData.get('updateFrequency'),
        time: formData.get('updateTime'),
        autoReboot: formData.get('autoReboot') === 'on',
        notifyBeforeUpdate: formData.get('notifyBeforeUpdate') === 'on'
    };
    
    try {
        const response = await fetch(ENDPOINTS.config, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(settings)
        });
        const data = await response.json();
        
        showNotification('Settings saved successfully', 'success');
    } catch (error) {
        console.error('Error saving settings:', error);
        showNotification('Error saving settings', 'error');
    }
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 
                         type === 'error' ? 'times-circle' : 
                         type === 'warning' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }, 100);
}

// Event listeners
checkUpdatesBtn.addEventListener('click', checkForUpdates);
installUpdatesBtn.addEventListener('click', installUpdates);
scheduleUpdateBtn.addEventListener('click', scheduleUpdate);
updateSettingsForm.addEventListener('submit', saveUpdateSettings);

// Initialize
fetchUpdateStatus();
setInterval(fetchUpdateStatus, 30000); // Refresh every 30 seconds 