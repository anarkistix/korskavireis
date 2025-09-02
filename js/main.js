// Korskavireis - Geografisk Gjettespill

class GeographyGame {
    constructor() {
        this.countries = [];
        this.currentCountry = null;
        this.attempts = 0;
        this.maxAttempts = 10;
        this.gamesPlayed = 0;
        this.isGameActive = false;
        this.hintUsed = false;
        this.populationHintUsed = false;
        this.capitalHintUsed = false;
        this.regionHintUsed = false;
        this.mountainHintUsed = false;
        this.currentLanguage = 'no'; // Default to Norwegian
        this.translations = {};
        this.bordersHintUsed = false;
        
        this.init();
    }

    async init() {
        console.log('Initialiserer geografisk gjettespill...');
        try {
            await this.loadTranslations();
            await this.loadCountries();
            
            // Last lagret språkvalg
            const savedLanguage = localStorage.getItem('selectedLanguage');
            if (savedLanguage) {
                this.currentLanguage = savedLanguage;
                // Oppdater aktiv knapp
                document.querySelectorAll('.lang-btn').forEach(btn => {
                    btn.classList.remove('active');
                });
                document.querySelector(`[data-lang="${savedLanguage}"]`)?.classList.add('active');
            }
            
            // Oppdater UI-tekster etter at oversettelser er lastet
            this.updateUIText();
            
            console.log('Land lastet, setter opp event listeners...');
            this.setupEventListeners();
            console.log('Event listeners satt opp, oppdaterer stats...');
            this.updateStats();
            console.log('Stats oppdatert, starter nytt spill...');
            await this.startNewGame();
            console.log('Nytt spill startet');
        } catch (error) {
            console.error('Feil i init:', error);
        }
        
        // Tving visning av alle lock-overlays etter init
        setTimeout(() => {
            this.forceShowAllLockOverlays();
        }, 100);
    }

    async loadTranslations() {
        try {
            const response = await fetch('translations.json');
            this.translations = await response.json();
            console.log('✅ Oversettelser lastet');
        } catch (error) {
            console.error('Feil ved lasting av oversettelser:', error);
        }
    }

    getText(key) {
        return this.translations[this.currentLanguage]?.[key] || key;
    }



    async updateLanguage(lang) {
        this.currentLanguage = lang;
        this.updateUIText();
        await this.updateCountryNames();
    }

    updateUIText() {
        try {
            // Oppdater UI-tekster
            // H1 er erstattet med logo, så vi hopper over den
            
            const subtitle = document.querySelector('.country-display h2');
            if (subtitle) subtitle.textContent = this.getText('subtitle');
            
            const loadingIndicator = document.getElementById('loading-indicator');
            if (loadingIndicator) loadingIndicator.textContent = this.getText('loading');
            
            const countryInput = document.getElementById('country-input');
            if (countryInput) countryInput.placeholder = this.getText('input_placeholder');
            
            const submitBtn = document.getElementById('submit-btn');
            if (submitBtn) submitBtn.textContent = this.getText('guess_button');
            
            const giveUpBtn = document.getElementById('give-up-btn');
            if (giveUpBtn) giveUpBtn.textContent = this.getText('give_up_button');
            
            const newGameBtn = document.getElementById('new-game-btn');
            if (newGameBtn) newGameBtn.textContent = this.getText('new_game_button');
            
            const googleMapsBtn = document.getElementById('google-maps-btn');
            if (googleMapsBtn) googleMapsBtn.textContent = this.getText('google_maps_button');
            
            const norliBtn = document.getElementById('norli-btn');
            if (norliBtn) norliBtn.textContent = this.getText('norli_button');
            
            // Oppdater hint-titler
            const hintBtn = document.querySelector('#hint-btn h4');
            if (hintBtn) hintBtn.textContent = this.getText('hint_1_title');
            
            const populationHintBtn = document.querySelector('#population-hint-btn h4');
            if (populationHintBtn) populationHintBtn.textContent = this.getText('hint_2_title');
            
            const capitalHintBtn = document.querySelector('#capital-hint-btn h4');
            if (capitalHintBtn) capitalHintBtn.textContent = this.getText('hint_3_title');
            
            const regionHintBtn = document.querySelector('#region-hint-btn h4');
            if (regionHintBtn) regionHintBtn.textContent = this.getText('hint_4_title');
            
            const mountainHintBtn = document.querySelector('#mountain-hint-btn h4');
            if (mountainHintBtn) mountainHintBtn.textContent = this.getText('hint_5_title');
            
            const bordersHintBtn = document.querySelector('#borders-hint-btn h4');
            if (bordersHintBtn) bordersHintBtn.textContent = this.getText('hint_6_title');
            
            // Oppdater footer
            const footerCopyright = document.querySelector('footer p:first-child');
            if (footerCopyright) footerCopyright.textContent = this.getText('footer_copyright');
            
            const footerBuiltBy = document.querySelector('footer p:last-child');
            if (footerBuiltBy) footerBuiltBy.textContent = this.getText('footer_built_by');
            
            console.log('✅ UI-tekster oppdatert');
        } catch (error) {
            console.error('Feil ved oppdatering av UI-tekster:', error);
        }
    }

    async updateCountryNames() {
        // Last land på nytt med riktig språk
        await this.loadCountries();
        
        // Oppdater autocomplete-liste hvis det er tekst i input-feltet
        const input = document.getElementById('country-input');
        if (input && input.value.length > 0) {
            this.showSuggestions(input.value);
        }
        
        console.log(`✅ Landnavn oppdatert til ${this.currentLanguage}`);
    }

    async switchLanguage(lang) {
        // Oppdater aktiv knapp
        document.querySelectorAll('.lang-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-lang="${lang}"]`).classList.add('active');
        
        // Oppdater språk
        this.currentLanguage = lang;
        
        // Oppdater UI og landnavn
        this.updateUIText();
        await this.updateCountryNames();
        
        // Oppdater autocomplete-liste hvis det er tekst i input-feltet
        const input = document.getElementById('country-input');
        if (input && input.value.length > 0) {
            this.showSuggestions(input.value);
        }
        
        // Lagre språkvalg i localStorage
        localStorage.setItem('selectedLanguage', lang);
        
        console.log(`🌍 Språk endret til: ${lang}`);
    }

    forceShowAllLockOverlays() {
        const lockOverlayIds = [
            'hint-lock-overlay',
            'population-lock-overlay', 
            'capital-lock-overlay',
            'region-lock-overlay',
            'mountain-lock-overlay',
            'borders-lock-overlay'
        ];

        lockOverlayIds.forEach(id => {
            const element = document.getElementById(id);
            if (element) {
                element.style.display = 'flex';
                console.log(`Force show: ${id} er nå synlig`);
            } else {
                console.error(`Force show: ${id} ikke funnet!`);
            }
        });
    }

    async loadCountries() {
        try {
            // Last riktig fil basert på språk
            const filename = this.currentLanguage === 'no' ? 'countries_data_no.json' : 'countries_data.json';
            console.log(`Laster land fra ${filename}...`);
            const response = await fetch(filename + '?v=' + Date.now());
            const data = await response.json();
            
            this.countries = data.map(country => {
                const center = country.geometry ? this.calculateCenter(country.geometry) : null;
                if (!center) {
                    console.warn(`Ingen center funnet for ${country.name}`);
                }
                

                
                return {
                    name: this.currentLanguage === 'no' ? country.name_no : country.name,
                    iso3: country.iso3,
                    continent: country.continent,
                    region: country.region,
                    imageFile: country.imageFile,
                    flagFile: country.flagFile,
                    population: country.population,
                    populationYear: country.population_year,
                    google_maps_url: country.google_maps_url,
                    capital: country.capital,
                    capital_coordinates: country.capital_coordinates,
                    highest_mountain: country.highest_mountain,
                    highest_elevation_meters: country.highest_elevation_meters,
                    highest_elevation_feet: country.highest_elevation_feet,
                    borders: country.borders,
                    borders_no: country.borders_no,
                    is_island: country.is_island,
                    center: center
                };
            }).filter(country => country.name && country.imageFile);

            console.log(`Lastet ${this.countries.length} land fra countries_data.json`);
            console.log(`Land med center: ${this.countries.filter(c => c.center).length}`);
            console.log(`Land uten center: ${this.countries.filter(c => !c.center).length}`);
            console.log(`Land med flagg: ${this.countries.filter(c => c.flagFile).length}`);
            console.log(`Land uten flagg: ${this.countries.filter(c => !c.flagFile).length}`);
            
        } catch (error) {
            console.error('Feil ved lasting av countries_data.json:', error);
            // Fallback til eksempel-data hvis datasettet ikke kan lastes
            this.countries = this.getSampleCountries();
        }
    }
    
    calculateCenter(geometry) {
        // Enkel beregning av sentrum basert på bounding box
        if (geometry.type === 'Polygon') {
            const coords = geometry.coordinates[0];
            let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
            
            coords.forEach(point => {
                minX = Math.min(minX, point[0]);
                minY = Math.min(minY, point[1]);
                maxX = Math.max(maxX, point[0]);
                maxY = Math.max(maxY, point[1]);
            });
            
            return {
                lon: (minX + maxX) / 2,
                lat: (minY + maxY) / 2
            };
        } else if (geometry.type === 'MultiPolygon') {
            // For MultiPolygon, beregn sentrum av alle polygoner
            let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
            
            geometry.coordinates.forEach(polygon => {
                const coords = polygon[0];
                coords.forEach(point => {
                    minX = Math.min(minX, point[0]);
                    minY = Math.min(minY, point[1]);
                    maxX = Math.max(maxX, point[0]);
                    maxY = Math.max(maxY, point[1]);
                });
            });
            
            return {
                lon: (minX + maxX) / 2,
                lat: (minY + maxY) / 2
            };
        }
        return null;
    }

    getSampleCountries() {
        return [
            {
                name: 'Norge',
                iso3: 'NOR',
                continent: 'Europe',
                region: 'Northern Europe',
                center: { lon: 8.468946, lat: 60.391263 },
                coordinates: [[[4.992078, 58.078884], [10.592105, 58.078884], [10.592105, 70.465054], [4.992078, 70.465054], [4.992078, 58.078884]]]
            },
            {
                name: 'Sverige',
                iso3: 'SWE',
                continent: 'Europe',
                region: 'Northern Europe',
                center: { lon: 18.643501, lat: 60.128161 },
                coordinates: [[[11.027369, 55.361737], [24.160908, 55.361737], [24.160908, 69.059771], [11.027369, 69.059771], [11.027369, 55.361737]]]
            },
            {
                name: 'Danmark',
                iso3: 'DNK',
                continent: 'Europe',
                region: 'Northern Europe',
                center: { lon: 9.501785, lat: 56.26392 },
                coordinates: [[[8.089977, 54.800014], [12.690006, 54.800014], [12.690006, 57.730017], [8.089977, 57.730017], [8.089977, 54.800014]]]
            }
        ];
    }

    setupEventListeners() {
        // Autocomplete funksjonalitet
        const countryInput = document.getElementById('country-input');
        const suggestionsList = document.getElementById('suggestions');

        countryInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            console.log('Input event triggered with query:', query, 'length:', query.length);
            this.showSuggestions(query);
        });

        countryInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                const selectedItem = suggestionsList.querySelector('.suggestion-item.selected');
                if (selectedItem) {
                    countryInput.value = selectedItem.textContent;
                    suggestionsList.innerHTML = '';
                    suggestionsList.style.display = 'none';
                }
                this.submitGuess();
            } else if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
                e.preventDefault();
                this.navigateSuggestions(e.key);
            } else if (e.key === 'Escape') {
                suggestionsList.innerHTML = '';
                suggestionsList.style.display = 'none';
            }
        });

        // Klikk på forslag
        suggestionsList.addEventListener('click', (e) => {
            if (e.target.classList.contains('suggestion-item')) {
                countryInput.value = e.target.textContent;
                suggestionsList.innerHTML = '';
                this.submitGuess();
            }
        });

        // Submit-knapp
        document.getElementById('submit-btn').addEventListener('click', () => {
            console.log('Submit-knapp klikket');
            this.submitGuess();
        });

        // Gi opp-knapp
        document.getElementById('give-up-btn').addEventListener('click', () => {
            console.log('Gi opp-knapp klikket');
            this.giveUp();
        });

        // Google Maps-knapp
        document.getElementById('google-maps-btn').addEventListener('click', () => {
            console.log('Google Maps-knapp klikket');
            this.openGoogleMaps();
        });

        // Norli-knapp
        document.getElementById('norli-btn').addEventListener('click', () => {
            console.log('Norli-knapp klikket');
            this.openNorliBooks();
        });

        // Hint-knapp
        const hintBtn = document.getElementById('hint-btn');
        if (hintBtn) {
            hintBtn.addEventListener('click', () => {
                this.showHint();
            });
        }

        // Lock-overlays for alle hint
        const lockOverlays = [
            { id: 'hint-lock-overlay', attempts: 1 },
            { id: 'population-lock-overlay', attempts: 2 },
            { id: 'capital-lock-overlay', attempts: 3 },
            { id: 'region-lock-overlay', attempts: 4 },
            { id: 'mountain-lock-overlay', attempts: 5 },
            { id: 'borders-lock-overlay', attempts: 6 }
        ];

        lockOverlays.forEach(overlay => {
            const element = document.getElementById(overlay.id);
            if (element) {
                // Sikre at lock-overlay er synlig ved start
                element.style.display = 'flex';
                element.addEventListener('click', (e) => {
                    e.stopPropagation(); // Hindre at klikket går til knappen
                    this.showLockMessage(overlay.attempts);
                });
                console.log(`Lock overlay ${overlay.id} initialisert`);
            } else {
                console.error(`Lock overlay ${overlay.id} ikke funnet!`);
            }
        });

        // Språkvelger event listeners
        const langButtons = document.querySelectorAll('.lang-btn');
        langButtons.forEach(btn => {
            btn.addEventListener('click', async () => {
                const lang = btn.getAttribute('data-lang');
                await this.switchLanguage(lang);
            });
        });

        // Befolkningshint-knapp
        const populationHintBtn = document.getElementById('population-hint-btn');
        if (populationHintBtn) {
            populationHintBtn.addEventListener('click', () => {
                this.showPopulationHint();
            });
        }

        // Hovedstadshint-knapp
                        const capitalHintBtn = document.getElementById('capital-hint-btn');
                if (capitalHintBtn) {
                    capitalHintBtn.addEventListener('click', () => {
                        this.showCapitalHint();
                    });
                }
                
                const regionHintBtn = document.getElementById('region-hint-btn');
                if (regionHintBtn) {
                    regionHintBtn.addEventListener('click', () => {
                        this.showRegionHint();
                    });
                }
                
                const mountainHintBtn = document.getElementById('mountain-hint-btn');
                if (mountainHintBtn) {
                    mountainHintBtn.addEventListener('click', () => {
                        this.showMountainHint();
                    });
                }
                
                const bordersHintBtn = document.getElementById('borders-hint-btn');
                if (bordersHintBtn) {
                    bordersHintBtn.addEventListener('click', () => {
                        this.showBordersHint();
                    });
                }

        // Nytt spill-knapp
        document.getElementById('new-game-btn').addEventListener('click', () => {
            this.startNewGame().catch(error => {
                console.error('Error starting new game:', error);
            });
        });

        // Klikk utenfor for å lukke forslag
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.input-container')) {
                suggestionsList.innerHTML = '';
            }
        });
        
        // Listen for config updates from admin panel
        window.addEventListener('message', (event) => {
            if (event.data && event.data.type === 'CONFIG_UPDATED') {
                console.log('Config update received from admin:', event.data.config);
                // Store the new config
                localStorage.setItem('sharedGameConfig', JSON.stringify(event.data.config));
                // Show notification
                this.showConfigUpdateNotification();
                // Optionally restart game with new settings
                if (this.isGameActive) {
                    setTimeout(() => {
                        this.startNewGame().catch(error => {
                            console.error('Error restarting game with new config:', error);
                        });
                    }, 1000);
                }
            }
        });
    }
    
    // Show config update notification
    showConfigUpdateNotification() {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #2196F3;
            color: white;
            padding: 1rem 2rem;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            z-index: 1000;
            animation: slideIn 0.3s ease-out;
        `;
        
        notification.innerHTML = `
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.2rem;">⚙️</span>
                <span>Nye innstillinger mottatt fra admin!</span>
            </div>
        `;
        
        // Add CSS animation if not already present
        if (!document.querySelector('#config-notification-style')) {
            const style = document.createElement('style');
            style.id = 'config-notification-style';
            style.textContent = `
                @keyframes slideIn {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
            `;
            document.head.appendChild(style);
        }
        
        document.body.appendChild(notification);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 3000);
    }

    showSuggestions(query) {
        const suggestionsList = document.getElementById('suggestions');
        suggestionsList.innerHTML = '';

        console.log('showSuggestions kalt med query:', query);
        console.log('Antall land tilgjengelig:', this.countries.length);

        if (query.length < 1) {
            console.log('Query for kort, returnerer');
            return;
        }

        const matches = this.countries
            .filter(country => 
                country.name.toLowerCase().includes(query) ||
                country.iso3.toLowerCase().includes(query)
            )
            .sort((a, b) => a.name.localeCompare(b.name))
            .slice(0, 10);

        console.log('Funn:', matches.length, 'land som matcher:', query);
        console.log('Funn:', matches.map(c => c.name));

        matches.forEach((country, index) => {
            const item = document.createElement('div');
            item.className = 'suggestion-item';
            item.textContent = country.name;
            
            // Markér første element som matcher query
            if (index === 0 && country.name.toLowerCase().startsWith(query)) {
                item.classList.add('first-match');
            }
            
            suggestionsList.appendChild(item);
        });

        if (matches.length > 0) {
            suggestionsList.style.display = 'block';
            console.log('Viser suggestions med', matches.length, 'elementer');
            
            // Smart scroll til riktig posisjon basert på query
            if (query.length === 1) {
                // For én bokstav, finn første land i hele listen som starter med den bokstaven
                const firstCountryStartingWith = this.countries.find(country => 
                    country.name.toLowerCase().startsWith(query)
                );
                
                if (firstCountryStartingWith) {
                    // Finn elementet i suggestions som matcher dette landet
                    const targetElement = Array.from(suggestionsList.querySelectorAll('.suggestion-item'))
                        .find(item => item.textContent === firstCountryStartingWith.name);
                    
                    if (targetElement) {
                        // Scroll til toppen av suggestions-lista for å vise starten av denne bokstaven
                        suggestionsList.scrollTop = 0;
                        // Deretter scroll til elementet med 'nearest' for å vise det i kontekst
                        targetElement.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
                    } else {
                        // Hvis landet ikke er i suggestions, scroll til toppen
                        suggestionsList.scrollTop = 0;
                    }
                } else {
                    // Ingen land starter med denne bokstaven, scroll til toppen
                    suggestionsList.scrollTop = 0;
                }
            } else {
                // For lengre queries, scroll til første element som starter med query
                const matchingElement = Array.from(suggestionsList.querySelectorAll('.suggestion-item'))
                    .find(item => item.textContent.toLowerCase().startsWith(query));
                if (matchingElement) {
                    matchingElement.scrollIntoView({ block: 'start', behavior: 'smooth' });
                }
            }
        } else if (query.length === 1) {
            // Vis tom suggestions-liste for én bokstav, men med smart scroll
            suggestionsList.style.display = 'block';
            console.log('Viser tom suggestions-liste for bokstav:', query);
            
            // Finn første land i hele listen som starter med denne bokstaven
            const firstCountryStartingWith = this.countries.find(country => 
                country.name.toLowerCase().startsWith(query)
            );
            
            if (firstCountryStartingWith) {
                // Scroll til toppen for å vise starten av denne bokstaven
                suggestionsList.scrollTop = 0;
            } else {
                // Ingen land starter med denne bokstaven, scroll til toppen
                suggestionsList.scrollTop = 0;
            }
        } else {
            suggestionsList.style.display = 'none';
            console.log('Skjuler suggestions - ingen treff');
        }
    }

    navigateSuggestions(direction) {
        const suggestionsList = document.getElementById('suggestions');
        const items = suggestionsList.querySelectorAll('.suggestion-item');
        const currentSelected = suggestionsList.querySelector('.suggestion-item.selected');
        
        if (items.length === 0) return;
        
        let nextIndex = 0;
        
        if (currentSelected) {
            const currentIndex = Array.from(items).indexOf(currentSelected);
            if (direction === 'ArrowDown') {
                nextIndex = (currentIndex + 1) % items.length;
            } else {
                nextIndex = currentIndex === 0 ? items.length - 1 : currentIndex - 1;
            }
            currentSelected.classList.remove('selected');
        }
        
        items[nextIndex].classList.add('selected');
        items[nextIndex].scrollIntoView({ block: 'nearest' });
    }

    async startNewGame() {
        this.attempts = 0;
        this.isGameActive = true;
        this.gamesPlayed++;
        this.hintUsed = false;
        this.populationHintUsed = false;
        this.capitalHintUsed = false;
        this.regionHintUsed = false;
        this.mountainHintUsed = false;
        this.bordersHintUsed = false;
        
        // Sjekk admin-innstillinger
        const adminSettings = await this.getAdminSettings();
        console.log('Admin-innstillinger ved start av nytt spill:', adminSettings);
        
        if (adminSettings && adminSettings.mode === 'specific' && adminSettings.specificCountry) {
            // Bruk spesifikt land fra admin
            const specificCountry = this.countries.find(c => c.name === adminSettings.specificCountry);
            if (specificCountry) {
                this.currentCountry = specificCountry;
                console.log(`Admin: Spill startet med spesifikt land: ${this.currentCountry.name}`);
            } else {
                console.log(`Admin: Spesifikt land "${adminSettings.specificCountry}" ikke funnet, bruker tilfeldig`);
                console.log('Tilgjengelige land:', this.countries.map(c => c.name).slice(0, 10));
                this.selectRandomCountry();
            }
        } else {
            // Bruk tilfeldig land (standard)
            console.log('Admin: Ingen spesifikt land satt, bruker tilfeldig');
            this.selectRandomCountry();
        }
        
        this.updateStats();
        this.resetUI();
        this.displayCountryImage();
    }

    selectRandomCountry() {
        if (this.countries.length > 0) {
            const randomIndex = Math.floor(Math.random() * this.countries.length);
            this.currentCountry = this.countries[randomIndex];
            console.log(`Nytt spill startet med: ${this.currentCountry.name}`);
            console.log('currentCountry google_maps_url:', this.currentCountry.google_maps_url);
            console.log('currentCountry keys:', Object.keys(this.currentCountry));
        } else {
            // Fallback hvis ingen land er lastet
            console.log('Ingen land lastet, bruker fallback');
            this.currentCountry = {
                name: 'Norge',
                iso3: 'NOR',
                continent: 'Europe',
                region: 'Northern Europe',
                center: { lon: 8.468946, lat: 60.391263 },
                imageFile: 'norway.png'
            };
        }
    }

    async getAdminSettings() {
        try {
            // First check global config (highest priority - persists across sessions)
            const globalConfig = localStorage.getItem('globalGameConfig');
            if (globalConfig) {
                const config = JSON.parse(globalConfig);
                console.log('Config loaded from global storage:', config);
                return {
                    mode: config.gameMode,
                    specificCountry: config.specificCountry
                };
            }
            
            // Then check shared config (for current session)
            const sharedConfig = localStorage.getItem('sharedGameConfig');
            if (sharedConfig) {
                const config = JSON.parse(sharedConfig);
                console.log('Config loaded from shared storage:', config);
                return {
                    mode: config.gameMode,
                    specificCountry: config.specificCountry
                };
            }
            
            // Then try to load from config.json (server-side config)
            try {
                console.log('Attempting to load config.json...');
                const response = await fetch('config.json?v=' + Date.now());
                console.log('Config.json response status:', response.status);
                if (response.ok) {
                    const config = await response.json();
                    console.log('Config loaded from file:', config);
                    console.log('Config gameMode:', config.gameMode);
                    console.log('Config specificCountry:', config.specificCountry);
                    
                    // Update shared config in localStorage for consistency
                    localStorage.setItem('sharedGameConfig', JSON.stringify(config));
                    
                    return {
                        mode: config.gameMode,
                        specificCountry: config.specificCountry
                    };
                } else {
                    console.log('Config.json response not ok, status:', response.status);
                }
            } catch (error) {
                console.log('Could not load config.json, error:', error);
                console.log('Using localStorage fallback');
            }
            
            // Final fallback to localStorage
            const settings = localStorage.getItem('adminGameSettings');
            console.log('localStorage settings:', settings);
            return settings ? JSON.parse(settings) : null;
        } catch (error) {
            console.error('Feil ved henting av admin-innstillinger:', error);
            return null;
        }
    }

    displayCountryOutline() {
        const canvas = document.getElementById('country-canvas');
        const ctx = canvas.getContext('2d');
        
        // Tøm canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Sett opp tegning - fyllt med svart farge
        ctx.strokeStyle = '#000';
        ctx.lineWidth = 1;
        ctx.fillStyle = '#000';
        
        console.log('Tegner geometri type:', this.currentCountry.geometry.type);
        console.log('Geometri koordinater:', this.currentCountry.geometry.coordinates);
        
        // Debug: Vis koordinatene først
        console.log('=== DEBUG INFO ===');
        console.log('Land:', this.currentCountry.name);
        console.log('Geometri type:', this.currentCountry.geometry.type);
        console.log('Antall koordinat-arrayer:', this.currentCountry.geometry.coordinates.length);
        
        if (this.currentCountry.geometry.type === 'Polygon') {
            console.log('Første koordinat-array lengde:', this.currentCountry.geometry.coordinates[0].length);
            console.log('Første 5 koordinater:', this.currentCountry.geometry.coordinates[0].slice(0, 5));
        } else if (this.currentCountry.geometry.type === 'MultiPolygon') {
            this.currentCountry.geometry.coordinates.forEach((polygon, index) => {
                console.log(`Polygon ${index} lengde:`, polygon[0].length);
                console.log(`Polygon ${index} første 5 koordinater:`, polygon[0].slice(0, 5));
            });
        }
        
        // Vis landbildet
        this.displayCountryImage();
        
        console.log('Viser landomriss for:', this.currentCountry.name);
    }
    
    displayCountryImage() {
        const countryImage = document.getElementById('country-image');
        const loadingIndicator = document.getElementById('loading-indicator');
        
        console.log('displayCountryImage kalt');
        console.log('currentCountry:', this.currentCountry);
        
        if (this.currentCountry && this.currentCountry.imageFile) {
            console.log('Viser bilde for:', this.currentCountry.name);
            console.log('Bildefil:', this.currentCountry.imageFile);
            
            // Skjul loading-indikator og vis bildet
            loadingIndicator.style.display = 'none';
            countryImage.style.display = 'block';
            
            const imagePath = `country_images/${this.currentCountry.imageFile}`;
            console.log('Bildesti:', imagePath);
            
            countryImage.src = imagePath;
            countryImage.alt = `Landomriss av ${this.currentCountry.name}`;
            
            // Error handler for bilde
            countryImage.onerror = () => {
                console.error('Feil ved lasting av bilde:', imagePath);
                this.showMessage('Feil ved lasting av landets bilde', 'error');
            };
            
            countryImage.onload = () => {
                console.log('Bilde lastet vellykket:', imagePath);
            };
            
            // Vis hint-knappen når landet vises
            document.getElementById('hint-container').style.display = 'block';
        } else {
            console.log('Ingen currentCountry eller imageFile');
        }
    }
    



    


    submitGuess() {
        console.log('submitGuess kalt');
        console.log('isGameActive:', this.isGameActive);
        
        if (!this.isGameActive) {
            console.log('Spill ikke aktiv, returnerer');
            return;
        }

        const countryInput = document.getElementById('country-input');
        const guessedCountryName = countryInput.value.trim();
        
        console.log('Gjettet landnavn:', guessedCountryName);
        
        if (!guessedCountryName) {
            console.log('Tomt landnavn, viser feilmelding');
            this.showMessage('Vennligst skriv inn et landnavn!', 'error');
            return;
        }

        // Finn landet som ble gjettet
        const guessedCountry = this.countries.find(country => 
            country.name.toLowerCase() === guessedCountryName.toLowerCase() ||
            country.iso3.toLowerCase() === guessedCountryName.toLowerCase()
        );

        if (!guessedCountry) {
            this.showMessage('Landet ble ikke funnet. Prøv et annet navn!', 'error');
            return;
        }

        this.attempts++;

        // Sjekk og lås opp hint basert på antall forsøk
        this.checkAndUnlockHints();

        if (guessedCountry.name === this.currentCountry.name) {
            // Riktig gjetting
            this.addFeedbackItem(guessedCountry, true);
            this.showMessage(`${this.getText('correct_guess')} ${this.currentCountry.name}.`, 'success');
            this.endGame(true);
        } else {
            // Feil gjetting
            if (!this.currentCountry.center || !guessedCountry.center) {
                // Fallback hvis center ikke er tilgjengelig
                this.addFeedbackItem(guessedCountry, false, null, null);
                this.showMessage(`Feil! Prøv igjen.`, 'info');
            } else {
                const distance = this.calculateDistance(
                    this.currentCountry.center.lat, this.currentCountry.center.lon,
                    guessedCountry.center.lat, guessedCountry.center.lon
                );
                
                            const direction = this.getDirection(
                guessedCountry.center.lat, guessedCountry.center.lon,
                this.currentCountry.center.lat, this.currentCountry.center.lon
            );

                this.addFeedbackItem(guessedCountry, false, distance, direction);
            }

            if (this.attempts >= this.maxAttempts) {
                this.showMessage(`${this.getText('gave_up')} ${this.currentCountry.name}`, 'error');
                this.endGame(false);
            }
        }

        this.updateStats();
        countryInput.value = '';
        document.getElementById('suggestions').innerHTML = '';
    }

    addFeedbackItem(guessedCountry, isCorrect, distance = null, direction = null) {
        const feedbackContainer = document.getElementById('feedback-container');
        const feedbackItem = document.createElement('div');
        feedbackItem.className = `feedback-item ${isCorrect ? 'feedback-correct' : ''}`;
        
        const numberDiv = document.createElement('div');
        numberDiv.className = 'feedback-number';
        numberDiv.textContent = this.attempts;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'feedback-content';
        
                        const detailsDiv = document.createElement('div');
                detailsDiv.className = 'feedback-details';
                
                if (isCorrect) {
                    detailsDiv.innerHTML = `<span style="color: #28a745; font-weight: 600;"><strong>${guessedCountry.name}</strong> 🎉🎉🎉 ${this.getText('feedback_correct')} 🎉🎉🎉</span>`;
                } else {
                    if (distance !== null && direction !== null) {
                        detailsDiv.innerHTML = `<span style="color: #666;"><strong>${guessedCountry.name}</strong>. ${this.getText('feedback_distance')} <strong>${Math.round(distance)} ${this.getText('feedback_km')} ${direction}</strong> ${this.getText('feedback_for')} <strong>${guessedCountry.name}</strong></span>`;
                    } else {
                        detailsDiv.innerHTML = `<span style="color: #666;">${this.getText('feedback_wrong')}</span>`;
                    }
                }
                

                
                contentDiv.appendChild(detailsDiv);
        
        feedbackItem.appendChild(numberDiv);
        feedbackItem.appendChild(contentDiv);
        
        // Sett siste gjett øverst i listen
        if (feedbackContainer.firstChild) {
            feedbackContainer.insertBefore(feedbackItem, feedbackContainer.firstChild);
        } else {
            feedbackContainer.appendChild(feedbackItem);
        }
        
        // Scroll til toppen for å vise siste gjett
        feedbackContainer.scrollTop = 0;
        
        // Scroll hele vinduet slik at kartets topp er øverst i skjermen
        this.scrollToMapTop();
    }

    calculateDistance(lat1, lon1, lat2, lon2) {
        const R = 6371; // Jordens radius i km
        const dLat = this.toRadians(lat2 - lat1);
        const dLon = this.toRadians(lon2 - lon1);
        const a = 
            Math.sin(dLat/2) * Math.sin(dLat/2) +
            Math.cos(this.toRadians(lat1)) * Math.cos(this.toRadians(lat2)) * 
            Math.sin(dLon/2) * Math.sin(dLon/2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        return R * c;
    }

    toRadians(degrees) {
        return degrees * (Math.PI/180);
    }

    getDirection(lat1, lon1, lat2, lon2) {
        const dLat = lat2 - lat1;
        const dLon = lon2 - lon1;
        
        // Beregn vinkel for å bestemme hovedretning
        // Bruk atan2(dLon, dLat) for å få riktig vinkel
        let angle = Math.atan2(dLon, dLat) * 180 / Math.PI;
        
        // Normaliser vinkelen til 0-360 grader
        if (angle < 0) {
            angle += 360;
        }
        
        // Debug logging
        console.log(`Retningsberegning: dLat=${dLat.toFixed(2)}, dLon=${dLon.toFixed(2)}, angle=${angle.toFixed(2)}`);
        
        // Definer 8 hovedretninger med presise vinkler
        if (angle >= 337.5 || angle < 22.5) {
            console.log(`Vinkel ${angle.toFixed(2)}° gir retning: nord`);
            return this.getText('direction_north');
        } else if (angle >= 22.5 && angle < 67.5) {
            console.log(`Vinkel ${angle.toFixed(2)}° gir retning: nordøst`);
            return this.getText('direction_northeast');
        } else if (angle >= 67.5 && angle < 112.5) {
            console.log(`Vinkel ${angle.toFixed(2)}° gir retning: øst`);
            return this.getText('direction_east');
        } else if (angle >= 112.5 && angle < 157.5) {
            console.log(`Vinkel ${angle.toFixed(2)}° gir retning: sørøst`);
            return this.getText('direction_southeast');
        } else if (angle >= 157.5 && angle < 202.5) {
            console.log(`Vinkel ${angle.toFixed(2)}° gir retning: sør`);
            return this.getText('direction_south');
        } else if (angle >= 202.5 && angle < 247.5) {
            console.log(`Vinkel ${angle.toFixed(2)}° gir retning: sørvest`);
            return this.getText('direction_southwest');
        } else if (angle >= 247.5 && angle < 292.5) {
            console.log(`Vinkel ${angle.toFixed(2)}° gir retning: vest`);
            return this.getText('direction_west');
        } else if (angle >= 292.5 && angle < 337.5) {
            console.log(`Vinkel ${angle.toFixed(2)}° gir retning: nordvest`);
            return this.getText('direction_northwest');
        }
        
        // Dette burde aldri skje, men for sikkerhets skyld
        console.log(`Vinkel ${angle.toFixed(2)}° gir fallback: nord`);
        return this.getText('direction_north');
    }

    endGame(won) {
        console.log('🎮 endGame kalt med won:', won);
        this.isGameActive = false;
        
        if (won) {
            console.log('🏆 Spillet vunnet - viser landnavn og hint');
            // Vis landnavn og alle hint når spillet vinnes
            const revealBox = document.getElementById('country-reveal-box');
            const revealedCountryName = document.getElementById('revealed-country-name');
            const countryName = this.currentLanguage === 'no' ? 
                this.currentCountry.name_no || this.currentCountry.name : 
                this.currentCountry.name;
            
            revealedCountryName.textContent = countryName;
            revealBox.style.display = 'block';
            
            // Vis alle hint automatisk
            console.log('🔍 Kaller revealAllHints()...');
            this.revealAllHints();
        }
        
        document.getElementById('new-game-btn').style.display = 'block';
        document.getElementById('submit-btn').style.display = 'none';
        document.getElementById('give-up-btn').style.display = 'none';
        document.getElementById('google-maps-btn').style.display = 'block';
        this.setNorliButtonLabel();
        document.getElementById('norli-btn').style.display = 'block';
    }

    resetUI() {
        document.getElementById('country-input').value = '';
        document.getElementById('country-input').disabled = false;
        document.getElementById('suggestions').innerHTML = '';
        document.getElementById('new-game-btn').style.display = 'none';
        document.getElementById('submit-btn').style.display = 'block';
        document.getElementById('give-up-btn').style.display = 'block';
        document.getElementById('google-maps-btn').style.display = 'none';
        document.getElementById('norli-btn').style.display = 'none';
        this.clearMessages();
        
        // Tøm feedback-container
        document.getElementById('feedback-container').innerHTML = '';
        
        // Skjul bildet og vis loading-indikator
        document.getElementById('country-image').style.display = 'none';
        document.getElementById('loading-indicator').style.display = 'block';
        
        // Reset og lås alle hint igjen
        this.resetAllHints();
        
        // Reset hint-flag
        document.getElementById('hint-flag').style.display = 'none';

        // Reset befolkningshint-knapp
        const populationHintBtn = document.getElementById('population-hint-btn');
        if (populationHintBtn) {
            populationHintBtn.querySelector('h4').textContent = this.getText('hint_2_title');
            populationHintBtn.disabled = false;
            populationHintBtn.style.display = 'inline-block'; // Vis knappen igjen
        }
        
        // Reset befolkningshint
        document.getElementById('population-hint').style.display = 'none';

        // Reset hovedstadshint-knapp
        const capitalHintBtn = document.getElementById('capital-hint-btn');
        if (capitalHintBtn) {
            capitalHintBtn.querySelector('h4').textContent = this.getText('hint_3_title');
            capitalHintBtn.disabled = false;
            capitalHintBtn.style.display = 'inline-block'; // Vis knappen igjen
        }
        
        // Reset hovedstadshint
        document.getElementById('capital-hint').style.display = 'none';

        // Reset regionhint-knapp
        const regionHintBtn = document.getElementById('region-hint-btn');
        if (regionHintBtn) {
            regionHintBtn.querySelector('h4').textContent = this.getText('hint_4_title');
            regionHintBtn.disabled = false;
            regionHintBtn.style.display = 'inline-block'; // Vis knappen igjen
        }
        
        // Reset regionhint
        document.getElementById('region-hint').style.display = 'none';

        // Reset mountainhint-knapp
        const mountainHintBtn = document.getElementById('mountain-hint-btn');
        if (mountainHintBtn) {
            mountainHintBtn.querySelector('h4').textContent = this.getText('hint_5_title');
            mountainHintBtn.disabled = false;
            mountainHintBtn.style.display = 'inline-block'; // Vis knappen igjen
        }
        
        // Reset mountainhint
        document.getElementById('mountain-hint').style.display = 'none';

        // Reset bordershint-knapp
        const bordersHintBtn = document.getElementById('borders-hint-btn');
        if (bordersHintBtn) {
            bordersHintBtn.querySelector('h4').textContent = this.getText('hint_6_title');
            bordersHintBtn.disabled = false;
            bordersHintBtn.style.display = 'inline-block'; // Vis knappen igjen
        }
        
        // Reset bordershint
        document.getElementById('borders-hint').style.display = 'none';
        
        // Skjul landnavn reveal-boks
        document.getElementById('country-reveal-box').style.display = 'none';
    }

    updateStats() {
    }

    showMessage(message, type = 'info') {
        const messageContainer = document.getElementById('message-container');
        const messageElement = document.createElement('div');
        messageElement.className = `message ${type}`;
        messageElement.textContent = message;
        
        messageContainer.appendChild(messageElement);
        
        // Fjern meldingen etter 5 sekunder
        setTimeout(() => {
            if (messageElement.parentNode) {
                messageElement.parentNode.removeChild(messageElement);
            }
        }, 5000);
    }

    clearMessages() {
        const messageContainer = document.getElementById('message-container');
        messageContainer.innerHTML = '';
    }

    showHint() {
        if (!this.currentCountry || this.hintUsed || this.attempts < 1) {
            return;
        }

        const hintFlag = document.getElementById('hint-flag');
        const hintFlagImg = document.getElementById('hint-flag-img');
        const hintBtn = document.getElementById('hint-btn');
        const lockOverlay = document.getElementById('hint-lock-overlay');

        if (this.currentCountry.flagFile) {
            hintFlagImg.src = `flags/${this.currentCountry.flagFile.replace('flags/', '')}?v=${Date.now()}`;
            this.placeHintContentNearButton(hintFlag, hintBtn);
            // Skjul lock-overlay når hint åpnes
            if (lockOverlay) {
                lockOverlay.style.display = 'none';
            }
            // Ikke skjul knappen - la den være synlig
            this.hintUsed = true;
        } else {
            // Hvis ingen flagg er tilgjengelig, vis en melding
            hintBtn.querySelector('h4').textContent = 'Ingen flagg tilgjengelig';
            hintBtn.disabled = true;
            this.hintUsed = true;
        }
    }

    showLockMessage(requiredAttempts) {
        const message = document.createElement('div');
        message.className = 'lock-message';
        const key = `lock_message_${requiredAttempts}`;
        message.textContent = this.getText(key);
        document.body.appendChild(message);
        
        // Fjern meldingen etter animasjonen
        setTimeout(() => {
            if (message.parentNode) {
                message.parentNode.removeChild(message);
            }
        }, 2000);
    }

    checkAndUnlockHints() {
        // Hint 1: Låst opp etter 1 forsøk
        if (this.attempts >= 1) {
            this.unlockHint(1);
        }
        
        // Hint 2: Låst opp etter 2 forsøk
        if (this.attempts >= 2) {
            this.unlockHint(2);
        }
        
        // Hint 3: Låst opp etter 3 forsøk
        if (this.attempts >= 3) {
            this.unlockHint(3);
        }
        
        // Hint 4: Låst opp etter 4 forsøk
        if (this.attempts >= 4) {
            this.unlockHint(4);
        }
        
        // Hint 5: Låst opp etter 5 forsøk
        if (this.attempts >= 5) {
            this.unlockHint(5);
        }
        
        // Hint 6: Låst opp etter 6 forsøk
        if (this.attempts >= 6) {
            this.unlockHint(6);
        }
    }

    unlockHint(hintNumber) {
        const hintConfigs = {
            1: { btnId: 'hint-btn', overlayId: 'hint-lock-overlay' },
            2: { btnId: 'population-hint-btn', overlayId: 'population-lock-overlay' },
            3: { btnId: 'capital-hint-btn', overlayId: 'capital-lock-overlay' },
            4: { btnId: 'region-hint-btn', overlayId: 'region-lock-overlay' },
            5: { btnId: 'mountain-hint-btn', overlayId: 'mountain-lock-overlay' },
            6: { btnId: 'borders-hint-btn', overlayId: 'borders-lock-overlay' }
        };

        const config = hintConfigs[hintNumber];
        if (!config) return;

        const hintBtn = document.getElementById(config.btnId);
        const lockOverlay = document.getElementById(config.overlayId);
        
        if (hintBtn) {
            hintBtn.classList.remove('locked');
        }
        if (lockOverlay) {
            lockOverlay.style.display = 'none';
        }
    }

    unlockHint1() {
        this.unlockHint(1);
    }

    resetAllHints() {
        const hintConfigs = [
            { btnId: 'hint-btn', overlayId: 'hint-lock-overlay', textKey: 'hint_1_title', contentId: 'hint-flag' },
            { btnId: 'population-hint-btn', overlayId: 'population-lock-overlay', textKey: 'hint_2_title', contentId: 'population-hint' },
            { btnId: 'capital-hint-btn', overlayId: 'capital-lock-overlay', textKey: 'hint_3_title', contentId: 'capital-hint' },
            { btnId: 'region-hint-btn', overlayId: 'region-lock-overlay', textKey: 'hint_4_title', contentId: 'region-hint' },
            { btnId: 'mountain-hint-btn', overlayId: 'mountain-lock-overlay', textKey: 'hint_5_title', contentId: 'mountain-hint' },
            { btnId: 'borders-hint-btn', overlayId: 'borders-lock-overlay', textKey: 'hint_6_title', contentId: 'borders-hint' }
        ];

        hintConfigs.forEach(config => {
            const hintBtn = document.getElementById(config.btnId);
            const lockOverlay = document.getElementById(config.overlayId);
            const hintContent = document.getElementById(config.contentId);
            
            if (hintBtn) {
                hintBtn.querySelector('h4').textContent = this.getText(config.textKey);
                hintBtn.disabled = false;
                hintBtn.style.display = 'inline-block';
                hintBtn.classList.add('locked');
            }
            
            if (lockOverlay) {
                lockOverlay.style.display = 'flex';
            }
            
            if (hintContent) {
                hintContent.style.display = 'none';
            }
        });
    }

    // Sørger for at hint-innholdet alltid åpnes inne i samme område som hintknappene
    placeHintContentNearButton(contentElement, buttonElement) {
        try {
            const hintsRow = document.querySelector('.hints-row');
            if (!hintsRow || !contentElement || !buttonElement) return;
            // Plasser hintet rett før knappen og skjul knappen,
            // slik at hintet tar over plassen til knappen i raden
            if (buttonElement.parentElement === hintsRow) {
                hintsRow.insertBefore(contentElement, buttonElement);
                buttonElement.style.display = 'none';
            } else if (contentElement.parentElement !== hintsRow) {
                hintsRow.appendChild(contentElement);
            }
            contentElement.style.display = 'flex';
        } catch (error) {
            console.error('Feil ved plassering av hint-innhold:', error);
        }
    }

    // Scroller slik at toppen av kart-området legger seg øverst i viewport
    scrollToMapTop() {
        try {
            const target = document.querySelector('.canvas-container') || document.querySelector('.game-area');
            if (!target) return;
            const y = target.getBoundingClientRect().top + window.pageYOffset;
            window.scrollTo({ top: y, behavior: 'smooth' });
        } catch (e) {
            console.warn('Kunne ikke scrolle til kartets topp', e);
        }
    }

    showPopulationHint() {
        if (!this.currentCountry || this.populationHintUsed || this.attempts < 2) {
            return;
        }

        const populationHint = document.getElementById('population-hint');
        const populationText = document.getElementById('population-text');
        const populationHintBtn = document.getElementById('population-hint-btn');
        const lockOverlay = document.getElementById('population-lock-overlay');

        if (this.currentCountry.population) {
            const formattedPopulation = this.currentCountry.population.toLocaleString('nb-NO');
            const year = this.currentCountry.populationYear || 'N/A';
            populationText.textContent = `${formattedPopulation} ${this.getText('inhabitants')} (${year})`;
            this.placeHintContentNearButton(populationHint, populationHintBtn);
            // Skjul lock-overlay når hint åpnes
            if (lockOverlay) {
                lockOverlay.style.display = 'none';
            }
            // Ikke skjul knappen - la den være synlig
            this.populationHintUsed = true;
        } else {
            // Hvis ingen befolkningsdata er tilgjengelig, vis en melding
            populationHintBtn.querySelector('h4').textContent = this.getText('no_population_data');
            populationHintBtn.disabled = true;
            this.populationHintUsed = true;
        }
    }

    showCapitalHint() {
        if (!this.currentCountry || this.capitalHintUsed || this.attempts < 3) {
            return;
        }

        const capitalHint = document.getElementById('capital-hint');
        const capitalText = document.getElementById('capital-text');
        const capitalHintBtn = document.getElementById('capital-hint-btn');
        const lockOverlay = document.getElementById('capital-lock-overlay');

        if (this.currentCountry.capital) {
            capitalText.textContent = this.currentCountry.capital;
            this.placeHintContentNearButton(capitalHint, capitalHintBtn);
            // Skjul lock-overlay når hint åpnes
            if (lockOverlay) {
                lockOverlay.style.display = 'none';
            }
            // Ikke skjul knappen - la den være synlig
            this.capitalHintUsed = true;
        } else {
            capitalHintBtn.querySelector('h4').textContent = this.getText('no_capital_data');
            capitalHintBtn.disabled = true;
            this.capitalHintUsed = true;
        }
    }

    showRegionHint() {
        if (!this.currentCountry || this.regionHintUsed || this.attempts < 4) {
            return;
        }

        const regionHint = document.getElementById('region-hint');
        const regionText = document.getElementById('region-text');
        const regionHintBtn = document.getElementById('region-hint-btn');
        const lockOverlay = document.getElementById('region-lock-overlay');

        if (this.currentCountry.region) {
            regionText.textContent = this.currentCountry.region;
            this.placeHintContentNearButton(regionHint, regionHintBtn);
            // Skjul lock-overlay når hint åpnes
            if (lockOverlay) {
                lockOverlay.style.display = 'none';
            }
            // Ikke skjul knappen - la den være synlig
            this.regionHintUsed = true;
        } else {
            regionHintBtn.querySelector('h4').textContent = this.getText('no_region_data');
            regionHintBtn.disabled = true;
            this.regionHintUsed = true;
        }
    }

    showMountainHint() {
        if (!this.currentCountry || this.mountainHintUsed || this.attempts < 5) {
            return;
        }

        const mountainHint = document.getElementById('mountain-hint');
        const mountainText = document.getElementById('mountain-text');
        const mountainHintBtn = document.getElementById('mountain-hint-btn');
        const lockOverlay = document.getElementById('mountain-lock-overlay');

        if (this.currentCountry.highest_mountain) {
            const mountainName = this.currentCountry.highest_mountain;
            const elevationMeters = this.currentCountry.highest_elevation_meters;
            const elevationFeet = this.currentCountry.highest_elevation_feet;
            mountainText.textContent = `${mountainName} (${elevationMeters}m / ${elevationFeet}ft)`;
            this.placeHintContentNearButton(mountainHint, mountainHintBtn);
            // Skjul lock-overlay når hint åpnes
            if (lockOverlay) {
                lockOverlay.style.display = 'none';
            }
            // Ikke skjul knappen - la den være synlig
            this.mountainHintUsed = true;
        } else {
            mountainHintBtn.querySelector('h4').textContent = this.getText('no_mountain_data');
            mountainHintBtn.disabled = true;
            this.mountainHintUsed = true;
        }
    }
    
    showBordersHint() {
        if (!this.currentCountry || this.bordersHintUsed || this.attempts < 6) {
            return;
        }

        const bordersHint = document.getElementById('borders-hint');
        const bordersText = document.getElementById('borders-text');
        const bordersHintBtn = document.getElementById('borders-hint-btn');
        const lockOverlay = document.getElementById('borders-lock-overlay');

        if (this.currentCountry.is_island) {
            bordersText.textContent = this.getText('island_no_borders');
            this.placeHintContentNearButton(bordersHint, bordersHintBtn);
            if (lockOverlay) {
                lockOverlay.style.display = 'none';
            }
            this.bordersHintUsed = true;
        } else if (this.currentCountry.borders && this.currentCountry.borders.length > 0) {
            const borders = this.currentLanguage === 'no' ? 
                (this.currentCountry.borders_no || this.currentCountry.borders) : 
                this.currentCountry.borders;
            bordersText.textContent = Array.isArray(borders) ? borders.join(', ') : borders;
            this.placeHintContentNearButton(bordersHint, bordersHintBtn);
            if (lockOverlay) {
                lockOverlay.style.display = 'none';
            }
            this.bordersHintUsed = true;
        } else {
            bordersHintBtn.querySelector('h4').textContent = this.getText('no_borders_data');
            bordersHintBtn.disabled = true;
            this.bordersHintUsed = true;
        }
    }
    
    revealAllHints() {
        console.log('🎯 revealAllHints() kalt');
        // Hent referanser til knapper for korrekt plassering
        const hintBtn = document.getElementById('hint-btn');
        const populationHintBtn = document.getElementById('population-hint-btn');
        const capitalHintBtn = document.getElementById('capital-hint-btn');
        const regionHintBtn = document.getElementById('region-hint-btn');
        const mountainHintBtn = document.getElementById('mountain-hint-btn');
        const bordersHintBtn = document.getElementById('borders-hint-btn');

        // Vis flagg-hint i raden
        const hintFlag = document.getElementById('hint-flag');
        const hintFlagImg = document.getElementById('hint-flag-img');
        if (hintFlag && hintFlagImg && this.currentCountry.flagFile && hintBtn) {
            hintFlagImg.src = `flags/${this.currentCountry.flagFile}?v=${Date.now()}`;
            this.placeHintContentNearButton(hintFlag, hintBtn);
        }

        // Vis befolknings-hint i raden
        const populationHint = document.getElementById('population-hint');
        const populationText = document.getElementById('population-text');
        if (populationHint && populationText && this.currentCountry.population && populationHintBtn) {
            const formattedPopulation = this.currentCountry.population.toLocaleString('nb-NO');
            const year = this.currentCountry.populationYear || 'N/A';
            populationText.textContent = `${formattedPopulation} ${this.getText('inhabitants')} (${year})`;
            this.placeHintContentNearButton(populationHint, populationHintBtn);
        }

        // Vis hovedstad-hint i raden
        const capitalHint = document.getElementById('capital-hint');
        const capitalText = document.getElementById('capital-text');
        if (capitalHint && capitalText && this.currentCountry.capital && capitalHintBtn) {
            capitalText.textContent = this.currentCountry.capital;
            this.placeHintContentNearButton(capitalHint, capitalHintBtn);
        }

        // Vis region-hint i raden
        const regionHint = document.getElementById('region-hint');
        const regionText = document.getElementById('region-text');
        if (regionHint && regionText && this.currentCountry.region && regionHintBtn) {
            regionText.textContent = this.currentCountry.region;
            this.placeHintContentNearButton(regionHint, regionHintBtn);
        }

        // Vis fjell-hint i raden
        const mountainHint = document.getElementById('mountain-hint');
        const mountainText = document.getElementById('mountain-text');
        if (mountainHint && mountainText && this.currentCountry.highest_mountain && mountainHintBtn) {
            const mountain = this.currentCountry.highest_mountain;
            const meters = this.currentCountry.highest_elevation_meters;
            const feet = this.currentCountry.highest_elevation_feet;
            mountainText.textContent = `${mountain} (${meters}m / ${feet}ft)`;
            this.placeHintContentNearButton(mountainHint, mountainHintBtn);
        }

        // Vis naboland-hint i raden
        const bordersHint = document.getElementById('borders-hint');
        const bordersText = document.getElementById('borders-text');
        if (bordersHint && bordersText && bordersHintBtn) {
            if (this.currentCountry.is_island) {
                bordersText.textContent = this.getText('island_no_borders');
            } else if (this.currentCountry.borders && this.currentCountry.borders.length > 0) {
                const borders = this.currentLanguage === 'no' ? 
                    (this.currentCountry.borders_no || this.currentCountry.borders) : 
                    this.currentCountry.borders;
                bordersText.textContent = Array.isArray(borders) ? borders.join(', ') : borders;
            } else {
                bordersText.textContent = this.getText('no_borders_data');
            }
            this.placeHintContentNearButton(bordersHint, bordersHintBtn);
        }
        
        // Skjul alle lock-overlays
        const lockOverlays = [
            'hint-lock-overlay',
            'population-lock-overlay',
            'capital-lock-overlay',
            'region-lock-overlay',
            'mountain-lock-overlay',
            'borders-lock-overlay'
        ];
        
        lockOverlays.forEach(overlayId => {
            const overlay = document.getElementById(overlayId);
            if (overlay) {
                overlay.style.display = 'none';
            }
        });
    }
    
    giveUp() {
        console.log('🏳️ giveUp() kalt');
        // Vis landnavn i reveal-boks
        const revealBox = document.getElementById('country-reveal-box');
        const revealedCountryName = document.getElementById('revealed-country-name');
        const countryName = this.currentLanguage === 'no' ? 
            this.currentCountry.name_no || this.currentCountry.name : 
            this.currentCountry.name;
        
        revealedCountryName.textContent = countryName;
        revealBox.style.display = 'block';
        
        // Vis alle hint automatisk
        this.revealAllHints();
        
        // Endre knappene
        document.getElementById('submit-btn').style.display = 'none';
        document.getElementById('give-up-btn').style.display = 'none';
        document.getElementById('new-game-btn').style.display = 'block';
        document.getElementById('google-maps-btn').style.display = 'block';
        this.setNorliButtonLabel();
        document.getElementById('norli-btn').style.display = 'block';
        
        // Deaktiver input
        document.getElementById('country-input').disabled = true;
        
        // Sett spill som avsluttet
        this.isGameActive = false;
    }

    openGoogleMaps() {
        console.log('openGoogleMaps called');
        console.log('currentCountry:', this.currentCountry);
        console.log('currentCountry name:', this.currentCountry?.name);
        console.log('google_maps_url exists:', !!this.currentCountry?.google_maps_url);
        console.log('google_maps_url value:', this.currentCountry?.google_maps_url);
        
        if (this.currentCountry && this.currentCountry.google_maps_url) {
            window.open(this.currentCountry.google_maps_url, '_blank');
        } else {
            this.showMessage(this.getText('no_maps_link'), 'error');
        }
    }

    openNorliBooks() {
        console.log('openNorliBooks called');
        console.log('currentCountry:', this.currentCountry);
        console.log('currentCountry name:', this.currentCountry?.name);
        
        if (this.currentCountry && this.currentCountry.name) {
            const countryName = this.currentCountry.name.toLowerCase();
            const norliUrl = `https://www.norli.no/search?query=${encodeURIComponent(countryName)}`;
            console.log('Opening Norli URL:', norliUrl);
            window.open(norliUrl, '_blank');
        } else {
            this.showMessage('Ingen land valgt', 'error');
        }
    }

    setNorliButtonLabel() {
        const norliBtn = document.getElementById('norli-btn');
        if (!norliBtn || !this.currentCountry) return;
        const countryName = this.currentLanguage === 'no' ?
            (this.currentCountry.name_no || this.currentCountry.name) :
            this.currentCountry.name;
        const label = this.currentLanguage === 'no'
            ? `📚 Kjøp reisebøker om ${countryName}`
            : `📚 Buy travel books about ${countryName}`;
        norliBtn.textContent = label;
    }

    showConfigUpdateNotification() {
        const messageContainer = document.getElementById('message-container');
        const messageElement = document.createElement('div');
        messageElement.className = 'message success';
        messageElement.textContent = '🎮 Nye innstillinger mottatt! Starter nytt spill...';
        messageContainer.appendChild(messageElement);
        
        // Remove message after 3 seconds
        setTimeout(() => {
            if (messageElement.parentNode) {
                messageElement.parentNode.removeChild(messageElement);
            }
        }, 3000);
    }
}

// Versjoneringssystem
async function loadVersionInfo() {
    try {
        const response = await fetch('version.json');
        const versionData = await response.json();
        
        // Oppdater versjonsinformasjon i footer
        const versionDisplay = document.getElementById('version-display');
        const buildInfo = document.getElementById('build-info');
        
        if (versionDisplay) {
            versionDisplay.textContent = versionData.tag || versionData.version;
        }
        
        if (buildInfo) {
            buildInfo.textContent = `Build: ${versionData.build}`;
        }
        
        console.log('✅ Versjon lastet:', versionData);
    } catch (error) {
        console.warn('⚠️ Kunne ikke laste versjonsinformasjon:', error);
    }
}

// Check for admin settings on page load
document.addEventListener('DOMContentLoaded', () => {
    loadVersionInfo();
    window.game = new GeographyGame();
    
    // Check if there are admin settings and show notification
    const adminSettings = localStorage.getItem('adminGameSettings');
    if (adminSettings) {
        const settings = JSON.parse(adminSettings);
        if (settings.mode === 'specific' && settings.specificCountry) {
            console.log('Admin: Spesifikt land satt til:', settings.specificCountry);
        }
    }
    
    // Listen for storage changes from admin panel
    window.addEventListener('storage', function(e) {
        if (e.key === 'adminGameSettings') {
            console.log('Admin-innstillinger oppdatert, starter nytt spill...');
            window.game.startNewGame().catch(error => {
                console.error('Error starting new game:', error);
            });
        }
        if (e.key === 'forceNewGame') {
            console.log('Force new game triggered, starter nytt spill...');
            window.game.startNewGame().catch(error => {
                console.error('Error starting new game:', error);
            });
        }
        if (e.key === 'globalGameConfig' || e.key === 'sharedGameConfig') {
            console.log('Config oppdatert, starter nytt spill...');
            window.game.startNewGame().catch(error => {
                console.error('Error starting new game:', error);
            });
        }
    });
    
    // Listen for postMessage events from admin panel
    window.addEventListener('message', function(event) {
        if (event.data && event.data.type === 'CONFIG_UPDATED') {
            console.log('Config oppdatert via postMessage:', event.data.config);
            
            // Update localStorage with the new config
            localStorage.setItem('sharedGameConfig', JSON.stringify(event.data.config));
            localStorage.setItem('globalGameConfig', JSON.stringify(event.data.config));
            
            // Show notification
            window.game.showConfigUpdateNotification();
            
            // Start new game after a short delay
            setTimeout(() => {
                window.game.startNewGame().catch(error => {
                    console.error('Error starting new game:', error);
                });
            }, 1000);
        }
    });
    
    // Also check for forceNewGame on page load
    const forceNewGame = localStorage.getItem('forceNewGame');
    if (forceNewGame) {
        console.log('Force new game found on page load, starter nytt spill...');
        localStorage.removeItem('forceNewGame'); // Clear the flag
        setTimeout(() => {
            window.game.startNewGame().catch(error => {
                console.error('Error starting new game:', error);
            });
        }, 100);
    }
});
