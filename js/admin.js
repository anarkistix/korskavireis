// Admin Panel JavaScript
const ADMIN_PASSWORD = 'iunc67eus';
let countriesData = [];
let currentCountry = null;

// Initialize admin panel
document.addEventListener('DOMContentLoaded', function() {
    loadCountriesData();
    updateSystemStatus();
    loadCurrentSettings();
});

// Load current settings from config.json or localStorage
async function loadCurrentSettings() {
    try {
        // First check global config (highest priority)
        const globalConfig = localStorage.getItem('globalGameConfig');
        if (globalConfig) {
            const config = JSON.parse(globalConfig);
            console.log('Loaded global config:', config);
            
            document.getElementById('game-mode').value = config.gameMode || 'random';
            document.getElementById('specific-country').value = config.specificCountry || '';
            toggleCountrySelect();
            return;
        }
        
        // Then check shared config
        const sharedConfig = localStorage.getItem('sharedGameConfig');
        if (sharedConfig) {
            const config = JSON.parse(sharedConfig);
            console.log('Loaded shared config:', config);
            
            document.getElementById('game-mode').value = config.gameMode || 'random';
            document.getElementById('specific-country').value = config.specificCountry || '';
            toggleCountrySelect();
            return;
        }
        
        // Try to load from config.json
        const response = await fetch('config.json?v=' + Date.now());
        if (response.ok) {
            const config = await response.json();
            console.log('Loaded current config:', config);
            
            // Set the form values
            document.getElementById('game-mode').value = config.gameMode || 'random';
            document.getElementById('specific-country').value = config.specificCountry || '';
            
            // Show/hide country select based on mode
            toggleCountrySelect();
            
            return;
        }
    } catch (error) {
        console.log('Could not load config.json, using localStorage');
    }
    
    // Fallback to localStorage
    const settings = localStorage.getItem('adminGameSettings');
    if (settings) {
        const parsed = JSON.parse(settings);
        console.log('Loaded settings from localStorage:', parsed);
        
        document.getElementById('game-mode').value = parsed.mode || 'random';
        document.getElementById('specific-country').value = parsed.specificCountry || '';
        toggleCountrySelect();
    }
}

// Authentication
function login() {
    const password = document.getElementById('admin-password').value;
    const errorElement = document.getElementById('login-error');
    
    if (password === ADMIN_PASSWORD) {
        document.getElementById('login-screen').style.display = 'none';
        document.getElementById('admin-panel').style.display = 'block';
        errorElement.style.display = 'none';
        
        // Load country dropdown
        populateCountryDropdown();
    } else {
        errorElement.textContent = 'Feil passord. Prøv igjen.';
        errorElement.style.display = 'block';
        document.getElementById('admin-password').value = '';
    }
}

function logout() {
    document.getElementById('login-screen').style.display = 'flex';
    document.getElementById('admin-panel').style.display = 'none';
    document.getElementById('admin-password').value = '';
    document.getElementById('login-error').style.display = 'none';
}

// Load countries data
async function loadCountriesData() {
    try {
        const response = await fetch('countries_data.json?v=' + Date.now());
        countriesData = await response.json();
        console.log('Land data lastet:', countriesData.length);
    } catch (error) {
        console.error('Feil ved lasting av land data:', error);
    }
}

// Populate country dropdown
function populateCountryDropdown() {
    const select = document.getElementById('specific-country');
    select.innerHTML = '<option value="">Velg land...</option>';
    
    countriesData.forEach(country => {
        const option = document.createElement('option');
        option.value = country.name;
        option.textContent = country.name;
        select.appendChild(option);
    });
    
    // Add event listeners for auto-save
    document.getElementById('game-mode').addEventListener('change', autoSaveSettings);
    document.getElementById('specific-country').addEventListener('change', autoSaveSettings);
}

// Toggle country select visibility
function toggleCountrySelect() {
    const gameMode = document.getElementById('game-mode').value;
    const countrySelectGroup = document.getElementById('country-select-group');
    
    if (gameMode === 'specific') {
        countrySelectGroup.style.display = 'block';
    } else {
        countrySelectGroup.style.display = 'none';
    }
    
    // Auto-save when settings change
    autoSaveSettings();
}

// Auto-save settings when they change
function autoSaveSettings() {
    const gameMode = document.getElementById('game-mode').value;
    const specificCountry = document.getElementById('specific-country').value;
    
    let config = {
        gameMode: gameMode,
        specificCountry: gameMode === 'specific' ? specificCountry : null,
        lastUpdated: new Date().toISOString()
    };
    
    // Store in localStorage for immediate use
    localStorage.setItem('adminGameSettings', JSON.stringify({
        mode: gameMode,
        specificCountry: gameMode === 'specific' ? specificCountry : null
    }));
    
    // Also store in global config for persistence
    localStorage.setItem('globalGameConfig', JSON.stringify(config));
    
    console.log('Auto-saved settings:', config);
}



// Apply game settings
function applyGameSettings() {
    const gameMode = document.getElementById('game-mode').value;
    const specificCountry = document.getElementById('specific-country').value;
    
    let config = {
        gameMode: gameMode,
        specificCountry: gameMode === 'specific' ? specificCountry : null,
        lastUpdated: new Date().toISOString()
    };
    
    // Store settings in localStorage for immediate use
    localStorage.setItem('adminGameSettings', JSON.stringify({
        mode: gameMode,
        specificCountry: gameMode === 'specific' ? specificCountry : null
    }));
    
    // Also store in a shared config key with higher priority
    localStorage.setItem('sharedGameConfig', JSON.stringify(config));
    
    // Store in a global config that persists across sessions
    localStorage.setItem('globalGameConfig', JSON.stringify(config));
    
    // Try to notify the main game if it's open
    try {
        // Send message to all open windows
        window.postMessage({
            type: 'CONFIG_UPDATED',
            config: config
        }, '*');
        
        // Also try to notify parent window if admin was opened from game
        if (window.opener) {
            window.opener.postMessage({
                type: 'CONFIG_UPDATED',
                config: config
            }, '*');
        }
    } catch (e) {
        console.log('Could not send message to game window:', e);
    }
    
    console.log('Config saved and broadcasted:', config);
    
    // Show success message
    showSuccessMessage('Innstillinger lagret! Spillet vil bruke de nye innstillingene umiddelbart.');
}

// Show success message
function showSuccessMessage(message) {
    // Remove existing message if any
    const existingMessage = document.getElementById('success-message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    // Create success message
    const messageDiv = document.createElement('div');
    messageDiv.id = 'success-message';
    messageDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #4CAF50;
        color: white;
        padding: 1rem 2rem;
        border-radius: 8px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
    `;
    
    messageDiv.innerHTML = `
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="font-size: 1.2rem;">✓</span>
            <span>${message}</span>
        </div>
    `;
    
    // Add CSS animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
    `;
    document.head.appendChild(style);
    
    document.body.appendChild(messageDiv);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
        if (messageDiv.parentNode) {
            messageDiv.remove();
        }
    }, 3000);
}

// Test current settings
function testCurrentSettings() {
    const adminSettings = localStorage.getItem('adminGameSettings');
    if (adminSettings) {
        const settings = JSON.parse(adminSettings);
        let message = `Nåværende innstillinger:\nModus: ${settings.mode}`;
        if (settings.mode === 'specific' && settings.specificCountry) {
            message += `\nSpesifikt land: ${settings.specificCountry}`;
        }
        alert(message);
    } else {
        alert('Ingen admin-innstillinger funnet.');
    }
}

// Force new game
function forceNewGame() {
    if (window.opener && window.opener.game) {
        window.opener.game.startNewGame().then(() => {
            alert('Nytt spill startet!');
        }).catch(error => {
            console.error('Error starting new game:', error);
            alert('Feil ved start av nytt spill. Sjekk console for detaljer.');
        });
    } else {
        // Try to communicate via localStorage and reload
        const adminSettings = localStorage.getItem('adminGameSettings');
        if (adminSettings) {
            // Trigger a custom event that the main game can listen to
            localStorage.setItem('forceNewGame', Date.now().toString());
            alert('Innstillinger sendt! Gå til spillet og trykk F5 for å starte nytt spill.');
        } else {
            alert('Ingen admin-innstillinger funnet. Sett innstillinger først.');
        }
    }
}

// Search for country
function searchCountry() {
    const searchTerm = document.getElementById('country-search').value.toLowerCase();
    const countryData = document.getElementById('country-data');
    
    if (!searchTerm) {
        alert('Skriv inn et landnavn for å søke.');
        return;
    }
    
    const country = countriesData.find(c => 
        c.name.toLowerCase().includes(searchTerm) || 
        c.original_name?.toLowerCase().includes(searchTerm)
    );
    
    if (country) {
        currentCountry = country;
        displayCountryData(country);
        countryData.style.display = 'block';
    } else {
        alert('Land ikke funnet. Prøv et annet navn.');
        countryData.style.display = 'none';
    }
}

// Display country data
function displayCountryData(country) {
    document.getElementById('selected-country-name').textContent = country.name;
    document.getElementById('country-iso3').textContent = country.iso3 || '-';
    document.getElementById('country-continent').textContent = country.continent || '-';
    document.getElementById('country-region').textContent = country.region || '-';
    document.getElementById('country-population').textContent = country.population ? country.population.toLocaleString() : '-';
    document.getElementById('country-population-year').textContent = country.population_year || '-';
    document.getElementById('country-image-file').textContent = country.imageFile || country.image_file || '-';
    document.getElementById('country-capital').textContent = country.capital || '-';
    
    // Format capital coordinates
    const capitalCoords = country.capital_coordinates;
    if (capitalCoords && capitalCoords.lat && capitalCoords.lon) {
        const lat = capitalCoords.lat >= 0 ? `${capitalCoords.lat.toFixed(4)}°N` : `${Math.abs(capitalCoords.lat).toFixed(4)}°S`;
        const lon = capitalCoords.lon >= 0 ? `${capitalCoords.lon.toFixed(4)}°E` : `${Math.abs(capitalCoords.lon).toFixed(4)}°W`;
        document.getElementById('country-capital-coordinates').textContent = `${lat}, ${lon}`;
    } else {
        document.getElementById('country-capital-coordinates').textContent = '-';
    }
    
    // Display current image
    const imageElement = document.getElementById('current-country-image');
    const imageFile = country.imageFile || country.image_file;
    if (imageFile) {
        imageElement.src = `country_images/${imageFile}?v=${Date.now()}`;
        imageElement.style.display = 'block';
    } else {
        imageElement.style.display = 'none';
    }
    
    // Populate edit form
    document.getElementById('edit-population').value = country.population || '';
    document.getElementById('edit-population-year').value = country.population_year || '';
}

// Upload new image
function uploadNewImage() {
    const fileInput = document.getElementById('new-country-image');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Velg en fil først.');
        return;
    }
    
    if (!currentCountry) {
        alert('Ingen land valgt.');
        return;
    }
    
    // In a real implementation, you would upload the file to the server
    // For now, we'll just show a preview
    const reader = new FileReader();
    reader.onload = function(e) {
        const imageElement = document.getElementById('current-country-image');
        imageElement.src = e.target.result;
        imageElement.style.display = 'block';
        
        alert('Bilde forhåndsvist. I en full implementasjon ville dette blitt lastet opp til serveren.');
    };
    reader.readAsDataURL(file);
}

// Save country data
function saveCountryData() {
    if (!currentCountry) {
        alert('Ingen land valgt.');
        return;
    }
    
    const population = document.getElementById('edit-population').value;
    const populationYear = document.getElementById('edit-population-year').value;
    
    // Update the country data
    currentCountry.population = population ? parseInt(population) : null;
    currentCountry.population_year = populationYear ? parseInt(populationYear) : null;
    
    // In a real implementation, you would save this to the server
    // For now, we'll just update the display
    displayCountryData(currentCountry);
    
    alert('Endringer lagret! (I en full implementasjon ville dette blitt lagret til serveren.)');
}

// Update system status
function updateSystemStatus() {
    if (countriesData.length === 0) return;
    
    const totalCountries = countriesData.length;
    const countriesWithImages = countriesData.filter(c => c.imageFile || c.image_file).length;
    const countriesWithFlags = countriesData.filter(c => c.flagFile).length;
    const countriesWithPopulation = countriesData.filter(c => c.population).length;
    const countriesWithCapital = countriesData.filter(c => c.capital).length;
    
    document.getElementById('total-countries').textContent = totalCountries;
    document.getElementById('countries-with-images').textContent = countriesWithImages;
    document.getElementById('countries-with-flags').textContent = countriesWithFlags;
    document.getElementById('countries-with-population').textContent = countriesWithPopulation;
    document.getElementById('countries-with-capital').textContent = countriesWithCapital;
}

// Enter key support for login
document.getElementById('admin-password').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        login();
    }
});

// Enter key support for search
document.getElementById('country-search').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        searchCountry();
    }
});

// Export all countries function
function exportAllCountries() {
    // Open export page in new tab
    window.open('export.html', '_blank');
}
