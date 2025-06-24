// Chart.js configuration
const chartConfig = {
    type: 'line',
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: 'rgba(0, 0, 0, 0.1)'
                }
            },
            x: {
                grid: {
                    display: false
                }
            }
        }
    }
};

// Initialize charts
function initializeCharts() {
    // CPU Usage Chart
    const cpuCtx = document.getElementById('cpuChart').getContext('2d');
    new Chart(cpuCtx, {
        ...chartConfig,
        data: {
            labels: Array.from({length: 12}, (_, i) => `${i * 5}m ago`).reverse(),
            datasets: [{
                label: 'CPU Usage',
                data: [45, 52, 38, 45, 58, 42, 48, 55, 40, 35, 42, 38],
                borderColor: '#3498db',
                backgroundColor: 'rgba(52, 152, 219, 0.1)',
                tension: 0.4,
                fill: true
            }]
        }
    });

    // Memory Usage Chart
    const memoryCtx = document.getElementById('memoryChart').getContext('2d');
    new Chart(memoryCtx, {
        ...chartConfig,
        data: {
            labels: Array.from({length: 12}, (_, i) => `${i * 5}m ago`).reverse(),
            datasets: [{
                label: 'Memory Usage',
                data: [65, 68, 72, 70, 65, 68, 75, 72, 68, 65, 70, 68],
                borderColor: '#2ecc71',
                backgroundColor: 'rgba(46, 204, 113, 0.1)',
                tension: 0.4,
                fill: true
            }]
        }
    });

    // Disk Usage Chart
    const diskCtx = document.getElementById('diskChart').getContext('2d');
    new Chart(diskCtx, {
        ...chartConfig,
        data: {
            labels: Array.from({length: 12}, (_, i) => `${i * 5}m ago`).reverse(),
            datasets: [{
                label: 'Disk Usage',
                data: [75, 75, 76, 75, 77, 76, 75, 76, 77, 76, 75, 76],
                borderColor: '#f1c40f',
                backgroundColor: 'rgba(241, 196, 15, 0.1)',
                tension: 0.4,
                fill: true
            }]
        }
    });

    // Network Traffic Chart
    const networkCtx = document.getElementById('networkChart').getContext('2d');
    new Chart(networkCtx, {
        ...chartConfig,
        data: {
            labels: Array.from({length: 12}, (_, i) => `${i * 5}m ago`).reverse(),
            datasets: [{
                label: 'Network Traffic',
                data: [25, 30, 28, 35, 32, 30, 28, 25, 30, 35, 32, 30],
                borderColor: '#e74c3c',
                backgroundColor: 'rgba(231, 76, 60, 0.1)',
                tension: 0.4,
                fill: true
            }]
        }
    });
}

// Update system status
function updateSystemStatus() {
    // Simulate real-time updates
    setInterval(() => {
        // Update CPU usage
        const cpuUsage = Math.floor(Math.random() * 100);
        document.querySelector('.system-status').style.backgroundColor = 
            `rgba(46, 204, 113, ${cpuUsage / 100})`;

        // Update security status
        const securityIssues = Math.floor(Math.random() * 3);
        const securityStatus = document.querySelector('.security-status');
        if (securityIssues === 0) {
            securityStatus.style.backgroundColor = 'rgba(46, 204, 113, 0.1)';
            document.querySelector('.security-status + .card-info .status').textContent = 'Healthy';
        } else {
            securityStatus.style.backgroundColor = 'rgba(241, 196, 15, 0.1)';
            document.querySelector('.security-status + .card-info .status').textContent = 
                `${securityIssues} Issues`;
        }

        // Update activity list
        const activities = [
            {
                type: 'security',
                title: 'Security Scan Completed',
                time: '2 minutes ago',
                status: 'success'
            },
            {
                type: 'update',
                title: 'System Update Available',
                time: '15 minutes ago',
                status: 'warning'
            },
            {
                type: 'resource',
                title: 'High CPU Usage Detected',
                time: '1 hour ago',
                status: 'error'
            }
        ];

        const activityList = document.querySelector('.activity-list');
        activityList.innerHTML = activities.map(activity => `
            <div class="activity-item">
                <div class="activity-icon ${activity.type}">
                    <i class="fas fa-${activity.type === 'security' ? 'shield-alt' : 
                                      activity.type === 'update' ? 'sync' : 'chart-line'}"></i>
                </div>
                <div class="activity-details">
                    <p class="activity-title">${activity.title}</p>
                    <p class="activity-time">${activity.time}</p>
                </div>
                <div class="activity-status ${activity.status}">
                    <i class="fas fa-${activity.status === 'success' ? 'check' : 
                                     activity.status === 'warning' ? 'exclamation-triangle' : 'times'}"></i>
                </div>
            </div>
        `).join('');
    }, 5000);
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    initializeCharts();
    updateSystemStatus();

    // Add click event listeners for navigation
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            document.querySelectorAll('.nav-links li').forEach(li => li.classList.remove('active'));
            link.parentElement.classList.add('active');
        });
    });

    // Add notification click handler
    document.querySelector('.notifications').addEventListener('click', () => {
        // Implement notification panel
        console.log('Show notifications');
    });
}); 