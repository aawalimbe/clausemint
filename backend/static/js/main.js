// Global variables
let currentDocument = null;
let currentDocumentId = null;

// DOM elements
const navItems = document.querySelectorAll('.nav-item');
const tabContents = document.querySelectorAll('.tab-content');
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const ndaForm = document.getElementById('ndaForm');
const ndaResult = document.getElementById('ndaResult');
const ndaContent = document.getElementById('ndaContent');
const exportNdaBtn = document.getElementById('exportNda');
const documentContent = document.getElementById('documentContent');
const analysisPanel = document.getElementById('analysisPanel');
const analysisContent = document.getElementById('analysisContent');
const riskSummary = document.getElementById('riskSummary');
const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const sendMessageBtn = document.getElementById('sendMessage');
const loadingOverlay = document.getElementById('loadingOverlay');

// Tab switching functionality
navItems.forEach(item => {
    item.addEventListener('click', () => {
        const targetTab = item.getAttribute('data-tab');
        
        // Update active nav item
        navItems.forEach(nav => nav.classList.remove('active'));
        item.classList.add('active');
        
        // Update active tab content
        tabContents.forEach(tab => tab.classList.remove('active'));
        document.getElementById(targetTab).classList.add('active');
    });
});

// File upload functionality
uploadArea.addEventListener('click', () => {
    fileInput.click();
});

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#6366f1';
    uploadArea.style.background = 'rgba(99, 102, 241, 0.1)';
});

uploadArea.addEventListener('dragleave', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#333333';
    uploadArea.style.background = '#2a2a2a';
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#333333';
    uploadArea.style.background = '#2a2a2a';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileUpload(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileUpload(e.target.files[0]);
    }
});

// File upload handler
async function handleFileUpload(file) {
    if (!file.name.endsWith('.docx')) {
        showNotification('Please upload a DOCX file', 'error');
        return;
    }
    
    showLoading(true);
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('title', file.name);
    formData.append('document_type', 'contract');
    
    try {
        const response = await fetch('/api/upload/', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentDocument = data;
            currentDocumentId = data.id;
            
            // Display document content
            displayDocumentContent(data.content);
            
            // Switch to document review tab
            switchToTab('document-review');
            
            // Analyze document
            await analyzeDocument(data.content);
            
            showNotification('Document uploaded and analyzed successfully', 'success');
        } else {
            showNotification(data.error || 'Upload failed', 'error');
        }
    } catch (error) {
        console.error('Upload error:', error);
        showNotification('Upload failed. Please try again.', 'error');
    } finally {
        showLoading(false);
    }
}

// Display document content
function displayDocumentContent(content) {
    documentContent.innerHTML = `
        <div class="document-text">
            <h4>Document Content</h4>
            <div class="content-text">${content.replace(/\n/g, '<br>')}</div>
        </div>
    `;
}

// Analyze document
async function analyzeDocument(content) {
    try {
        const response = await fetch('/api/redlining/analyze/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ content: content })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayAnalysisResults(data);
        } else {
            showNotification(data.error || 'Analysis failed', 'error');
        }
    } catch (error) {
        console.error('Analysis error:', error);
        showNotification('Analysis failed. Please try again.', 'error');
    }
}

// Display analysis results
function displayAnalysisResults(data) {
    analysisPanel.style.display = 'block';
    
    // Display risk summary
    const summary = data.summary;
    riskSummary.innerHTML = `
        <div class="risk-item risk-red">
            <i class="fas fa-exclamation-triangle"></i>
            <span>${summary.red_clauses} High Risk</span>
        </div>
        <div class="risk-item risk-amber">
            <i class="fas fa-exclamation-circle"></i>
            <span>${summary.amber_clauses} Needs Review</span>
        </div>
        <div class="risk-item risk-green">
            <i class="fas fa-check-circle"></i>
            <span>${summary.green_clauses} Standard</span>
        </div>
        <div class="risk-item">
            <i class="fas fa-percentage"></i>
            <span>${summary.risk_percentage}% Risk</span>
        </div>
    `;
    
    // Display clause analysis
    analysisContent.innerHTML = '';
    data.analysis.forEach((clause, index) => {
        const clauseElement = createClauseAnalysisElement(clause, index);
        analysisContent.appendChild(clauseElement);
    });
}

// Create clause analysis element
function createClauseAnalysisElement(clause, index) {
    const div = document.createElement('div');
    div.className = `clause-analysis risk-${clause.risk_level}`;
    
    const riskIcon = clause.risk_level === 'red' ? 'exclamation-triangle' : 
                    clause.risk_level === 'amber' ? 'exclamation-circle' : 'check-circle';
    
    div.innerHTML = `
        <div class="clause-text">"${clause.clause_text}"</div>
        <div class="clause-details">
            <div class="clause-risk">
                <i class="fas fa-${riskIcon}"></i>
                <span>${clause.risk_level.toUpperCase()} Risk</span>
            </div>
            <div class="clause-confidence">Confidence: ${clause.confidence}%</div>
        </div>
        <div class="clause-explanation">${clause.explanation}</div>
        ${clause.suggestions ? `
            <div class="clause-suggestions">
                <h6>Suggestions</h6>
                <p>${clause.suggestions}</p>
            </div>
        ` : ''}
    `;
    
    return div;
}

// NDA form submission
ndaForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(ndaForm);
    const ndaData = {
        party_a: formData.get('party_a'),
        party_b: formData.get('party_b'),
        party_c: formData.get('party_c') || '',
        nda_type: formData.get('nda_type'),
        purpose: formData.get('purpose'),
        confidentiality_period: formData.get('confidentiality_period'),
        jurisdiction: formData.get('jurisdiction')
    };
    
    showLoading(true);
    
    try {
        const response = await fetch('/api/nda/generate/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(ndaData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayNdaResult(data.nda_content);
            showNotification('NDA generated successfully', 'success');
        } else {
            showNotification(data.error || 'Generation failed', 'error');
        }
    } catch (error) {
        console.error('NDA generation error:', error);
        showNotification('Generation failed. Please try again.', 'error');
    } finally {
        showLoading(false);
    }
});

// Display NDA result
function displayNdaResult(content) {
    ndaContent.textContent = content;
    ndaResult.style.display = 'block';
    exportNdaBtn.disabled = false;
    
    // Scroll to result
    ndaResult.scrollIntoView({ behavior: 'smooth' });
}

// Export NDA
exportNdaBtn.addEventListener('click', async () => {
    if (!ndaContent.textContent) {
        showNotification('No NDA content to export', 'error');
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch('/api/nda/export/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ nda_content: ndaContent.textContent })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Create and download file
            const blob = new Blob([data.content], { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = data.filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
            showNotification('NDA exported successfully', 'success');
        } else {
            showNotification(data.error || 'Export failed', 'error');
        }
    } catch (error) {
        console.error('Export error:', error);
        showNotification('Export failed. Please try again.', 'error');
    } finally {
        showLoading(false);
    }
});

// Chat functionality
sendMessageBtn.addEventListener('click', sendChatMessage);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendChatMessage();
    }
});

// Send chat message
async function sendChatMessage() {
    const message = chatInput.value.trim();
    if (!message) return;
    
    if (!currentDocumentId) {
        showNotification('Please upload a document first', 'error');
        return;
    }
    
    // Add user message to chat
    addChatMessage(message, 'user');
    chatInput.value = '';
    
    showLoading(true);
    
    try {
        const response = await fetch('/api/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                document_id: currentDocumentId,
                message: message
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            addChatMessage(data.response, 'assistant');
        } else {
            addChatMessage('Sorry, I encountered an error. Please try again.', 'assistant');
        }
    } catch (error) {
        console.error('Chat error:', error);
        addChatMessage('Sorry, I encountered an error. Please try again.', 'assistant');
    } finally {
        showLoading(false);
    }
}

// Add chat message
function addChatMessage(content, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${type}`;
    
    const time = new Date().toLocaleTimeString();
    
    messageDiv.innerHTML = `
        <div class="message-content">
            ${content}
            <div class="message-time">${time}</div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Copy to clipboard
function copyToClipboard() {
    if (ndaContent.textContent) {
        navigator.clipboard.writeText(ndaContent.textContent).then(() => {
            showNotification('NDA copied to clipboard', 'success');
        }).catch(() => {
            showNotification('Failed to copy to clipboard', 'error');
        });
    }
}

// Switch to tab
function switchToTab(tabName) {
    navItems.forEach(nav => nav.classList.remove('active'));
    tabContents.forEach(tab => tab.classList.remove('active'));
    
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    document.getElementById(tabName).classList.add('active');
}

// Show/hide loading overlay
function showLoading(show) {
    loadingOverlay.style.display = show ? 'flex' : 'none';
}

// Show notification
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        </div>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#6366f1'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        z-index: 1001;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-width: 400px;
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 5 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 5000);
}

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    console.log('Clausemint app initialized');
    
    // Add notification styles
    const style = document.createElement('style');
    style.textContent = `
        .notification-content {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .notification-content i {
            font-size: 1.1rem;
        }
    `;
    document.head.appendChild(style);
}); 