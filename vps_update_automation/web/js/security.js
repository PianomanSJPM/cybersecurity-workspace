// API endpoints
const API_BASE = 'http://localhost:5002/api';
const ENDPOINTS = {
    security: `${API_BASE}/security`,
    config: `${API_BASE}/config`
};

// Security status elements
const overallSecurityEl = document.getElementById('overallSecurity');
const openPortsEl = document.getElementById('openPorts');
const failedLoginsEl = document.getElementById('failedLogins');
const lastScanEl = document.getElementById('lastScan');
const securityIssuesList = document.getElementById('securityIssuesList');
const portStatusTable = document.getElementById('portStatusTable');

// Security control buttons
const startScanBtn = document.getElementById('startScan');
const blockIPBtn = document.getElementById('blockIP');
const viewLogsBtn = document.getElementById('viewLogs');

// Settings form
const securitySettingsForm = document.getElementById('securitySettingsForm');

// Fetch security status
async function fetchSecurityStatus() {
    try {
        const response = await fetch(ENDPOINTS.security);
        const data = await response.json();
        
        overallSecurityEl.textContent = data.status;
        openPortsEl.textContent = `${data.open_ports.length} ports open`;
        failedLoginsEl.textContent = `${data.failed_logins} failed attempts`;
        lastScanEl.textContent = new Date(data.last_scan).toLocaleString();
        
        // Update security issues list
        securityIssuesList.innerHTML = data.issues.map(issue => `
            <div class="issue-item ${issue.severity}">
                <div class="issue-icon">
                    <i class="fas fa-${issue.severity === 'high' ? 'exclamation-triangle' : 
                                    issue.severity === 'medium' ? 'exclamation-circle' : 'info-circle'}"></i>
                </div>
                <div class="issue-details">
                    <h4>${issue.title}</h4>
                    <p>${issue.description}</p>
                </div>
                <div class="issue-actions">
                    <button class="btn small" onclick="resolveIssue('${issue.id}')">
                        <i class="fas fa-check"></i>
                        Resolve
                    </button>
                </div>
            </div>
        `).join('');
        
        // Update port status table
        portStatusTable.innerHTML = data.open_ports.map(port => `
            <tr>
                <td>${port.number}</td>
                <td>${port.service}</td>
                <td>
                    <span class="status-badge ${port.status.toLowerCase()}">
                        ${port.status}
                    </span>
                </td>
                <td>
                    <button class="btn small" onclick="closePort(${port.number})">
                        <i class="fas fa-times"></i>
                        Close
                    </button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error fetching security status:', error);
        showNotification('Error fetching security status', 'error');
    }
}

// Start security scan
async function startSecurityScan() {
    try {
        startScanBtn.disabled = true;
        startScanBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Scanning...';
        
        const response = await fetch(`${ENDPOINTS.security}/scan`, { method: 'POST' });
        const data = await response.json();
        
        showNotification(data.message, data.status);
        await fetchSecurityStatus();
    } catch (error) {
        console.error('Error starting security scan:', error);
        showNotification('Error starting security scan', 'error');
    } finally {
        startScanBtn.disabled = false;
        startScanBtn.innerHTML = '<i class="fas fa-search"></i> Start Security Scan';
    }
}

// Block IP address
async function blockIPAddress() {
    const ip = prompt('Enter IP address to block:');
    if (!ip) return;
    
    try {
        blockIPBtn.disabled = true;
        blockIPBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Blocking...';
        
        const response = await fetch(`${ENDPOINTS.security}/block`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ip })
        });
        const data = await response.json();
        
        showNotification(data.message, data.status);
        await fetchSecurityStatus();
    } catch (error) {
        console.error('Error blocking IP:', error);
        showNotification('Error blocking IP', 'error');
    } finally {
        blockIPBtn.disabled = false;
        blockIPBtn.innerHTML = '<i class="fas fa-ban"></i> Block IP Address';
    }
}

// View security logs
function viewSecurityLogs() {
    // Implement security logs view
    console.log('View security logs');
}

// Resolve security issue
async function resolveIssue(issueId) {
    try {
        const response = await fetch(`${ENDPOINTS.security}/resolve`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ issueId })
        });
        const data = await response.json();
        
        showNotification(data.message, data.status);
        await fetchSecurityStatus();
    } catch (error) {
        console.error('Error resolving issue:', error);
        showNotification('Error resolving issue', 'error');
    }
}

// Close port
async function closePort(portNumber) {
    try {
        const response = await fetch(`${ENDPOINTS.security}/close-port`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ port: portNumber })
        });
        const data = await response.json();
        
        showNotification(data.message, data.status);
        await fetchSecurityStatus();
    } catch (error) {
        console.error('Error closing port:', error);
        showNotification('Error closing port', 'error');
    }
}

// Save security settings
async function saveSecuritySettings(event) {
    event.preventDefault();
    
    const formData = new FormData(securitySettingsForm);
    const settings = {
        scanFrequency: formData.get('scanFrequency'),
        autoBlock: formData.get('autoBlock') === 'on',
        notifyOnThreat: formData.get('notifyOnThreat') === 'on',
        allowedIPs: formData.get('allowedIPs').split('\n').filter(ip => ip.trim())
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
startScanBtn.addEventListener('click', startSecurityScan);
blockIPBtn.addEventListener('click', blockIPAddress);
viewLogsBtn.addEventListener('click', viewSecurityLogs);
securitySettingsForm.addEventListener('submit', saveSecuritySettings);

// Initialize
fetchSecurityStatus();
setInterval(fetchSecurityStatus, 30000); // Refresh every 30 seconds 