
function toggleTheme() {
    const currentTheme = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.classList.remove(currentTheme);
    document.documentElement.classList.add(newTheme);

    // Change icon based on the new theme
    const icon = document.getElementById('theme-icon');
    icon.src = newTheme === 'dark' ? "{% static 'images/dark-mode-toggle-icon.svg' %}" : "{% static 'images/dark-mode-toggle-icon.svg' %}";

    localStorage.setItem('theme', newTheme);
}

document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.classList.add(savedTheme);

        // Set icon based on the saved theme
        const icon = document.getElementById('theme-icon');
        icon.src = savedTheme === 'dark' ? "{% static 'images/dark-mode-toggle-icon.svg' %}" : "{% static 'images/dark-mode-toggle-icon.svg' %}";
    } else {
        document.documentElement.classList.add('light');
    }
});

