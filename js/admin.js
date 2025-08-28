// Admin Panel JavaScript
const ADMIN_PASSWORD = 'iunc67eus';
let countriesData = [];
let currentCountry = null;

// Initialize admin panel
document.addEventListener('DOMContentLoaded', function() {
    loadCountriesData();
    updateSystemStatus();
});

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
}

// Apply game settings
function applyGameSettings() {
    const gameMode = document.getElementById('game-mode').value;
    const specificCountry = document.getElementById('specific-country').value;
    
    let settings = {
        mode: gameMode,
        specificCountry: gameMode === 'specific' ? specificCountry : null
    };
    
    // Store settings in localStorage for the game to use
    localStorage.setItem('adminGameSettings', JSON.stringify(settings));
    
    alert('Innstillinger lagret! Spillet vil bruke disse innstillingene ved neste oppstart.');
}

// Test current settings
function testCurrentSettings() {
    const settings = localStorage.getItem('adminGameSettings');
    if (settings) {
        const parsedSettings = JSON.parse(settings);
        alert(`Nåværende innstillinger:\nModus: ${parsedSettings.mode}\nSpesifikt land: ${parsedSettings.specificCountry || 'Ikke satt'}`);
    } else {
        alert('Ingen admin-innstillinger satt. Spillet bruker standard tilfeldig modus.');
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
    
    document.getElementById('total-countries').textContent = totalCountries;
    document.getElementById('countries-with-images').textContent = countriesWithImages;
    document.getElementById('countries-with-flags').textContent = countriesWithFlags;
    document.getElementById('countries-with-population').textContent = countriesWithPopulation;
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
