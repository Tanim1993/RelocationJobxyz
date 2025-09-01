// Main JavaScript for Relocation Jobs Hub

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Add loading states to buttons
    addLoadingStates();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Setup form enhancements
    setupFormEnhancements();
    
    // Setup job comparison functionality
    setupJobComparison();
    
    // Setup search enhancements
    setupSearchEnhancements();
}

function addLoadingStates() {
    // Add loading states to search and application buttons
    const searchButtons = document.querySelectorAll('button[type="submit"]');
    
    searchButtons.forEach(button => {
        button.addEventListener('click', function() {
            const originalText = this.innerHTML;
            this.classList.add('loading');
            this.disabled = true;
            
            // Remove loading state after 5 seconds (fallback)
            setTimeout(() => {
                this.classList.remove('loading');
                this.disabled = false;
                this.innerHTML = originalText;
            }, 5000);
        });
    });
}

function initializeTooltips() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function setupFormEnhancements() {
    // Auto-submit filters after selection
    const filterSelects = document.querySelectorAll('select[name="job_type"], select[name="location"], select[name="relocation_type"]');
    
    filterSelects.forEach(select => {
        select.addEventListener('change', function() {
            // Small delay to allow user to see the selection
            setTimeout(() => {
                this.closest('form').submit();
            }, 500);
        });
    });
    
    // Clear filters functionality
    const clearFiltersBtn = document.getElementById('clear-filters');
    if (clearFiltersBtn) {
        clearFiltersBtn.addEventListener('click', function() {
            const form = this.closest('form');
            const selects = form.querySelectorAll('select');
            selects.forEach(select => {
                select.value = '';
            });
            form.submit();
        });
    }
}

function setupJobComparison() {
    // Job comparison checkboxes
    const compareCheckboxes = document.querySelectorAll('.compare-job-checkbox');
    const compareButton = document.getElementById('compare-jobs-btn');
    
    if (compareCheckboxes.length > 0) {
        compareCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', updateCompareButton);
        });
    }
    
    function updateCompareButton() {
        const selectedJobs = document.querySelectorAll('.compare-job-checkbox:checked');
        
        if (compareButton) {
            if (selectedJobs.length >= 2) {
                compareButton.style.display = 'block';
                compareButton.textContent = `Compare ${selectedJobs.length} Jobs`;
            } else {
                compareButton.style.display = 'none';
            }
        }
    }
}

function setupSearchEnhancements() {
    // Search suggestions and autocomplete
    const jobTypeInput = document.querySelector('input[name="job_type"]');
    const locationInput = document.querySelector('input[name="location"]');
    
    if (jobTypeInput) {
        setupAutocomplete(jobTypeInput, [
            'QA Engineer', 'Software Engineer', 'Data Scientist', 'DevOps Engineer',
            'Product Manager', 'UX Designer', 'Frontend Developer', 'Backend Developer',
            'Full Stack Developer', 'Machine Learning Engineer', 'Data Analyst',
            'Cybersecurity Specialist', 'Cloud Architect', 'Mobile Developer'
        ]);
    }
    
    if (locationInput) {
        setupAutocomplete(locationInput, [
            'United States', 'Canada', 'United Kingdom', 'Germany', 'Netherlands',
            'Australia', 'New Zealand', 'Singapore', 'Sweden', 'Denmark',
            'Switzerland', 'Ireland', 'Finland', 'Norway', 'Austria'
        ]);
    }
}

function setupAutocomplete(input, suggestions) {
    const suggestionsList = createSuggestionsList(input);
    
    input.addEventListener('input', function() {
        const value = this.value.toLowerCase();
        
        if (value.length < 2) {
            hideSuggestions(suggestionsList);
            return;
        }
        
        const filteredSuggestions = suggestions.filter(suggestion =>
            suggestion.toLowerCase().includes(value)
        );
        
        if (filteredSuggestions.length > 0) {
            showSuggestions(suggestionsList, filteredSuggestions, input);
        } else {
            hideSuggestions(suggestionsList);
        }
    });
    
    // Hide suggestions when clicking outside
    document.addEventListener('click', function(e) {
        if (!input.contains(e.target) && !suggestionsList.contains(e.target)) {
            hideSuggestions(suggestionsList);
        }
    });
}

function createSuggestionsList(input) {
    const suggestionsList = document.createElement('div');
    suggestionsList.className = 'suggestions-list position-absolute bg-white border rounded shadow-sm';
    suggestionsList.style.cssText = `
        top: 100%;
        left: 0;
        right: 0;
        z-index: 1000;
        max-height: 200px;
        overflow-y: auto;
        display: none;
    `;
    
    // Make input container relative for positioning
    input.parentElement.style.position = 'relative';
    input.parentElement.appendChild(suggestionsList);
    
    return suggestionsList;
}

function showSuggestions(suggestionsList, suggestions, input) {
    suggestionsList.innerHTML = '';
    
    suggestions.slice(0, 8).forEach(suggestion => {
        const suggestionItem = document.createElement('div');
        suggestionItem.className = 'suggestion-item px-3 py-2 cursor-pointer';
        suggestionItem.textContent = suggestion;
        suggestionItem.style.cursor = 'pointer';
        
        suggestionItem.addEventListener('mouseenter', function() {
            this.style.backgroundColor = 'var(--bs-primary)';
            this.style.color = 'white';
        });
        
        suggestionItem.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
            this.style.color = '';
        });
        
        suggestionItem.addEventListener('click', function() {
            input.value = suggestion;
            hideSuggestions(suggestionsList);
            input.focus();
        });
        
        suggestionsList.appendChild(suggestionItem);
    });
    
    suggestionsList.style.display = 'block';
}

function hideSuggestions(suggestionsList) {
    suggestionsList.style.display = 'none';
}

// Utility functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} position-fixed top-0 start-50 translate-middle-x mt-3`;
    notification.style.cssText = 'z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check' : type === 'error' ? 'exclamation-triangle' : 'info'}-circle me-2"></i>
        ${message}
        <button type="button" class="btn-close ms-auto" onclick="this.parentElement.remove()"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

function formatSalary(salary) {
    if (!salary) return 'Not specified';
    
    // Format salary numbers with commas
    return salary.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

function shareJob(jobTitle, jobCompany, jobUrl) {
    if (navigator.share) {
        navigator.share({
            title: `${jobTitle} at ${jobCompany}`,
            text: `Check out this relocation opportunity: ${jobTitle} at ${jobCompany}`,
            url: jobUrl || window.location.href
        }).catch(console.error);
    } else {
        // Fallback: copy to clipboard
        const shareText = `${jobTitle} at ${jobCompany} - ${jobUrl || window.location.href}`;
        navigator.clipboard.writeText(shareText).then(() => {
            showNotification('Job link copied to clipboard!', 'success');
        }).catch(() => {
            showNotification('Could not copy to clipboard', 'error');
        });
    }
}

// Analytics and tracking (placeholder for future implementation)
function trackJobView(jobId) {
    // Track job views for analytics
    console.log(`Job ${jobId} viewed`);
}

function trackEmailGeneration(jobId) {
    // Track email template generations
    console.log(`Email template generated for job ${jobId}`);
}

function trackJobApplication(jobId) {
    // Track when users click apply
    console.log(`Application initiated for job ${jobId}`);
}

// Export functions for use in other scripts
window.RelocationJobsHub = {
    showNotification,
    formatSalary,
    shareJob,
    trackJobView,
    trackEmailGeneration,
    trackJobApplication
};
