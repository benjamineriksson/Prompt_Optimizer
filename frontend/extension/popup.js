/**
 * Lyra Prompt Optimizer Extension JavaScript
 * Handles UI interactions and API communication
 */

class PromptOptimizerExtension {
    constructor() {
        // Production backend URL on Railway
        this.apiUrl = 'https://promptoptimizer-production.up.railway.app';
        this.isOptimizing = false;
        
        this.initializeElements();
        this.attachEventListeners();
        this.checkBackendStatus();
    }

    initializeElements() {
        // Form elements
        this.rawPromptEl = document.getElementById('rawPrompt');
        this.targetAIEl = document.getElementById('targetAI');
        this.optimizeBtnEl = document.getElementById('optimizeBtn');
        this.btnTextEl = this.optimizeBtnEl.querySelector('.btn-text');
        this.btnLoaderEl = this.optimizeBtnEl.querySelector('.btn-loader');
        
        // Output elements
        this.outputSectionEl = document.getElementById('outputSection');
        this.optimizedPromptEl = document.getElementById('optimizedPrompt');
        this.improvementsEl = document.getElementById('improvements');
        this.improvementsListEl = document.getElementById('improvementsList');
        this.techniquesEl = document.getElementById('techniques');
        this.techniquesListEl = document.getElementById('techniquesList');
        this.proTipEl = document.getElementById('proTip');
        this.proTipTextEl = document.getElementById('proTipText');
        this.copyBtnEl = document.getElementById('copyBtn');
        
        // Error elements
        this.errorSectionEl = document.getElementById('errorSection');
        this.errorMessageEl = document.getElementById('errorMessage');
        this.retryBtnEl = document.getElementById('retryBtn');
        
        // Status elements
        this.statusDotEl = document.getElementById('statusDot');
        this.statusTextEl = document.getElementById('statusText');
        this.charCountEl = document.getElementById('charCount');
    }

    attachEventListeners() {
        // Character counter
        this.rawPromptEl.addEventListener('input', () => {
            this.updateCharCounter();
            this.validateInput();
        });

        // Optimize button
        this.optimizeBtnEl.addEventListener('click', () => this.optimizePrompt());

        // Copy button
        this.copyBtnEl.addEventListener('click', () => this.copyToClipboard());

        // Retry button
        this.retryBtnEl.addEventListener('click', () => this.resetToInput());

        // Form validation on change
        document.querySelectorAll('input[name="promptStyle"]').forEach(radio => {
            radio.addEventListener('change', () => this.validateInput());
        });

        this.targetAIEl.addEventListener('change', () => this.validateInput());

        // Load saved data
        this.loadSavedData();
    }

    updateCharCounter() {
        const count = this.rawPromptEl.value.length;
        this.charCountEl.textContent = count;
        
        if (count > 5000) {
            this.charCountEl.style.color = '#dc2626';
        } else if (count > 4500) {
            this.charCountEl.style.color = '#f59e0b';
        } else {
            this.charCountEl.style.color = '#6b7280';
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
                }
            });

            if (response.ok) {
                const data = await response.json();
                if (data.status === 'healthy') {
                    this.setStatus('ready', 'Ready');
                } else {
                    this.setStatus('error', 'API unavailable');
                }
            } else {
                this.setStatus('error', 'Connection failed');
            }
        } catch (error) {
            console.error('Backend status check failed:', error);
            this.setStatus('error', 'Backend offline');
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
            this.hideOutput();
            this.hideError();
            this.setStatus('loading', 'Optimizing...');

            // Collect form data
            const promptStyle = document.querySelector('input[name="promptStyle"]:checked').value;
            const rawPrompt = this.rawPromptEl.value.trim();
            const targetAI = this.targetAIEl.value;

            // Save form data
            this.saveFormData({ rawPrompt, promptStyle, targetAI });

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
                })
            });

            const data = await response.json();

            if (response.ok && !data.error) {
                this.displayResult(data);
                this.setStatus('ready', 'Optimization complete');
            } else {
                throw new Error(data.message || 'Optimization failed');
            }

        } catch (error) {
            console.error('Optimization error:', error);
            this.showError(error.message || 'Failed to optimize prompt. Please try again.');
            this.setStatus('error', 'Optimization failed');
        } finally {
            this.isOptimizing = false;
            this.setLoadingState(false);
        }
    }

    setLoadingState(loading) {
        if (loading) {
            this.btnTextEl.style.display = 'none';
            this.btnLoaderEl.style.display = 'flex';
            this.optimizeBtnEl.disabled = true;
        } else {
            this.btnTextEl.style.display = 'block';
            this.btnLoaderEl.style.display = 'none';
            this.optimizeBtnEl.disabled = !this.validateInput();
        }
    }

    displayResult(data) {
        // Show optimized prompt
        this.optimizedPromptEl.textContent = data.optimized_prompt || data.raw_response;

        // Show improvements
        if (data.improvements && data.improvements.length > 0) {
            this.improvementsListEl.innerHTML = '';
            data.improvements.forEach(improvement => {
                const li = document.createElement('li');
                li.textContent = improvement;
                this.improvementsListEl.appendChild(li);
            });
            this.improvementsEl.style.display = 'block';
        } else {
            this.improvementsEl.style.display = 'none';
        }

        // Show techniques
        if (data.techniques_applied && data.techniques_applied.length > 0) {
            this.techniquesListEl.textContent = data.techniques_applied.join(', ');
            this.techniquesEl.style.display = 'block';
        } else {
            this.techniquesEl.style.display = 'none';
        }

        // Show pro tip
        if (data.pro_tip) {
            this.proTipTextEl.textContent = data.pro_tip;
            this.proTipEl.style.display = 'block';
        } else {
            this.proTipEl.style.display = 'none';
        }

        this.outputSectionEl.style.display = 'block';
        
        // Scroll to output
        this.outputSectionEl.scrollIntoView({ behavior: 'smooth' });
    }

    hideOutput() {
        this.outputSectionEl.style.display = 'none';
    }

    showError(message) {
        this.errorMessageEl.textContent = message;
        this.errorSectionEl.style.display = 'block';
        this.errorSectionEl.scrollIntoView({ behavior: 'smooth' });
    }

    hideError() {
        this.errorSectionEl.style.display = 'none';
    }

    resetToInput() {
        this.hideError();
        this.hideOutput();
        this.setStatus('ready', 'Ready');
    }

    async copyToClipboard() {
        try {
            const text = this.optimizedPromptEl.textContent;
            await navigator.clipboard.writeText(text);
            
            // Visual feedback
            const originalText = this.copyBtnEl.textContent;
            this.copyBtnEl.textContent = '✓ Copied!';
            this.copyBtnEl.style.background = '#10b981';
            
            setTimeout(() => {
                this.copyBtnEl.textContent = originalText;
                this.copyBtnEl.style.background = '';
            }, 2000);
            
        } catch (error) {
            console.error('Copy failed:', error);
            // Fallback selection method
            const range = document.createRange();
            range.selectNode(this.optimizedPromptEl);
            window.getSelection().removeAllRanges();
            window.getSelection().addRange(range);
        }
    }

    saveFormData(data) {
        try {
            chrome.storage.local.set({
                lyra_form_data: data
            });
        } catch (error) {
            console.error('Failed to save form data:', error);
        }
    }

    loadSavedData() {
        try {
            chrome.storage.local.get(['lyra_form_data'], (result) => {
                if (result.lyra_form_data) {
                    const data = result.lyra_form_data;
                    
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
            });
        } catch (error) {
            console.error('Failed to load saved data:', error);
        }
    }
}

// Initialize the extension when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new PromptOptimizerExtension();
});
