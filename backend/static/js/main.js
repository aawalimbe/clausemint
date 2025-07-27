// Global variables
let currentDocument = null;
let currentDocumentId = null;
let currentAIProvider = 'mistral'; // Default to Mistral
let currentNDAParams = null; // Store NDA parameters for export

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

// Legal-themed loading messages for streaming
const legalLoadingMessages = [
    {
        icon: 'fas fa-balance-scale',
        message: 'Analyzing legal requirements...',
        progress: 10
    },
    {
        icon: 'fas fa-gavel',
        message: 'Crafting confidentiality clauses...',
        progress: 25
    },
    {
        icon: 'fas fa-shield-alt',
        message: 'Implementing security measures...',
        progress: 40
    },
    {
        icon: 'fas fa-file-contract',
        message: 'Drafting legal provisions...',
        progress: 60
    },
    {
        icon: 'fas fa-handshake',
        message: 'Balancing party interests...',
        progress: 80
    },
    {
        icon: 'fas fa-stream',
        message: 'AI is streaming your document in real-time...',
        progress: 90
    },
    {
        icon: 'fas fa-check-circle',
        message: 'Finalizing document structure...',
        progress: 95
    }
];

let currentMessageIndex = 0;
let messageInterval;

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
    
    // Validate required fields
    if (!ndaData.party_a || !ndaData.party_b || !ndaData.purpose) {
        showNotification('Please fill in all required fields', 'error');
        return;
    }
    
    // Show NDA loading modal
    showNDALoadingModal();
    
    try {
        // Use streaming endpoint for real-time generation
        const response = await fetch('/api/nda/generate/streaming/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(ndaData)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            updateLoadingMessage('fas fa-exclamation-triangle', 'Failed to generate document', 0, 'error');
            setTimeout(() => {
                hideNDALoadingModal();
                showNotification(errorData.error || 'Failed to generate NDA', 'error');
            }, 2000);
            return;
        }
        
        // Handle streaming response
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        
        while (true) {
            const { done, value } = await reader.read();
            
            if (done) break;
            
            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n');
            buffer = lines.pop(); // Keep incomplete line in buffer
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    try {
                        const data = JSON.parse(line.slice(6));
                        
                        if (data.status === 'started') {
                            updateLoadingMessage('fas fa-cogs', 'AI is generating your document...', 50);
                        } else if (data.status === 'completed') {
                            updateLoadingMessage('fas fa-check-circle', 'Document crafted successfully!', 100, 'success');
                            
                            setTimeout(() => {
                                hideNDALoadingModal();
                                displayNdaResult(data.content, data.parameters);
                                showNotification('🎉 Your NDA has been expertly crafted and is ready for review!', 'success');
                            }, 1500);
                            return;
                        } else if (data.status === 'error') {
                            updateLoadingMessage('fas fa-exclamation-triangle', 'Generation failed', 0, 'error');
                            setTimeout(() => {
                                hideNDALoadingModal();
                                showNotification(data.error || 'Failed to generate NDA', 'error');
                            }, 2000);
                            return;
                        }
                    } catch (e) {
                        console.error('Error parsing streaming data:', e);
                    }
                }
            }
        }
        
    } catch (error) {
        console.error('NDA generation error:', error);
        updateLoadingMessage('fas fa-exclamation-triangle', 'Connection error occurred', 0, 'error');
        setTimeout(() => {
            hideNDALoadingModal();
            showNotification('Failed to generate NDA - please check your connection', 'error');
        }, 2000);
    }
});

// Display NDA result
function displayNdaResult(content, params = null) {
    ndaContent.textContent = content;
    ndaResult.style.display = 'block';
    exportNdaBtn.disabled = false;
    
    // Store parameters for export
    if (params) {
        currentNDAParams = params;
    }
    
    // Scroll to result
    ndaResult.scrollIntoView({ behavior: 'smooth' });
}

// Export NDA
exportNdaBtn.addEventListener('click', async () => {
    if (!ndaContent.textContent) {
        showNotification('No NDA content to export', 'error');
        return;
    }
    
    // Show loading modal for export
    showNDALoadingModal();
    updateLoadingMessage('fas fa-file-word', 'Preparing document for download...', 50);
    
    try {
        const response = await fetch('/api/nda/export/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                nda_content: ndaContent.textContent,
                party_a: currentNDAParams?.party_a || 'Party A',
                party_b: currentNDAParams?.party_b || 'Party B'
            })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            // Show success message
            updateLoadingMessage('fas fa-check-circle', 'Document ready for download!', 100, 'success');
            
            setTimeout(() => {
                hideNDALoadingModal();
                
                // Trigger download
                const link = document.createElement('a');
                link.href = data.download_url;
                link.download = data.filename;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                
                showNotification('📄 Your NDA document has been prepared and downloaded successfully!', 'success');
            }, 1500);
            
        } else {
            updateLoadingMessage('fas fa-exclamation-triangle', 'Failed to prepare document', 0, 'error');
            setTimeout(() => {
                hideNDALoadingModal();
                showNotification(data.error || 'Export failed', 'error');
            }, 2000);
        }
    } catch (error) {
        console.error('Export error:', error);
        updateLoadingMessage('fas fa-exclamation-triangle', 'Export failed', 0, 'error');
        setTimeout(() => {
            hideNDALoadingModal();
            showNotification('Export failed. Please try again.', 'error');
        }, 2000);
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
    
    // Initialize AI provider status
    checkAIStatus();
    
    // Initialize jurisdictions dropdown
    loadJurisdictions();
    
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

// AI Provider Management Functions
async function checkAIStatus() {
    try {
        const response = await fetch('/api/ai/status/');
        const data = await response.json();
        
        if (response.ok) {
            currentAIProvider = data.current_provider;
            updateAIProviderBadge(data.current_provider, data.connection_status);
        }
    } catch (error) {
        console.error('Error checking AI status:', error);
    }
}

function updateAIProviderBadge(provider, connectionStatus) {
    const badge = document.getElementById('aiProviderBadge');
    if (badge) {
        const status = connectionStatus.status === 'connected' ? '🟢' : '🔴';
        badge.innerHTML = `<i class="fas fa-robot"></i> ${status} ${provider.toUpperCase()}`;
        
        // Update badge color based on connection status
        if (connectionStatus.status === 'connected') {
            badge.style.background = 'rgba(16, 185, 129, 0.1)';
            badge.style.color = '#10b981';
            badge.style.borderColor = 'rgba(16, 185, 129, 0.3)';
        } else {
            badge.style.background = 'rgba(239, 68, 68, 0.1)';
            badge.style.color = '#ef4444';
            badge.style.borderColor = 'rgba(239, 68, 68, 0.3)';
        }
    }
}

async function switchAIProvider(provider) {
    try {
        const response = await fetch('/api/ai/switch/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ provider: provider })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentAIProvider = provider;
            updateAIProviderBadge(provider, data.connection_status);
            showNotification(`Switched to ${provider.toUpperCase()}`, 'success');
        } else {
            showNotification(data.error || 'Failed to switch provider', 'error');
        }
    } catch (error) {
        console.error('Error switching AI provider:', error);
        showNotification('Failed to switch AI provider', 'error');
    }
}

// Jurisdiction Management Functions
async function loadJurisdictions() {
    try {
        const response = await fetch('/api/jurisdictions/');
        const data = await response.json();
        
        if (response.ok) {
            populateJurisdictionDropdown(data.jurisdictions, data.default);
        } else {
            console.error('Error loading jurisdictions:', data.error);
        }
    } catch (error) {
        console.error('Error loading jurisdictions:', error);
    }
}

function populateJurisdictionDropdown(jurisdictions, defaultJurisdiction) {
    const select = document.getElementById('jurisdiction');
    if (!select) return;
    
    // Clear existing options
    select.innerHTML = '';
    
    // Add jurisdictions
    jurisdictions.forEach(jurisdiction => {
        const option = document.createElement('option');
        option.value = jurisdiction;
        option.textContent = jurisdiction;
        
        // Set default jurisdiction as selected
        if (jurisdiction === defaultJurisdiction) {
            option.selected = true;
        }
        
        select.appendChild(option);
    });
}

// NDA Loading Modal Functions
function showNDALoadingModal() {
    const modal = document.getElementById('ndaLoadingModal');
    const modalInstance = new bootstrap.Modal(modal);
    modalInstance.show();
    
    // Start cycling through messages
    currentMessageIndex = 0;
    updateLoadingMessage(
        legalLoadingMessages[0].icon,
        legalLoadingMessages[0].message,
        legalLoadingMessages[0].progress
    );
    
    messageInterval = setInterval(() => {
        currentMessageIndex = (currentMessageIndex + 1) % legalLoadingMessages.length;
        const message = legalLoadingMessages[currentMessageIndex];
        updateLoadingMessage(message.icon, message.message, message.progress);
    }, 3000); // Increased to 3 seconds for longer processing
}

function hideNDALoadingModal() {
    const modal = document.getElementById('ndaLoadingModal');
    const modalInstance = bootstrap.Modal.getInstance(modal);
    if (modalInstance) {
        modalInstance.hide();
    }
    
    // Clear message interval
    if (messageInterval) {
        clearInterval(messageInterval);
        messageInterval = null;
    }
}

function updateLoadingMessage(icon, message, progress, status = '') {
    const messageElement = document.getElementById('loadingMessage');
    const progressElement = document.getElementById('loadingProgress');
    
    // Update icon and message
    messageElement.innerHTML = `
        <p class="mb-2"><i class="${icon} ${status === 'success' ? 'loading-success' : status === 'error' ? 'loading-error' : ''}"></i></p>
        <p class="text-muted">${message}</p>
    `;
    
    // Update progress
    progressElement.style.width = `${progress}%`;
    
    // Update title based on status
    const titleElement = document.getElementById('loadingTitle');
    if (status === 'success') {
        titleElement.textContent = 'Document Ready!';
    } else if (status === 'error') {
        titleElement.textContent = 'Generation Failed';
    } else {
        titleElement.textContent = 'Crafting Your Legal Document';
    }
} 