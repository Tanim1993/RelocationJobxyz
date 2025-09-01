/**
 * Cultural Loading Spinners JavaScript Library
 * Provides dynamic loading spinners with cultural themes
 */

class CulturalSpinners {
    constructor() {
        this.themes = {
            asian: {
                name: 'Asian Harmony',
                description: 'Yin-Yang inspired balance',
                messages: ['Finding harmony...', 'Balancing elements...', 'Seeking equilibrium...']
            },
            european: {
                name: 'European Castle',
                description: 'Medieval fortress strength',
                messages: ['Building foundations...', 'Fortifying data...', 'Constructing results...']
            },
            'middle-eastern': {
                name: 'Middle Eastern Mandala',
                description: 'Sacred geometry patterns',
                messages: ['Weaving patterns...', 'Creating sacred geometry...', 'Aligning elements...']
            },
            african: {
                name: 'African Tribal',
                description: 'Vibrant tribal patterns',
                messages: ['Gathering wisdom...', 'Connecting traditions...', 'Celebrating diversity...']
            },
            latin: {
                name: 'Latin American Fiesta',
                description: 'Festive celebration spirit',
                messages: ['Celebrating progress...', 'Dancing with data...', 'Bringing joy to work...']
            },
            nordic: {
                name: 'Nordic Minimalist',
                description: 'Clean Scandinavian design',
                messages: ['Simplifying complexity...', 'Creating clean solutions...', 'Organizing efficiently...']
            },
            native: {
                name: 'Native Dream Catcher',
                description: 'Spiritual protection and guidance',
                messages: ['Catching dreams...', 'Filtering possibilities...', 'Guiding your path...']
            },
            pacific: {
                name: 'Pacific Islander Wave',
                description: 'Ocean flow and movement',
                messages: ['Riding the waves...', 'Flowing with currents...', 'Navigating waters...']
            }
        };
        
        this.activeSpinners = new Map();
        this.init();
    }
    
    init() {
        // Auto-detect and enhance existing spinners
        this.enhanceExistingSpinners();
        
        // Set up form submission interceptors
        this.setupFormInterceptors();
        
        console.log('Cultural Spinners initialized with', Object.keys(this.themes).length, 'themes');
    }
    
    /**
     * Create a cultural spinner
     * @param {string} containerId - ID of container element
     * @param {string} theme - Cultural theme name
     * @param {string} size - Size: 'small', 'normal', 'large'
     * @param {string} message - Custom loading message
     */
    create(containerId, theme = 'asian', size = 'normal', message = null) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error('Container not found:', containerId);
            return null;
        }
        
        const themeData = this.themes[theme] || this.themes.asian;
        const loadingMessage = message || this.getRandomMessage(theme);
        
        const spinnerHtml = `
            <div class="cultural-spinner spinner-${theme} ${size}" id="spinner-${containerId}">
                <div class="spinner-text">${loadingMessage}</div>
            </div>
        `;
        
        container.innerHTML = spinnerHtml;
        this.activeSpinners.set(containerId, {
            theme,
            size,
            message: loadingMessage,
            startTime: Date.now()
        });
        
        // Auto-rotate message every 3 seconds
        this.startMessageRotation(containerId, theme);
        
        return container.querySelector('.cultural-spinner');
    }
    
    /**
     * Remove spinner and show content
     * @param {string} containerId - ID of container element
     * @param {string} content - Content to show after loading
     */
    remove(containerId, content = '') {
        const container = document.getElementById(containerId);
        if (!container) return;
        
        const spinner = this.activeSpinners.get(containerId);
        if (spinner) {
            const duration = Date.now() - spinner.startTime;
            console.log(`Spinner ${containerId} active for ${duration}ms`);
        }
        
        // Fade out animation
        const spinnerElement = container.querySelector('.cultural-spinner');
        if (spinnerElement) {
            spinnerElement.style.opacity = '0';
            spinnerElement.style.transition = 'opacity 0.3s ease-out';
            
            setTimeout(() => {
                container.innerHTML = content;
            }, 300);
        } else {
            container.innerHTML = content;
        }
        
        this.activeSpinners.delete(containerId);
        this.stopMessageRotation(containerId);
    }
    
    /**
     * Get random loading message for theme
     */
    getRandomMessage(theme) {
        const themeData = this.themes[theme] || this.themes.asian;
        const messages = themeData.messages;
        return messages[Math.floor(Math.random() * messages.length)];
    }
    
    /**
     * Start rotating messages for a spinner
     */
    startMessageRotation(containerId, theme) {
        const interval = setInterval(() => {
            const container = document.getElementById(containerId);
            if (!container || !this.activeSpinners.has(containerId)) {
                clearInterval(interval);
                return;
            }
            
            const textElement = container.querySelector('.spinner-text');
            if (textElement) {
                textElement.textContent = this.getRandomMessage(theme);
            }
        }, 3000);
        
        // Store interval for cleanup
        if (this.activeSpinners.has(containerId)) {
            this.activeSpinners.get(containerId).messageInterval = interval;
        }
    }
    
    /**
     * Stop message rotation
     */
    stopMessageRotation(containerId) {
        const spinner = this.activeSpinners.get(containerId);
        if (spinner && spinner.messageInterval) {
            clearInterval(spinner.messageInterval);
        }
    }
    
    /**
     * Enhance existing bootstrap spinners with cultural themes
     */
    enhanceExistingSpinners() {
        const bootstrapSpinners = document.querySelectorAll('.spinner-border, .spinner-grow');
        bootstrapSpinners.forEach((spinner, index) => {
            if (!spinner.classList.contains('cultural-enhanced')) {
                const themes = Object.keys(this.themes);
                const randomTheme = themes[Math.floor(Math.random() * themes.length)];
                
                spinner.classList.add('cultural-enhanced');
                spinner.classList.add(`spinner-${randomTheme}`);
                
                // Add loading text if not present
                if (!spinner.nextElementSibling || !spinner.nextElementSibling.classList.contains('spinner-text')) {
                    const textElement = document.createElement('div');
                    textElement.className = 'spinner-text';
                    textElement.textContent = this.getRandomMessage(randomTheme);
                    spinner.parentNode.insertBefore(textElement, spinner.nextSibling);
                }
            }
        });
    }
    
    /**
     * Setup form submission interceptors to show cultural spinners
     */
    setupFormInterceptors() {
        document.addEventListener('submit', (e) => {
            const form = e.target;
            if (form.tagName === 'FORM' && !form.classList.contains('no-spinner')) {
                // Determine cultural theme based on form context
                const theme = this.determineFormTheme(form);
                
                // Create spinner overlay
                this.showFormSpinner(form, theme);
            }
        });
        
        // Intercept button clicks for AJAX requests
        document.addEventListener('click', (e) => {
            const button = e.target.closest('button, .btn');
            if (button && button.classList.contains('cultural-spinner-trigger')) {
                const theme = button.dataset.culturalTheme || 'asian';
                const containerId = button.dataset.spinnerId || 'default-spinner-container';
                
                // Create spinner container if it doesn't exist
                let container = document.getElementById(containerId);
                if (!container) {
                    container = document.createElement('div');
                    container.id = containerId;
                    container.className = 'text-center my-3';
                    button.parentNode.insertBefore(container, button.nextSibling);
                }
                
                this.create(containerId, theme);
            }
        });
    }
    
    /**
     * Determine cultural theme based on form content and context
     */
    determineFormTheme(form) {
        // Check for data attributes
        if (form.dataset.culturalTheme) {
            return form.dataset.culturalTheme;
        }
        
        // Analyze form content for cultural context
        const formText = form.textContent.toLowerCase();
        
        if (formText.includes('asian') || formText.includes('china') || formText.includes('japan') || formText.includes('harmony')) {
            return 'asian';
        } else if (formText.includes('european') || formText.includes('europe') || formText.includes('medieval')) {
            return 'european';
        } else if (formText.includes('middle') || formText.includes('arabic') || formText.includes('islamic')) {
            return 'middle-eastern';
        } else if (formText.includes('african') || formText.includes('tribal') || formText.includes('safari')) {
            return 'african';
        } else if (formText.includes('latin') || formText.includes('spanish') || formText.includes('fiesta')) {
            return 'latin';
        } else if (formText.includes('nordic') || formText.includes('scandinavian') || formText.includes('minimal')) {
            return 'nordic';
        } else if (formText.includes('native') || formText.includes('indigenous') || formText.includes('dream')) {
            return 'native';
        } else if (formText.includes('pacific') || formText.includes('island') || formText.includes('ocean')) {
            return 'pacific';
        }
        
        // Default to random theme
        const themes = Object.keys(this.themes);
        return themes[Math.floor(Math.random() * themes.length)];
    }
    
    /**
     * Show spinner overlay for form submissions
     */
    showFormSpinner(form, theme) {
        const overlay = document.createElement('div');
        overlay.className = 'form-spinner-overlay';
        overlay.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(255, 255, 255, 0.9);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            border-radius: 0.375rem;
        `;
        
        const spinnerContainer = document.createElement('div');
        spinnerContainer.className = 'text-center';
        
        const spinner = document.createElement('div');
        spinner.className = `cultural-spinner spinner-${theme} large`;
        
        const text = document.createElement('div');
        text.className = 'spinner-text';
        text.textContent = this.getRandomMessage(theme);
        
        spinnerContainer.appendChild(spinner);
        spinnerContainer.appendChild(text);
        overlay.appendChild(spinnerContainer);
        
        // Make form container relative if not already
        if (getComputedStyle(form).position === 'static') {
            form.style.position = 'relative';
        }
        
        form.appendChild(overlay);
        
        // Auto-remove after 10 seconds (safety net)
        setTimeout(() => {
            if (overlay.parentNode) {
                overlay.remove();
            }
        }, 10000);
    }
    
    /**
     * Get list of available themes
     */
    getAvailableThemes() {
        return Object.keys(this.themes).map(key => ({
            key,
            ...this.themes[key]
        }));
    }
    
    /**
     * Create theme selector
     */
    createThemeSelector(containerId, onThemeChange = null) {
        const container = document.getElementById(containerId);
        if (!container) return;
        
        const selector = document.createElement('select');
        selector.className = 'form-select cultural-theme-selector';
        selector.innerHTML = Object.keys(this.themes).map(key => 
            `<option value="${key}">${this.themes[key].name}</option>`
        ).join('');
        
        selector.addEventListener('change', (e) => {
            const selectedTheme = e.target.value;
            if (onThemeChange) {
                onThemeChange(selectedTheme);
            }
            
            // Demo the selected theme
            this.showThemeDemo(selectedTheme);
        });
        
        container.appendChild(selector);
        return selector;
    }
    
    /**
     * Show theme demonstration
     */
    showThemeDemo(theme) {
        let demoContainer = document.getElementById('theme-demo-container');
        if (!demoContainer) {
            demoContainer = document.createElement('div');
            demoContainer.id = 'theme-demo-container';
            demoContainer.className = 'text-center my-3';
            document.body.appendChild(demoContainer);
        }
        
        this.create('theme-demo-container', theme, 'large');
        
        setTimeout(() => {
            this.remove('theme-demo-container', '<p class="text-success">Theme demonstration complete!</p>');
        }, 3000);
    }
}

// Initialize cultural spinners when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    if (!window.culturalSpinners) {
        window.culturalSpinners = new CulturalSpinners();
        console.log('Cultural Spinners library loaded successfully');
    }
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CulturalSpinners;
}

// Prevent duplicate declarations
if (typeof window !== 'undefined' && window.culturalSpinners) {
    console.log('Cultural Spinners already initialized');
} else if (typeof window !== 'undefined') {
    window.culturalSpinners = new CulturalSpinners();
}