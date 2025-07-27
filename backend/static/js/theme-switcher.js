/**
 * Clausemint Theme Switcher
 * Handles theme switching between dark and light modes
 */

class ThemeSwitcher {
    constructor() {
        this.currentTheme = 'dark'; // Default theme
        this.themeToggle = null;
        this.init();
    }

    init() {
        // Load saved theme from localStorage
        this.loadSavedTheme();
        
        // Create theme switcher element
        this.createThemeSwitcher();
        
        // Add event listeners
        this.addEventListeners();
        
        // Apply initial theme
        this.applyTheme(this.currentTheme);
    }

    loadSavedTheme() {
        const savedTheme = localStorage.getItem('clausemint-theme');
        if (savedTheme && (savedTheme === 'dark' || savedTheme === 'light')) {
            this.currentTheme = savedTheme;
        }
    }

    createThemeSwitcher() {
        // Create theme switcher container
        const themeSwitcher = document.createElement('div');
        themeSwitcher.className = 'theme-switcher';
        themeSwitcher.id = 'theme-switcher';
        
        // Create theme toggle button
        this.themeToggle = document.createElement('button');
        this.themeToggle.className = 'theme-toggle';
        this.themeToggle.setAttribute('aria-label', 'Toggle theme');
        this.themeToggle.setAttribute('title', 'Switch between dark and light themes');
        
        // Set initial icon
        this.updateThemeIcon();
        
        // Append to container
        themeSwitcher.appendChild(this.themeToggle);
        
        // Add to body
        document.body.appendChild(themeSwitcher);
    }

    addEventListeners() {
        // Theme toggle click event
        this.themeToggle.addEventListener('click', () => {
            this.toggleTheme();
        });

        // Keyboard shortcut (Ctrl/Cmd + T)
        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 't') {
                e.preventDefault();
                this.toggleTheme();
            }
        });

        // System theme preference change
        if (window.matchMedia) {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            mediaQuery.addEventListener('change', (e) => {
                // Only auto-switch if user hasn't manually set a preference
                if (!localStorage.getItem('clausemint-theme')) {
                    this.currentTheme = e.matches ? 'dark' : 'light';
                    this.applyTheme(this.currentTheme);
                }
            });
        }
    }

    toggleTheme() {
        this.currentTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        this.applyTheme(this.currentTheme);
        this.saveTheme();
        this.updateThemeIcon();
        
        // Add animation class
        this.themeToggle.classList.add('theme-switching');
        setTimeout(() => {
            this.themeToggle.classList.remove('theme-switching');
        }, 300);
    }

    applyTheme(theme) {
        // Set data attribute on document
        document.documentElement.setAttribute('data-theme', theme);
        
        // Update meta theme-color for mobile browsers
        this.updateMetaThemeColor(theme);
        
        // Trigger custom event for other components
        const event = new CustomEvent('themeChanged', { 
            detail: { theme: theme } 
        });
        document.dispatchEvent(event);
    }

    updateThemeIcon() {
        const icon = this.currentTheme === 'dark' ? '☀️' : '🌙';
        this.themeToggle.innerHTML = icon;
        this.themeToggle.setAttribute('title', 
            this.currentTheme === 'dark' 
                ? 'Switch to light theme' 
                : 'Switch to dark theme'
        );
    }

    updateMetaThemeColor(theme) {
        let metaThemeColor = document.querySelector('meta[name="theme-color"]');
        
        if (!metaThemeColor) {
            metaThemeColor = document.createElement('meta');
            metaThemeColor.name = 'theme-color';
            document.head.appendChild(metaThemeColor);
        }
        
        // Set theme color based on current theme
        const themeColor = theme === 'dark' ? '#040504' : '#e3f2f0';
        metaThemeColor.content = themeColor;
    }

    saveTheme() {
        localStorage.setItem('clausemint-theme', this.currentTheme);
    }

    getCurrentTheme() {
        return this.currentTheme;
    }

    setTheme(theme) {
        if (theme === 'dark' || theme === 'light') {
            this.currentTheme = theme;
            this.applyTheme(theme);
            this.saveTheme();
            this.updateThemeIcon();
        }
    }
}

/**
 * Theme-aware component base class
 * For components that need to react to theme changes
 */
class ThemeAwareComponent {
    constructor() {
        this.currentTheme = 'dark';
        this.init();
    }

    init() {
        // Listen for theme changes
        document.addEventListener('themeChanged', (e) => {
            this.onThemeChange(e.detail.theme);
        });
        
        // Get initial theme
        const themeSwitcher = window.themeSwitcher;
        if (themeSwitcher) {
            this.currentTheme = themeSwitcher.getCurrentTheme();
        }
    }

    onThemeChange(theme) {
        this.currentTheme = theme;
        this.updateTheme();
    }

    updateTheme() {
        // Override this method in child classes
        console.log('Theme changed to:', this.currentTheme);
    }
}

/**
 * Theme utilities
 */
const ThemeUtils = {
    // Get CSS custom property value
    getCSSVariable(property) {
        return getComputedStyle(document.documentElement)
            .getPropertyValue(property).trim();
    },

    // Set CSS custom property value
    setCSSVariable(property, value) {
        document.documentElement.style.setProperty(property, value);
    },

    // Check if current theme is dark
    isDarkTheme() {
        return document.documentElement.getAttribute('data-theme') === 'dark';
    },

    // Check if current theme is light
    isLightTheme() {
        return document.documentElement.getAttribute('data-theme') === 'light';
    },

    // Get theme-aware color
    getThemeColor(colorType) {
        const theme = this.isDarkTheme() ? 'dark' : 'light';
        const colorMap = {
            dark: {
                primary: '#44b28b',
                secondary: '#3eb48c',
                background: '#040504',
                text: '#e7e7e7',
                muted: '#7c7c7c'
            },
            light: {
                primary: '#3eb48c',
                secondary: '#44b28b',
                background: '#e3f2f0',
                text: '#555e5b',
                muted: '#a4a4a4'
            }
        };
        return colorMap[theme][colorType] || colorMap[theme].primary;
    }
};

/**
 * Initialize theme switcher when DOM is ready
 */
document.addEventListener('DOMContentLoaded', () => {
    // Initialize theme switcher
    window.themeSwitcher = new ThemeSwitcher();
    
    // Add theme switcher to global scope
    window.ThemeAwareComponent = ThemeAwareComponent;
    window.ThemeUtils = ThemeUtils;
    
    console.log('🎨 Clausemint Theme Switcher initialized');
    console.log('Current theme:', window.themeSwitcher.getCurrentTheme());
    console.log('Keyboard shortcut: Ctrl/Cmd + T to toggle theme');
});

/**
 * Export for module systems
 */
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ThemeSwitcher, ThemeAwareComponent, ThemeUtils };
} 