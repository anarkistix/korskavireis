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
        
        this.init();
    }

    async init() {
        console.log('Initialiserer geografisk gjettespill...');
        try {
            await this.loadCountries();
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
    }

    async loadCountries() {
        try {
            console.log('Laster land fra countries_data.json...');
            const response = await fetch('countries_data.json?v=' + Date.now());
            const data = await response.json();
            
            this.countries = data.map(country => {
                const center = country.geometry ? this.calculateCenter(country.geometry) : null;
                if (!center) {
                    console.warn(`Ingen center funnet for ${country.name}`);
                }
                

                
                return {
                    name: country.name,
                    iso3: country.iso3,
                    continent: country.continent,
                    region: country.region,
                    imageFile: country.image_file,
                    flagFile: country.flagFile,
                    population: country.population,
                    populationYear: country.population_year,
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

        // Hint-knapp
        const hintBtn = document.getElementById('hint-btn');
        if (hintBtn) {
            hintBtn.addEventListener('click', () => {
                this.showHint();
            });
        }

        // Befolkningshint-knapp
        const populationHintBtn = document.getElementById('population-hint-btn');
        if (populationHintBtn) {
            populationHintBtn.addEventListener('click', () => {
                this.showPopulationHint();
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
            // First try to load from shared config (highest priority)
            const sharedConfig = localStorage.getItem('sharedGameConfig');
            if (sharedConfig) {
                const config = JSON.parse(sharedConfig);
                console.log('Config loaded from shared storage:', config);
                return {
                    mode: config.gameMode,
                    specificCountry: config.specificCountry
                };
            }
            
            // Then try to load from config.json
            try {
                console.log('Attempting to load config.json...');
                const response = await fetch('config.json?v=' + Date.now());
                console.log('Config.json response status:', response.status);
                if (response.ok) {
                    const config = await response.json();
                    console.log('Config loaded from file:', config);
                    console.log('Config gameMode:', config.gameMode);
                    console.log('Config specificCountry:', config.specificCountry);
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
            
            // Fallback to localStorage
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

        if (guessedCountry.name === this.currentCountry.name) {
            // Riktig gjetting
            this.addFeedbackItem(guessedCountry, true);
            this.showMessage(`Gratulerer! Du gjettet riktig på forsøk ${this.attempts}!`, 'success');
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
                this.showMessage(`Spillet er slutt! Riktig land var: ${this.currentCountry.name}`, 'error');
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
                    detailsDiv.innerHTML = '<span style="color: #28a745; font-weight: 600;">✓ Riktig!</span>';
                } else {
                    if (distance !== null && direction !== null) {
                        detailsDiv.innerHTML = `<span style="color: #666;"><strong>${guessedCountry.name}</strong>. Landet vi skal fram til ligger <strong>${Math.round(distance)} km ${direction}</strong> for <strong>${guessedCountry.name}</strong></span>`;
                    } else {
                        detailsDiv.innerHTML = '<span style="color: #666;">Feil gjetting</span>';
                    }
                }
                

                
                contentDiv.appendChild(detailsDiv);
        
        feedbackItem.appendChild(numberDiv);
        feedbackItem.appendChild(contentDiv);
        
        feedbackContainer.appendChild(feedbackItem);
        
        // Scroll til bunnen av feedback-container
        feedbackContainer.scrollTop = feedbackContainer.scrollHeight;
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
            return 'nord';
        } else if (angle >= 22.5 && angle < 67.5) {
            console.log(`Vinkel ${angle.toFixed(2)}° gir retning: nordøst`);
            return 'nordøst';
        } else if (angle >= 67.5 && angle < 112.5) {
            console.log(`Vinkel ${angle.toFixed(2)}° gir retning: øst`);
            return 'øst';
        } else if (angle >= 112.5 && angle < 157.5) {
            console.log(`Vinkel ${angle.toFixed(2)}° gir retning: sørøst`);
            return 'sørøst';
        } else if (angle >= 157.5 && angle < 202.5) {
            console.log(`Vinkel ${angle.toFixed(2)}° gir retning: sør`);
            return 'sør';
        } else if (angle >= 202.5 && angle < 247.5) {
            console.log(`Vinkel ${angle.toFixed(2)}° gir retning: sørvest`);
            return 'sørvest';
        } else if (angle >= 247.5 && angle < 292.5) {
            console.log(`Vinkel ${angle.toFixed(2)}° gir retning: vest`);
            return 'vest';
        } else if (angle >= 292.5 && angle < 337.5) {
            console.log(`Vinkel ${angle.toFixed(2)}° gir retning: nordvest`);
            return 'nordvest';
        }
        
        // Dette burde aldri skje, men for sikkerhets skyld
        console.log(`Vinkel ${angle.toFixed(2)}° gir fallback: nord`);
        return 'nord';
    }

    endGame(won) {
        this.isGameActive = false;
        document.getElementById('new-game-btn').style.display = 'block';
        document.getElementById('submit-btn').style.display = 'none';
    }

    resetUI() {
        document.getElementById('country-input').value = '';
        document.getElementById('suggestions').innerHTML = '';
        document.getElementById('new-game-btn').style.display = 'none';
        document.getElementById('submit-btn').style.display = 'block';
        this.clearMessages();
        
        // Tøm feedback-container
        document.getElementById('feedback-container').innerHTML = '';
        
        // Skjul bildet og vis loading-indikator
        document.getElementById('country-image').style.display = 'none';
        document.getElementById('loading-indicator').style.display = 'block';
        
        // Reset hint-knapp
        const hintBtn = document.getElementById('hint-btn');
        if (hintBtn) {
            hintBtn.querySelector('h4').textContent = 'Vis flagg som hint';
            hintBtn.disabled = false;
            hintBtn.style.display = 'block'; // Vis knappen igjen
        }
        
        // Reset hint-flag
        document.getElementById('hint-flag').style.display = 'none';

        // Reset befolkningshint-knapp
        const populationHintBtn = document.getElementById('population-hint-btn');
        if (populationHintBtn) {
            populationHintBtn.querySelector('h4').textContent = 'Vis befolkning som hint';
            populationHintBtn.disabled = false;
            populationHintBtn.style.display = 'block'; // Vis knappen igjen
        }
        
        // Reset befolkningshint
        document.getElementById('population-hint').style.display = 'none';
    }

    updateStats() {
        document.getElementById('attempts').textContent = this.attempts;
        document.getElementById('max-attempts').textContent = this.maxAttempts;
        document.getElementById('games-played').textContent = this.gamesPlayed;
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
        if (!this.currentCountry || this.hintUsed) {
            return;
        }

        const hintFlag = document.getElementById('hint-flag');
        const hintFlagImg = document.getElementById('hint-flag-img');
        const hintBtn = document.getElementById('hint-btn');

        if (this.currentCountry.flagFile) {
            hintFlagImg.src = this.currentCountry.flagFile;
            hintFlag.style.display = 'block';
            hintBtn.style.display = 'none'; // Skjul knappen og vis flagget i stedet
            this.hintUsed = true;
        } else {
            // Hvis ingen flagg er tilgjengelig, vis en melding
            hintBtn.querySelector('h4').textContent = 'Ingen flagg tilgjengelig';
            hintBtn.disabled = true;
            this.hintUsed = true;
        }
    }

    showPopulationHint() {
        if (!this.currentCountry || this.populationHintUsed) {
            return;
        }

        const populationHint = document.getElementById('population-hint');
        const populationText = document.getElementById('population-text');
        const populationHintBtn = document.getElementById('population-hint-btn');

        if (this.currentCountry.population) {
            const formattedPopulation = this.currentCountry.population.toLocaleString('nb-NO');
            const year = this.currentCountry.populationYear || 'N/A';
            populationText.textContent = `${formattedPopulation} innbyggere (${year})`;
            populationHint.style.display = 'block';
            populationHintBtn.style.display = 'none'; // Skjul knappen og vis befolkningstall i stedet
            this.populationHintUsed = true;
                        } else {
                    // Hvis ingen befolkningsdata er tilgjengelig, vis en melding
                    populationHintBtn.querySelector('h4').textContent = 'Ingen befolkningsdata tilgjengelig';
                    populationHintBtn.disabled = true;
                    this.populationHintUsed = true;
                }
    }
}

// Check for admin settings on page load
document.addEventListener('DOMContentLoaded', () => {
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
