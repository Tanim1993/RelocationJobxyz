// Global AI Tools JavaScript Fix
// Ensures all buttons across AI tools are functional

document.addEventListener('DOMContentLoaded', function() {
    console.log('AI Tools JavaScript loaded');
    
    // Fix Language Proficiency Predictor
    const assessmentForm = document.getElementById('assessmentForm');
    if (assessmentForm) {
        assessmentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log('Language assessment form submitted');
            generateLanguagePlan();
        });
    }
    
    // Fix Cultural Intelligence Analyzer
    const culturalForm = document.getElementById('culturalAssessmentForm');
    if (culturalForm) {
        culturalForm.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log('Cultural assessment form submitted');
            generateCulturalAnalysis();
        });
    }
    
    // Fix Language Learning Roadmap buttons
    setupLanguageRoadmapButtons();
    
    // Fix Immigration Law Resources
    const immigrationForm = document.getElementById('immigrationResourceForm');
    if (immigrationForm) {
        console.log('Immigration form found, setting up event listener');
        immigrationForm.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log('Immigration form submitted via global handler');
            generateImmigrationResources();
        });
    }
    
    // Fix Career Path Predictor (if exists)
    const careerForm = document.getElementById('careerForm');
    if (careerForm) {
        console.log('Career form found, setting up event listener');
        careerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log('Career form submitted via global handler');
            generateCareerPathFromForm();
        });
    }
    
    // Global button click handler
    document.addEventListener('click', function(e) {
        const button = e.target.closest('button');
        if (button) {
            console.log('Button clicked:', {
                id: button.id,
                text: button.textContent.trim(),
                className: button.className
            });
            
            // Handle specific button types
            if (button.classList.contains('btn-start-learning')) {
                startLearningJourney();
            } else if (button.classList.contains('btn-complete-challenge')) {
                completeChallenge(button);
            } else if (button.classList.contains('btn-claim-achievement')) {
                claimAchievement(button);
            }
        }
    });
});

// Language Proficiency Predictor Functions
function generateLanguagePlan() {
    try {
        const form = document.getElementById('assessmentForm');
        if (!form) return;
        
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        
        // Validate required fields
        if (!data.target_language || !data.current_level) {
            showMessage('Please fill in all required fields', 'error');
            return;
        }
        
        console.log('Generating language plan for:', data);
        
        // Create results
        const results = createLanguagePlanResults(data);
        displayLanguageResults(results);
        
        showMessage('Language learning plan generated successfully!', 'success');
        
    } catch (error) {
        console.error('Language plan generation error:', error);
        showMessage('Failed to generate plan. Please try again.', 'error');
    }
}

function createLanguagePlanResults(data) {
    const levels = {
        'beginner': 'A1 Beginner',
        'elementary': 'A2 Elementary', 
        'intermediate': 'B1 Intermediate',
        'upper-intermediate': 'B2 Upper-Intermediate',
        'advanced': 'C1 Advanced',
        'proficient': 'C2 Proficient'
    };
    
    const targetLevel = getNextLevel(data.current_level);
    const estimatedTime = calculateLearningTime(data.current_level, targetLevel);
    
    return {
        currentLevel: levels[data.current_level],
        targetLevel: levels[targetLevel],
        language: data.target_language,
        estimatedTime: estimatedTime,
        phases: generateLearningPhases(data),
        resources: generateResources(data.target_language)
    };
}

function getNextLevel(current) {
    const progression = {
        'beginner': 'elementary',
        'elementary': 'intermediate',
        'intermediate': 'upper-intermediate',
        'upper-intermediate': 'advanced',
        'advanced': 'proficient',
        'proficient': 'proficient'
    };
    return progression[current] || 'intermediate';
}

function calculateLearningTime(current, target) {
    const timeMap = {
        'beginner-elementary': '3-4 months',
        'elementary-intermediate': '4-6 months',
        'intermediate-upper-intermediate': '6-8 months',
        'upper-intermediate-advanced': '8-12 months',
        'advanced-proficient': '12+ months'
    };
    return timeMap[`${current}-${target}`] || '6-8 months';
}

function generateLearningPhases(data) {
    return [
        {
            name: 'Foundation Building',
            duration: '4-6 weeks',
            goals: ['Master basic vocabulary (500+ words)', 'Learn essential grammar structures', 'Practice basic conversations'],
            activities: ['Daily vocabulary practice (30 min)', 'Grammar exercises (20 min)', 'Listening practice (15 min)']
        },
        {
            name: 'Skill Development', 
            duration: '6-8 weeks',
            goals: ['Expand vocabulary (1000+ words)', 'Improve pronunciation', 'Write simple texts'],
            activities: ['Reading comprehension', 'Speaking practice with native speakers', 'Writing exercises']
        },
        {
            name: 'Fluency Building',
            duration: '8-10 weeks', 
            goals: ['Achieve conversational fluency', 'Understand media content', 'Professional communication'],
            activities: ['Immersion activities', 'Business language practice', 'Cultural studies']
        }
    ];
}

function generateResources(language) {
    const resources = {
        'English': ['Cambridge English Online', 'BBC Learning English', 'Grammarly'],
        'Spanish': ['SpanishDict', 'Conjuguemos', 'News in Slow Spanish'],
        'French': ['TV5Monde', 'Conjugaison.com', 'RFI Savoirs'],
        'German': ['Deutsche Welle', 'Conjugator', 'GermanPod101'],
        'default': ['Language exchange apps', 'Online tutoring platforms', 'Language learning podcasts']
    };
    return resources[language] || resources['default'];
}

function displayLanguageResults(results) {
    const resultsHTML = `
        <div class="row mt-4">
            <div class="col-12">
                <div class="card shadow">
                    <div class="card-header bg-success text-white">
                        <h5><i class="fas fa-trophy me-2"></i>Your Personalized Learning Plan</h5>
                    </div>
                    <div class="card-body">
                        <div class="row mb-4">
                            <div class="col-md-6">
                                <div class="card h-100">
                                    <div class="card-body text-center">
                                        <h6>Current Level</h6>
                                        <div class="h4 text-primary">${results.currentLevel}</div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="card h-100">
                                    <div class="card-body text-center">
                                        <h6>Target Level</h6>
                                        <div class="h4 text-success">${results.targetLevel}</div>
                                        <small class="text-muted">Estimated: ${results.estimatedTime}</small>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <h6>Learning Phases:</h6>
                        <div class="row">
                            ${results.phases.map((phase, index) => `
                                <div class="col-md-4 mb-3">
                                    <div class="card">
                                        <div class="card-header">
                                            <h6 class="mb-0">Phase ${index + 1}: ${phase.name}</h6>
                                            <small class="text-muted">${phase.duration}</small>
                                        </div>
                                        <div class="card-body">
                                            <strong>Goals:</strong>
                                            <ul class="small">
                                                ${phase.goals.map(goal => `<li>${goal}</li>`).join('')}
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                        
                        <div class="mt-3">
                            <h6>Recommended Resources:</h6>
                            <div class="d-flex flex-wrap gap-2">
                                ${results.resources.map(resource => `<span class="badge bg-primary">${resource}</span>`).join('')}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Insert results after form
    const form = document.getElementById('assessmentForm');
    const existingResults = document.querySelector('.language-results');
    if (existingResults) {
        existingResults.remove();
    }
    
    const resultsDiv = document.createElement('div');
    resultsDiv.className = 'language-results';
    resultsDiv.innerHTML = resultsHTML;
    form.parentNode.insertBefore(resultsDiv, form.nextSibling);
    
    // Scroll to results
    resultsDiv.scrollIntoView({ behavior: 'smooth' });
}

// Cultural Intelligence Functions
function generateCulturalAnalysis() {
    try {
        const form = document.getElementById('culturalAssessmentForm');
        if (!form) return;
        
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        
        if (!data.home_country || !data.target_country) {
            showMessage('Please select both home and target countries', 'error');
            return;
        }
        
        console.log('Generating cultural analysis for:', data);
        
        const analysis = createCulturalAnalysis(data);
        displayCulturalResults(analysis);
        
        showMessage('Cultural intelligence analysis completed!', 'success');
        
    } catch (error) {
        console.error('Cultural analysis error:', error);
        showMessage('Failed to generate analysis. Please try again.', 'error');
    }
}

function createCulturalAnalysis(data) {
    // Calculate cultural intelligence score
    const baseScore = 65;
    const experienceBonus = data.international_experience === 'work' ? 20 : 
                           data.international_experience === 'study' ? 15 : 
                           data.international_experience === 'tourist' ? 5 : 0;
    
    const score = Math.min(100, baseScore + experienceBonus + Math.floor(Math.random() * 15));
    
    return {
        score: score,
        level: score >= 80 ? 'High' : score >= 60 ? 'Moderate' : 'Developing',
        homeCountry: getCountryName(data.home_country),
        targetCountry: getCountryName(data.target_country),
        keyDifferences: generateCulturalDifferences(data.home_country, data.target_country),
        recommendations: generateCulturalRecommendations(score),
        adaptationPlan: generateAdaptationPlan(data)
    };
}

function getCountryName(code) {
    const countries = {
        'us': 'United States', 'uk': 'United Kingdom', 'ca': 'Canada',
        'au': 'Australia', 'de': 'Germany', 'fr': 'France',
        'jp': 'Japan', 'cn': 'China', 'in': 'India',
        'br': 'Brazil', 'mx': 'Mexico', 'other': 'Other'
    };
    return countries[code] || 'Unknown';
}

function generateCulturalDifferences(home, target) {
    const differences = [
        'Communication styles (direct vs. indirect)',
        'Work-life balance expectations',
        'Meeting and presentation formats',
        'Decision-making processes',
        'Social hierarchy and authority'
    ];
    return differences;
}

function generateCulturalRecommendations(score) {
    if (score >= 80) {
        return [
            'You show strong cultural awareness',
            'Focus on specific cultural nuances',
            'Consider becoming a cultural mentor',
            'Share your experiences with others'
        ];
    } else if (score >= 60) {
        return [
            'Develop deeper cultural understanding',
            'Practice active observation skills',
            'Engage with local communities',
            'Read about cultural business practices'
        ];
    } else {
        return [
            'Start with basic cultural research',
            'Watch documentaries about the target culture',
            'Connect with cultural exchange groups',
            'Practice open-minded conversations'
        ];
    }
}

function generateAdaptationPlan(data) {
    return [
        'Week 1-2: Research cultural basics and etiquette',
        'Week 3-4: Practice communication styles',
        'Month 2: Engage with local communities',
        'Month 3: Develop professional relationships'
    ];
}

function displayCulturalResults(analysis) {
    const resultsHTML = `
        <div class="row mt-4">
            <div class="col-12">
                <div class="card shadow">
                    <div class="card-header bg-info text-white">
                        <h5><i class="fas fa-compass me-2"></i>Your Cultural Intelligence Report</h5>
                    </div>
                    <div class="card-body">
                        <div class="row mb-4">
                            <div class="col-md-4 text-center">
                                <div class="card">
                                    <div class="card-body">
                                        <div class="display-4 text-primary">${analysis.score}</div>
                                        <h6>Cultural Intelligence Score</h6>
                                        <span class="badge ${analysis.level === 'High' ? 'bg-success' : analysis.level === 'Moderate' ? 'bg-warning' : 'bg-secondary'}">${analysis.level}</span>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-8">
                                <h6>Cultural Transition: ${analysis.homeCountry} → ${analysis.targetCountry}</h6>
                                <div class="row">
                                    <div class="col-12">
                                        <h6 class="mt-3">Key Cultural Differences to Consider:</h6>
                                        <ul>
                                            ${analysis.keyDifferences.map(diff => `<li>${diff}</li>`).join('')}
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6">
                                <h6>Personalized Recommendations:</h6>
                                <ul>
                                    ${analysis.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                                </ul>
                            </div>
                            <div class="col-md-6">
                                <h6>Adaptation Plan:</h6>
                                <ul>
                                    ${analysis.adaptationPlan.map(step => `<li>${step}</li>`).join('')}
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    const form = document.getElementById('culturalAssessmentForm');
    const existingResults = document.querySelector('.cultural-results');
    if (existingResults) {
        existingResults.remove();
    }
    
    const resultsDiv = document.createElement('div');
    resultsDiv.className = 'cultural-results';
    resultsDiv.innerHTML = resultsHTML;
    form.parentNode.insertBefore(resultsDiv, form.nextSibling);
    
    resultsDiv.scrollIntoView({ behavior: 'smooth' });
}

// Language Learning Roadmap Functions
function setupLanguageRoadmapButtons() {
    // Initialize gamification elements
    if (document.querySelector('.language-roadmap')) {
        initializeGameElements();
    }
}

function initializeGameElements() {
    // Set up default user stats if not present
    const userStats = {
        current_level: 1,
        total_xp: 120,
        streak_days: 5,
        badges_earned: 3,
        level_progress: 65
    };
    
    // Update display elements
    updateStatsDisplay(userStats);
}

function updateStatsDisplay(stats) {
    const elements = {
        '.current-level': stats.current_level,
        '.total-xp': stats.total_xp,
        '.streak-days': stats.streak_days,
        '.badges-earned': stats.badges_earned
    };
    
    Object.entries(elements).forEach(([selector, value]) => {
        const element = document.querySelector(selector);
        if (element) element.textContent = value;
    });
}

function startLearningJourney() {
    showMessage('Learning journey started! Complete daily challenges to earn XP.', 'success');
    updateProgress(25);
}

function completeChallenge(button) {
    const xpGain = Math.floor(Math.random() * 50) + 25;
    button.textContent = 'Completed!';
    button.classList.add('btn-success');
    button.disabled = true;
    
    showMessage(`Challenge completed! +${xpGain} XP earned.`, 'success');
    updateProgress(xpGain);
}

function claimAchievement(button) {
    button.textContent = 'Claimed!';
    button.classList.add('btn-success');
    button.disabled = true;
    
    showMessage('Achievement unlocked! Badge added to your collection.', 'success');
}

function updateProgress(xpGain) {
    // Update XP display
    const xpElement = document.querySelector('.total-xp');
    if (xpElement) {
        const currentXP = parseInt(xpElement.textContent) + xpGain;
        xpElement.textContent = currentXP;
    }
}

// Utility Functions
function showMessage(message, type = 'info') {
    const alertClass = type === 'error' ? 'alert-danger' : 
                      type === 'success' ? 'alert-success' : 'alert-info';
    
    const alertHTML = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            <i class="fas ${type === 'error' ? 'fa-exclamation-triangle' : type === 'success' ? 'fa-check-circle' : 'fa-info-circle'} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        const alertDiv = document.createElement('div');
        alertDiv.innerHTML = alertHTML;
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            const alert = alertDiv.querySelector('.alert');
            if (alert) alert.remove();
        }, 5000);
    }
    
    console.log(`${type.toUpperCase()}: ${message}`);
}

// Career Path Functions
function generateCareerPathFromForm() {
    try {
        console.log('Generating career path from global handler');
        const form = document.getElementById('careerForm');
        if (!form) {
            console.error('Career form not found');
            return;
        }
        
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        
        console.log('Career form data:', data);
        
        // Validate required fields
        if (!data.current_role || !data.experience || !data.industry || !data.goal) {
            showMessage('Please fill in all required fields', 'error');
            return;
        }
        
        // Generate career prediction
        const prediction = createCareerPrediction(data);
        displayCareerResults(prediction);
        
        showMessage('Career path generated successfully!', 'success');
        
    } catch (error) {
        console.error('Career path generation error:', error);
        showMessage('Failed to generate career path. Please try again.', 'error');
    }
}

function createCareerPrediction(data) {
    const careerPaths = {
        technology: {
            leadership: {
                nextRole: "Senior Software Engineer",
                nextRoleDescription: "Lead technical projects and mentor junior developers while building management skills.",
                timeline: "1-2 years",
                longTermRole: "Engineering Manager",
                longTermDescription: "Manage engineering teams and drive technical strategy for products.",
                salaryRange: "$140k - $200k+",
                skillsNeeded: ["Team leadership", "Project management", "Strategic thinking", "Communication"],
                actionSteps: ["Take on team lead responsibilities", "Complete management training", "Build stakeholder relationships", "Develop technical vision"],
                advice: "Focus on developing both technical excellence and people management skills. Start mentoring others and taking on cross-functional projects."
            },
            technical: {
                nextRole: "Senior Developer/Architect",
                nextRoleDescription: "Become the go-to technical expert and design complex systems.",
                timeline: "1-2 years",
                longTermRole: "Principal Engineer/CTO",
                longTermDescription: "Lead technical architecture decisions and innovation across the organization.",
                salaryRange: "$160k - $250k+",
                skillsNeeded: ["System design", "Advanced programming", "Architecture patterns", "Technical leadership"],
                actionSteps: ["Master advanced technologies", "Contribute to open source", "Design system architecture", "Mentor other engineers"],
                advice: "Deepen your technical expertise in emerging technologies and focus on system design and architecture skills."
            }
        },
        finance: {
            leadership: {
                nextRole: "Senior Financial Analyst",
                nextRoleDescription: "Lead financial planning initiatives and guide strategic decisions.",
                timeline: "1-2 years",
                longTermRole: "Finance Director",
                longTermDescription: "Oversee financial operations and strategy for business units.",
                salaryRange: "$130k - $190k+",
                skillsNeeded: ["Strategic planning", "Team management", "Financial modeling", "Executive communication"],
                actionSteps: ["Lead major financial projects", "Complete MBA or CFA", "Build executive relationships", "Develop business acumen"],
                advice: "Combine financial expertise with business strategy knowledge. Focus on becoming a strategic business partner."
            }
        },
        default: {
            nextRole: "Senior Professional",
            nextRoleDescription: "Advance to a senior level in your current field with expanded responsibilities.",
            timeline: "1-2 years",
            longTermRole: "Department Leader",
            longTermDescription: "Lead a team or department in your area of expertise.",
            salaryRange: "$100k - $150k+",
            skillsNeeded: ["Leadership", "Communication", "Strategic thinking", "Industry expertise"],
            actionSteps: ["Take on leadership roles", "Develop expertise", "Build professional network", "Pursue relevant certifications"],
            advice: "Focus on developing both technical skills and leadership capabilities. Build strong relationships within your industry."
        }
    };
    
    // Get specific prediction or use default
    let prediction = careerPaths.default;
    if (careerPaths[data.industry] && careerPaths[data.industry][data.goal]) {
        prediction = careerPaths[data.industry][data.goal];
    }
    
    // Adjust timeline based on experience
    let timeline = prediction.timeline;
    if (data.experience === '0-1') {
        timeline = timeline.replace('1-2', '2-3');
    } else if (data.experience === '10+') {
        timeline = timeline.replace('2-3', '1-2');
    }
    
    return {
        ...prediction,
        timeline: timeline
    };
}

function displayCareerResults(prediction) {
    const resultsHTML = `
        <div class="row">
            <div class="col-md-6">
                <div class="card h-100">
                    <div class="card-header">
                        <h6 class="mb-0"><i class="fas fa-target me-2"></i>Recommended Next Step</h6>
                    </div>
                    <div class="card-body">
                        <h5 class="text-primary">${prediction.nextRole}</h5>
                        <p>${prediction.nextRoleDescription}</p>
                        <div class="timeline-estimate">
                            <small class="text-muted">
                                <i class="fas fa-clock me-1"></i>Timeline: ${prediction.timeline}
                            </small>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card h-100">
                    <div class="card-header">
                        <h6 class="mb-0"><i class="fas fa-chart-line me-2"></i>Long-term Vision</h6>
                    </div>
                    <div class="card-body">
                        <h5 class="text-success">${prediction.longTermRole}</h5>
                        <p>${prediction.longTermDescription}</p>
                        <div class="salary-estimate">
                            <small class="text-muted">
                                <i class="fas fa-dollar-sign me-1"></i>Potential salary: ${prediction.salaryRange}
                            </small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row mt-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h6 class="mb-0"><i class="fas fa-list-check me-2"></i>Action Plan</h6>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6">
                                <h6 class="text-primary">Skills to Develop:</h6>
                                <ul class="list-unstyled">
                                    ${prediction.skillsNeeded.map(skill => `<li><i class="fas fa-arrow-right text-primary me-2"></i>${skill}</li>`).join('')}
                                </ul>
                            </div>
                            <div class="col-md-6">
                                <h6 class="text-primary">Next Steps:</h6>
                                <ul class="list-unstyled">
                                    ${prediction.actionSteps.map(step => `<li><i class="fas fa-check-circle text-success me-2"></i>${step}</li>`).join('')}
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row mt-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h6 class="mb-0"><i class="fas fa-lightbulb me-2"></i>Career Advice</h6>
                    </div>
                    <div class="card-body">
                        <div class="alert alert-info">
                            <strong>Personalized Recommendation:</strong> ${prediction.advice}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Insert results
    const resultsSection = document.getElementById('resultsSection');
    const resultsContent = document.getElementById('resultsContent');
    
    if (resultsContent) {
        resultsContent.innerHTML = resultsHTML;
        if (resultsSection) {
            resultsSection.style.display = 'block';
            resultsSection.scrollIntoView({ behavior: 'smooth' });
        }
    } else {
        console.error('Results sections not found');
    }
}

function generateCareerPath() {
    // Fallback function for compatibility
    generateCareerPathFromForm();
}

console.log('AI Tools JavaScript Fix loaded successfully');

// Initialize cultural spinners integration
document.addEventListener('DOMContentLoaded', function() {
    // Add cultural spinner support to all AI tool forms
    const aiToolForms = document.querySelectorAll('form[id*="Form"], form[class*="ai-tool"]');
    aiToolForms.forEach(form => {
        if (!form.classList.contains('no-spinner')) {
            // Auto-detect cultural theme based on tool type
            const formId = form.id || '';
            let theme = 'asian'; // default
            
            if (formId.includes('language') || formId.includes('proficiency')) {
                theme = 'asian';
            } else if (formId.includes('cultural') || formId.includes('intelligence')) {
                theme = 'middle-eastern';
            } else if (formId.includes('career') || formId.includes('guidance')) {
                theme = 'european';
            } else if (formId.includes('salary') || formId.includes('intelligence')) {
                theme = 'nordic';
            } else if (formId.includes('immigration') || formId.includes('law')) {
                theme = 'native';
            } else if (formId.includes('roadmap') || formId.includes('learning')) {
                theme = 'latin';
            }
            
            form.setAttribute('data-cultural-theme', theme);
        }
    });
    
    // Enhance submit buttons with cultural spinner triggers
    const submitButtons = document.querySelectorAll('button[type="submit"], .btn-primary');
    submitButtons.forEach(button => {
        if (!button.classList.contains('cultural-spinner-trigger')) {
            button.classList.add('cultural-spinner-trigger');
            
            // Set theme based on context
            const formParent = button.closest('form');
            if (formParent && formParent.getAttribute('data-cultural-theme')) {
                button.setAttribute('data-cultural-theme', formParent.getAttribute('data-cultural-theme'));
            }
        }
    });
});