async function loadAnalytics() {
    const elements = {
        'stat-total': '/analytics/api/summary/',
        'stat-avg': '/analytics/api/summary/',
        'stat-tech': '/analytics/api/summary/',
        'stat-comm': '/analytics/api/summary/'
    };
    
    try {
        const response = await fetch('/analytics/api/summary/');
        if (response.ok) {
            const data = await response.json();
            
            document.getElementById('stat-total').textContent = data.total_interviews || 0;
            document.getElementById('stat-avg').textContent = `${data.avg_overall_score || 0}%`;
            document.getElementById('stat-tech').textContent = `${data.avg_technical_score || 0}%`;
            document.getElementById('stat-comm').textContent = `${data.avg_communication_score || 0}%`;
        }
    } catch (e) {
        console.log('Summary unavailable');
    }
    
    try {
        const response = await fetch('/analytics/api/performance/');
        if (response.ok) {
            const data = await response.json();
            renderScoreChart(data.score_history || []);
        }
    } catch (e) {
        console.log('Performance data unavailable');
    }
    
    try {
        const response = await fetch('/analytics/api/role-analysis/');
        if (response.ok) {
            const data = await response.json();
            renderRoleStats(data.roles || []);
        }
    } catch (e) {
        console.log('Role analysis unavailable');
    }
}

function renderScoreChart(history) {
    const container = document.getElementById('chart-container');
    if (!container) return;
    
    if (history.length === 0) {
        container.innerHTML = '<p class="text-gray-400 text-center py-12">No data available yet</p>';
        return;
    }
    
    const canvas = document.createElement('canvas');
    container.innerHTML = '';
    container.appendChild(canvas);
    
    const ctx = canvas.getContext('2d');
    
    const labels = history.map(h => new Date(h.date).toLocaleDateString());
    const scores = history.map(h => h.score);
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Overall Score',
                data: scores,
                borderColor: '#2563EB',
                backgroundColor: 'rgba(37, 99, 235, 0.1)',
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
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
                    max: 100,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

function renderRoleStats(roles) {
    const container = document.getElementById('role-stats');
    if (!container) return;
    
    if (roles.length === 0) {
        container.innerHTML = '<p class="text-gray-400 text-center py-8">No data available</p>';
        return;
    }
    
    container.innerHTML = roles.map(role => `
        <div>
            <div class="flex justify-between text-sm mb-1">
                <span class="font-medium text-gray-900">${role.role}</span>
                <span class="text-gray-500">${role.count} interviews - ${Math.round(role.avg_score || 0)}% avg</span>
            </div>
            <div class="bg-gray-200 rounded-full h-2">
                <div class="bg-primary h-2 rounded-full transition-all duration-500" style="width: ${role.avg_score || 0}%"></div>
            </div>
        </div>
    `).join('');
}

document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('stat-total')) {
        loadAnalytics();
    }
});
