# Clausemint Theme System

## Overview

The Clausemint theme system provides a comprehensive dark and light theme implementation with smooth transitions and persistent user preferences. The system is built using CSS custom properties (CSS variables) and JavaScript for dynamic theme switching.

## 🎨 Color Palettes

### Dark Theme (Default)
- **Background Primary**: `#040504` (Marshland)
- **Background Secondary**: `#0a0a0a` (Slightly lighter dark)
- **Background Tertiary**: `#111111` (Card backgrounds)
- **Background Elevated**: `#1a1a1a` (Elevated elements)
- **Text Primary**: `#e7e7e7` (Mercury - Input text, text)
- **Text Secondary**: `#7c7c7c` (Boulder - Inactive text, tip)
- **Accent Primary**: `#44b28b` (Ocean Green - Lines, borders, separators, Title Text)
- **Accent Secondary**: `#3eb48c` (Keppel - Alternative accent)
- **Border Primary**: `#44b28b` (Ocean Green - Lines, borders, separators)

### Light Theme
- **Background Primary**: `#e3f2f0` (Aqua Squeeze)
- **Background Secondary**: `#f0f8f7` (Slightly darker light)
- **Background Tertiary**: `#ffffff` (Card backgrounds)
- **Background Elevated**: `#f8f9fa` (Elevated elements)
- **Text Primary**: `#555e5b` (Nandor - Input text, text)
- **Text Secondary**: `#a4a4a4` (Silver Chalice - Inactive text, tip)
- **Accent Primary**: `#3eb48c` (Keppel - Lines, borders, separators, Title Text)
- **Accent Secondary**: `#44b28b` (Ocean Green - Alternative accent)
- **Border Primary**: `#3eb48c` (Keppel - Lines, borders, separators)

## 📁 File Structure

```
backend/static/css/
├── themes.css              # Main theme system with CSS variables
├── main.css               # Application styles (imports themes.css)
└── theme-demo.css         # Demo styles for showcasing themes

backend/static/js/
└── theme-switcher.js      # Theme switching functionality

backend/templates/
└── index.html             # Includes theme-switcher.js
```

## 🔧 Implementation

### CSS Variables System

The theme system uses CSS custom properties defined in `themes.css`:

```css
:root {
    /* Dark Theme (Default) */
    --bg-primary: #040504;
    --bg-secondary: #0a0a0a;
    --text-primary: #e7e7e7;
    --accent-primary: #44b28b;
    /* ... more variables */
}

[data-theme="light"] {
    /* Light Theme */
    --bg-primary: #e3f2f0;
    --bg-secondary: #f0f8f7;
    --text-primary: #555e5b;
    --accent-primary: #3eb48c;
    /* ... more variables */
}
```

### JavaScript Theme Switcher

The `ThemeSwitcher` class provides:

- **Automatic theme detection** from localStorage
- **Smooth transitions** between themes
- **Keyboard shortcuts** (Ctrl/Cmd + T)
- **System theme preference** detection
- **Persistent theme storage**

```javascript
// Initialize theme switcher
window.themeSwitcher = new ThemeSwitcher();

// Switch themes programmatically
themeSwitcher.setTheme('light');
themeSwitcher.setTheme('dark');

// Get current theme
const currentTheme = themeSwitcher.getCurrentTheme();
```

## 🎯 Features

### 1. Theme Switching
- **Floating theme toggle** in top-right corner
- **Keyboard shortcut**: `Ctrl/Cmd + T`
- **Smooth transitions** for all elements
- **Persistent storage** in localStorage

### 2. System Integration
- **Automatic detection** of system theme preference
- **Meta theme-color** updates for mobile browsers
- **Custom events** for theme change notifications

### 3. Component Support
- **All UI components** automatically adapt to theme
- **RAG colors** (Red/Amber/Green) work in both themes
- **Form elements** with proper focus states
- **Modal dialogs** with theme-aware styling

### 4. Accessibility
- **High contrast** ratios in both themes
- **Focus indicators** with theme colors
- **Screen reader** friendly theme toggle
- **Keyboard navigation** support

## 🚀 Usage

### Basic Implementation

1. **Include CSS files**:
```html
<link rel="stylesheet" href="{% static 'css/themes.css' %}">
<link rel="stylesheet" href="{% static 'css/main.css' %}">
```

2. **Include JavaScript**:
```html
<script src="{% static 'js/theme-switcher.js' %}"></script>
```

3. **Theme switcher automatically initializes** and creates the toggle button.

### Advanced Usage

#### Theme-Aware Components

Create components that react to theme changes:

```javascript
class MyComponent extends ThemeAwareComponent {
    updateTheme() {
        // Update component when theme changes
        const isDark = this.currentTheme === 'dark';
        this.element.style.background = isDark ? '#040504' : '#e3f2f0';
    }
}
```

#### Theme Utilities

Use the `ThemeUtils` helper:

```javascript
// Check current theme
if (ThemeUtils.isDarkTheme()) {
    // Dark theme specific logic
}

// Get theme-aware color
const primaryColor = ThemeUtils.getThemeColor('primary');

// Set CSS variable
ThemeUtils.setCSSVariable('--custom-color', '#ff0000');
```

#### Custom Theme Events

Listen for theme changes:

```javascript
document.addEventListener('themeChanged', (e) => {
    console.log('Theme changed to:', e.detail.theme);
    // Update your component
});
```

## 🎨 Customization

### Adding New Colors

1. **Add to CSS variables** in `themes.css`:
```css
:root {
    --custom-color: #123456;
}

[data-theme="light"] {
    --custom-color: #654321;
}
```

2. **Use in your CSS**:
```css
.my-element {
    background-color: var(--custom-color);
}
```

### Creating New Themes

1. **Add new theme data attribute**:
```css
[data-theme="custom"] {
    --bg-primary: #your-color;
    --text-primary: #your-color;
    /* ... other variables */
}
```

2. **Update JavaScript** to support the new theme:
```javascript
themeSwitcher.setTheme('custom');
```

## 📱 Responsive Design

The theme system includes responsive design considerations:

- **Mobile-friendly** theme toggle positioning
- **Touch-friendly** button sizes
- **Responsive color palettes** for different screen sizes
- **Print styles** that automatically use light theme

## 🔍 Browser Support

- **Modern browsers**: Full support with CSS custom properties
- **Fallback**: Graceful degradation for older browsers
- **Progressive enhancement**: Theme switching works even without CSS variables

## 🧪 Testing

### Manual Testing
1. **Load the application** - should default to dark theme
2. **Click theme toggle** - should switch to light theme
3. **Refresh page** - should remember the selected theme
4. **Use keyboard shortcut** - `Ctrl/Cmd + T` should toggle theme
5. **Check all components** - forms, buttons, modals, etc.

### Automated Testing
```javascript
// Test theme switching
describe('Theme System', () => {
    it('should switch between themes', () => {
        const switcher = new ThemeSwitcher();
        expect(switcher.getCurrentTheme()).toBe('dark');
        
        switcher.setTheme('light');
        expect(switcher.getCurrentTheme()).toBe('light');
    });
});
```

## 🐛 Troubleshooting

### Common Issues

1. **Theme not switching**:
   - Check if `theme-switcher.js` is loaded
   - Verify CSS variables are defined
   - Check browser console for errors

2. **Styles not updating**:
   - Ensure elements use CSS variables
   - Check for hardcoded colors
   - Verify CSS specificity

3. **Theme not persisting**:
   - Check localStorage permissions
   - Verify localStorage is available
   - Check for JavaScript errors

### Debug Mode

Enable debug logging:

```javascript
// Add to theme-switcher.js
const DEBUG = true;

if (DEBUG) {
    console.log('Theme system debug:', {
        currentTheme: this.currentTheme,
        savedTheme: localStorage.getItem('clausemint-theme'),
        systemPreference: window.matchMedia('(prefers-color-scheme: dark)').matches
    });
}
```

## 📚 Best Practices

### CSS Guidelines
- **Always use CSS variables** instead of hardcoded colors
- **Test both themes** for all new components
- **Use semantic variable names** (e.g., `--text-primary` not `--color-1`)
- **Include transitions** for smooth theme switching

### JavaScript Guidelines
- **Listen for theme events** instead of polling
- **Use the ThemeAwareComponent** base class for new components
- **Test theme switching** in your component logic
- **Handle theme changes** gracefully

### Design Guidelines
- **Maintain contrast ratios** in both themes
- **Use consistent spacing** and typography
- **Test with real content** not just placeholder text
- **Consider accessibility** in both themes

## 🔮 Future Enhancements

### Planned Features
- **Custom theme builder** for users
- **Theme presets** (high contrast, sepia, etc.)
- **Automatic theme scheduling** (dark at night)
- **Theme analytics** and usage tracking

### Performance Optimizations
- **CSS-in-JS** for dynamic themes
- **Theme preloading** for faster switching
- **Compressed CSS variables** for smaller bundle size
- **Lazy loading** for theme-specific assets

---

**Summary**: The Clausemint theme system provides a robust, accessible, and user-friendly way to switch between dark and light themes with smooth transitions and persistent preferences. 