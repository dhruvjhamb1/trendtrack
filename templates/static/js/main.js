// Global chart instances for proper cleanup
let engagementChartInstance = null;
let interactionsChartInstance = null;

function toggleLoading(show) {
    document.getElementById('loading').style.display = show ? 'flex' : 'none';
}

function handleError(error) {
    console.error('API Error:', error);
    const errorMessage = document.createElement('div');
    errorMessage.className = 'error-message glass-card';
    errorMessage.innerHTML = `
        <p>An error occurred while fetching insights. Please try again.</p>
        <p class="error-details">${error.message || 'Unknown error'}</p>
    `;
    document.getElementById('insights-display').appendChild(errorMessage);
}

async function analyzePostType(postType) {
    try {
        toggleLoading(true);
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ post_type: postType })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }

        const insightsDisplay = document.getElementById('metrics-display');
        insightsDisplay.innerHTML = `
            <div class="insights-container">
                <h3>Insights for ${postType}</h3>
                <p>${data.insights}</p>
            </div>
        `;

        // Clean up existing charts before creating new ones
        if (engagementChartInstance) {
            engagementChartInstance.destroy();
        }
        if (interactionsChartInstance) {
            interactionsChartInstance.destroy();
        }

        createEngagementChart(data);
        createInteractionsChart(data);
    } catch (error) {
        handleError(error);
    } finally {
        toggleLoading(false);
    }
}

async function generateInsights() {
    try {
        toggleLoading(true);
        const response = await fetch('/api/insights', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }

        const insightsDisplay = document.getElementById('insights-display');
        insightsDisplay.innerHTML = `
            <div class="insights-container">
                <h3>Overall Analysis</h3>
                <p>${data.insights}</p>
            </div>
        `;
    } catch (error) {
        handleError(error);
    } finally {
        toggleLoading(false);
    }
}

// Error message styles
document.head.insertAdjacentHTML('beforeend', `
<style>
.error-message {
    background: rgba(255, 0, 0, 0.1);
    border: 1px solid rgba(255, 0, 0, 0.2);
    color: #ff6b6b;
    padding: 1rem;
    margin-top: 1rem;
    border-radius: var(--border-radius);
}

.error-details {
    font-size: 0.9rem;
    margin-top: 0.5rem;
    color: #ff8787;
}
</style>
`);

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    if (data.error) {
        resultsDiv.innerHTML = `<p class="error">${data.error}</p>`;
    } else {
        resultsDiv.innerHTML = data.insights;
    }
}

function createEngagementChart(data) {
    const ctx = document.getElementById('engagementChart').getContext('2d');
    
    engagementChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Likes', 'Comments', 'Shares'],
            datasets: [{
                label: 'Engagement Metrics',
                data: [
                    data.metrics.avg_likes,
                    data.metrics.avg_comments,
                    data.metrics.avg_shares
                ],
                backgroundColor: [
                    'rgba(0, 194, 255, 0.7)',
                    'rgba(0, 102, 255, 0.7)',
                    'rgba(0, 153, 255, 0.7)'
                ],
                borderColor: [
                    'rgba(0, 194, 255, 1)',
                    'rgba(0, 102, 255, 1)',
                    'rgba(0, 153, 255, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Engagement Breakdown',
                    color: '#e2e8f0'
                },
                legend: {
                    labels: {
                        color: '#e2e8f0'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#e2e8f0'
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#e2e8f0'
                    }
                }
            }
        }
    });
}

function createInteractionsChart(data) {
    const ctx = document.getElementById('interactionsChart').getContext('2d');
    
    interactionsChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Reach', 'Total Interactions', 'Engagement Rate'],
            datasets: [{
                label: 'Performance Metrics',
                data: [
                    data.metrics.avg_reach,
                    data.metrics.avg_likes + data.metrics.avg_comments + data.metrics.avg_shares,
                    data.metrics.avg_engagement_rate
                ],
                borderColor: 'rgba(0, 194, 255, 1)',
                backgroundColor: 'rgba(0, 194, 255, 0.2)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Performance Overview',
                    color: '#e2e8f0'
                },
                legend: {
                    labels: {
                        color: '#e2e8f0'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#e2e8f0'
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#e2e8f0'
                    }
                }
            }
        }
    });
} 