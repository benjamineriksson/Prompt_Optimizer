/**
 * Lyra Prompt Optimizer Web Application JavaScript
 * Handles UI interactions and API communication for the standalone web app
 */

class LyraWebApp {
    constructor() {
        // REPLACE THIS URL with your production backend URL
        // Example: this.apiUrl = 'https://your-app-name.railway.app';
        this.apiUrl = 'http://localhost:8000'; // UPDATE THIS AFTER DEPLOYMENT
        this.isOptimizing = false;
        
        this.initializeElements();
        this.attachEventListeners();
        this.checkBackendStatus();
        this.loadSavedData();
    }

    initializeElements() {
        // Form elements
        this.rawPromptEl = document.getElementById('rawPrompt');
        this.targetAIEl = document.getElementById('targetAI');
        this.optimizeBtnEl = document.getElementById('optimizeBtn');
        this.btnContentEl = this.optimizeBtnEl.querySelector('.btn-content');
        this.btnLoaderEl = this.optimizeBtnEl.querySelector('.btn-loader');
        
        // Results elements
        this.resultsSectionEl = document.getElementById('resultsSection');
        this.optimizedPromptEl = document.getElementById('optimizedPrompt');
        this.improvementsCardEl = document.getElementById('improvementsCard');
        this.improvementsListEl = document.getElementById('improvementsList');
        this.techniquesCardEl = document.getElementById('techniquesCard');
        this.techniquesListEl = document.getElementById('techniquesList');
        this.proTipCardEl = document.getElementById('proTipCard');
        this.proTipTextEl = document.getElementById('proTipText');
        this.copyBtnEl = document.getElementById('copyBtn');
        this.newOptimizationBtnEl = document.getElementById('newOptimizationBtn');
        
        // Error elements
        this.errorSectionEl = document.getElementById('errorSection');
        this.errorMessageEl = document.getElementById('errorMessage');
        this.retryBtnEl = document.getElementById('retryBtn');
        this.resetBtnEl = document.getElementById('resetBtn');
        
        // Status elements
        this.statusDotEl = document.getElementById('statusDot');
        this.statusTextEl = document.getElementById('statusText');
        this.charCountEl = document.getElementById('charCount');
    }

    attachEventListeners() {
        // Character counter and validation
        this.rawPromptEl.addEventListener('input', () => {
            this.updateCharCounter();
            this.validateInput();
            this.saveFormData();
        });

        // Optimize button
        this.optimizeBtnEl.addEventListener('click', (e) => {
            e.preventDefault();
            this.optimizePrompt();
        });

        // Copy button
        this.copyBtnEl.addEventListener('click', () => this.copyToClipboard());

        // Navigation buttons
        this.newOptimizationBtnEl.addEventListener('click', () => this.resetToInput());
        this.retryBtnEl.addEventListener('click', () => this.optimizePrompt());
        this.resetBtnEl.addEventListener('click', () => this.resetForm());

        // Form change handlers
        document.querySelectorAll('input[name="promptStyle"]').forEach(radio => {
            radio.addEventListener('change', () => {
                this.validateInput();
                this.saveFormData();
            });
        });

        this.targetAIEl.addEventListener('change', () => {
            this.validateInput();
            this.saveFormData();
        });

        // Auto-save on page unload
        window.addEventListener('beforeunload', () => this.saveFormData());

        // Handle Enter key in textarea (Ctrl+Enter to submit)
        this.rawPromptEl.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                e.preventDefault();
                if (!this.isOptimizing && this.validateInput()) {
                    this.optimizePrompt();
                }
            }
        });
    }

    updateCharCounter() {
        const count = this.rawPromptEl.value.length;
        this.charCountEl.textContent = count;
        
        // Update color based on character count
        if (count > 5000) {
            this.charCountEl.style.color = 'var(--error-color)';
        } else if (count > 4500) {
            this.charCountEl.style.color = 'var(--warning-color)';
        } else {
            this.charCountEl.style.color = 'var(--text-muted)';
        }
    }

    validateInput() {
        const prompt = this.rawPromptEl.value.trim();
        const isValid = prompt.length >= 10 && prompt.length <= 5000;
        
        this.optimizeBtnEl.disabled = !isValid || this.isOptimizing;
        
        return isValid;
    }

    async checkBackendStatus() {
        try {
            this.setStatus('loading', 'Checking connection...');
            
            const response = await fetch(`${this.apiUrl}/health`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
                // Add timeout
                signal: AbortSignal.timeout(10000)
            });

            if (response.ok) {
                const data = await response.json();
                if (data.status === 'healthy') {
                    this.setStatus('ready', 'Connected and ready');
                } else {
                    this.setStatus('error', 'Backend service unavailable');
                }
            } else {
                this.setStatus('error', 'Backend connection failed');
            }
        } catch (error) {
            console.error('Backend status check failed:', error);
            this.setStatus('error', 'Backend offline - Please ensure the server is running');
        }
    }

    setStatus(type, message) {
        this.statusTextEl.textContent = message;
        this.statusDotEl.className = `status-dot ${type}`;
    }

    async optimizePrompt() {
        if (this.isOptimizing || !this.validateInput()) return;

        try {
            this.isOptimizing = true;
            this.setLoadingState(true);
            this.hideResults();
            this.hideError();
            this.setStatus('loading', 'Optimizing with Lyra\'s 4-D Methodology...');

            // Collect form data
            const promptStyle = document.querySelector('input[name="promptStyle"]:checked').value;
            const rawPrompt = this.rawPromptEl.value.trim();
            const targetAI = this.targetAIEl.value;

            // Log optimization attempt
            console.log('Starting optimization:', {
                style: promptStyle,
                target: targetAI,
                promptLength: rawPrompt.length
            });

            // Make API request
            const response = await fetch(`${this.apiUrl}/optimize`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    raw_prompt: rawPrompt,
                    prompt_style: promptStyle,
                    target_ai: targetAI
                }),
                // Add timeout
                signal: AbortSignal.timeout(120000) // 2 minutes
            });

            const data = await response.json();

            if (response.ok && !data.error) {
                this.displayResults(data);
                this.setStatus('ready', 'Optimization complete');
                
                // Analytics
                this.trackOptimization(promptStyle, targetAI, true);
            } else {
                throw new Error(data.message || `HTTP ${response.status}: ${response.statusText}`);
            }

        } catch (error) {
            console.error('Optimization error:', error);
            
            let errorMessage = 'Failed to optimize prompt. ';
            
            if (error.name === 'AbortError') {
                errorMessage += 'Request timed out. Please try again.';
            } else if (error.message.includes('NetworkError') || error.message.includes('fetch')) {
                errorMessage += 'Network connection failed. Please check your internet connection and ensure the backend server is running.';
            } else {
                errorMessage += error.message || 'Please try again.';
            }
            
            this.showError(errorMessage);
            this.setStatus('error', 'Optimization failed');
            
            // Analytics
            this.trackOptimization(
                document.querySelector('input[name="promptStyle"]:checked').value,
                this.targetAIEl.value,
                false
            );
        } finally {
            this.isOptimizing = false;
            this.setLoadingState(false);
        }
    }

    setLoadingState(loading) {
        if (loading) {
            this.btnContentEl.style.display = 'none';
            this.btnLoaderEl.style.display = 'flex';
            this.optimizeBtnEl.disabled = true;
        } else {
            this.btnContentEl.style.display = 'flex';
            this.btnLoaderEl.style.display = 'none';
            this.optimizeBtnEl.disabled = !this.validateInput();
        }
    }

    displayResults(data) {
        // Display optimized prompt
        this.optimizedPromptEl.textContent = data.optimized_prompt || data.raw_response;

        // Show improvements
        if (data.improvements && data.improvements.length > 0) {
            this.improvementsListEl.innerHTML = '';
            data.improvements.forEach(improvement => {
                const li = document.createElement('li');
                li.textContent = improvement;
                this.improvementsListEl.appendChild(li);
            });
            this.improvementsCardEl.style.display = 'block';
        } else {
            this.improvementsCardEl.style.display = 'none';
        }

        // Show techniques
        if (data.techniques_applied && data.techniques_applied.length > 0) {
            this.techniquesListEl.textContent = data.techniques_applied.join(', ');
            this.techniquesCardEl.style.display = 'block';
        } else {
            this.techniquesCardEl.style.display = 'none';
        }

        // Show pro tip
        if (data.pro_tip && data.pro_tip.trim()) {
            this.proTipTextEl.textContent = data.pro_tip;
            this.proTipCardEl.style.display = 'block';
        } else {
            this.proTipCardEl.style.display = 'none';
        }

        // Show results section
        this.resultsSectionEl.style.display = 'block';
        
        // Smooth scroll to results
        this.resultsSectionEl.scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });

        // Save successful optimization
        this.saveOptimizationResult(data);
    }

    hideResults() {
        this.resultsSectionEl.style.display = 'none';
    }

    showError(message) {
        this.errorMessageEl.textContent = message;
        this.errorSectionEl.style.display = 'block';
        
        // Scroll to error
        this.errorSectionEl.scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    }

    hideError() {
        this.errorSectionEl.style.display = 'none';
    }

    resetToInput() {
        this.hideError();
        this.hideResults();
        this.setStatus('ready', 'Ready for new optimization');
        
        // Scroll to top
        document.querySelector('.hero').scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    }

    resetForm() {
        this.rawPromptEl.value = '';
        document.querySelector('input[name="promptStyle"][value="BASIC"]').checked = true;
        this.targetAIEl.value = 'ChatGPT';
        
        this.updateCharCounter();
        this.validateInput();
        this.clearSavedData();
        this.resetToInput();
    }

    async copyToClipboard() {
        try {
            const text = this.optimizedPromptEl.textContent;
            await navigator.clipboard.writeText(text);
            
            // Visual feedback
            const originalContent = this.copyBtnEl.innerHTML;
            this.copyBtnEl.innerHTML = '<span class="btn-icon">✓</span>Copied!';
            this.copyBtnEl.style.background = 'var(--success-color)';
            this.copyBtnEl.style.color = 'white';
            
            setTimeout(() => {
                this.copyBtnEl.innerHTML = originalContent;
                this.copyBtnEl.style.background = '';
                this.copyBtnEl.style.color = '';
            }, 2000);
            
        } catch (error) {
            console.error('Copy failed:', error);
            
            // Fallback selection method
            const range = document.createRange();
            range.selectNode(this.optimizedPromptEl);
            window.getSelection().removeAllRanges();
            window.getSelection().addRange(range);
            
            // Show fallback message
            const originalContent = this.copyBtnEl.innerHTML;
            this.copyBtnEl.innerHTML = '<span class="btn-icon">📋</span>Selected';
            
            setTimeout(() => {
                this.copyBtnEl.innerHTML = originalContent;
            }, 2000);
        }
    }

    saveFormData() {
        try {
            const data = {
                rawPrompt: this.rawPromptEl.value,
                promptStyle: document.querySelector('input[name="promptStyle"]:checked').value,
                targetAI: this.targetAIEl.value,
                timestamp: Date.now()
            };
            
            localStorage.setItem('lyra_form_data', JSON.stringify(data));
        } catch (error) {
            console.error('Failed to save form data:', error);
        }
    }

    loadSavedData() {
        try {
            const saved = localStorage.getItem('lyra_form_data');
            if (saved) {
                const data = JSON.parse(saved);
                
                // Only load if data is recent (within 24 hours)
                const isRecent = (Date.now() - data.timestamp) < (24 * 60 * 60 * 1000);
                
                if (isRecent) {
                    if (data.rawPrompt) {
                        this.rawPromptEl.value = data.rawPrompt;
                        this.updateCharCounter();
                    }
                    
                    if (data.promptStyle) {
                        const radio = document.querySelector(`input[name="promptStyle"][value="${data.promptStyle}"]`);
                        if (radio) radio.checked = true;
                    }
                    
                    if (data.targetAI) {
                        this.targetAIEl.value = data.targetAI;
                    }
                    
                    this.validateInput();
                }
            }
        } catch (error) {
            console.error('Failed to load saved data:', error);
        }
    }

    saveOptimizationResult(data) {
        try {
            const result = {
                ...data,
                timestamp: Date.now(),
                input: {
                    raw_prompt: this.rawPromptEl.value,
                    prompt_style: document.querySelector('input[name="promptStyle"]:checked').value,
                    target_ai: this.targetAIEl.value
                }
            };
            
            // Save latest result
            localStorage.setItem('lyra_latest_result', JSON.stringify(result));
            
            // Save to history (keep last 10)
            let history = [];
            try {
                const savedHistory = localStorage.getItem('lyra_optimization_history');
                if (savedHistory) {
                    history = JSON.parse(savedHistory);
                }
            } catch (e) {
                console.error('Failed to load optimization history:', e);
            }
            
            history.unshift(result);
            history = history.slice(0, 10); // Keep only last 10
            
            localStorage.setItem('lyra_optimization_history', JSON.stringify(history));
        } catch (error) {
            console.error('Failed to save optimization result:', error);
        }
    }

    clearSavedData() {
        try {
            localStorage.removeItem('lyra_form_data');
        } catch (error) {
            console.error('Failed to clear saved data:', error);
        }
    }

    trackOptimization(style, targetAI, success) {
        // Simple analytics tracking
        try {
            console.log('Optimization tracked:', {
                style,
                targetAI,
                success,
                timestamp: new Date().toISOString()
            });
        } catch (error) {
            console.error('Analytics tracking failed:', error);
        }
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new LyraWebApp();
});

// Handle browser back/forward navigation
window.addEventListener('popstate', () => {
    // Reset to input view when navigating back
    const app = window.lyraApp;
    if (app && typeof app.resetToInput === 'function') {
        app.resetToInput();
    }
});
