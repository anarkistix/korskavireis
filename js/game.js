// Korskavireis - Geografisk Gjettespill

class GeographyGame {
    constructor() {
        this.countries = [];
        this.currentCountry = null;
        this.attempts = 0;
        this.maxAttempts = 10;
        this.gamesPlayed = 0;
        this.isGameActive = false;
        
        this.init();
    }

    async init() {
        console.log('Initialiserer geografisk gjettespill...');
        await this.loadCountries();
        this.setupEventListeners();
        this.updateStats();
        this.startNewGame();
    }

    async loadCountries() {
        try {
            console.log('Laster land fra GeoJSON-datasett...');
            const response = await fetch('world-administrative-boundaries.geojson');
            const data = await response.json();
            
            this.countries = data.features.map(feature => ({
                name: feature.properties.name,
                iso3: feature.properties.iso3,
                continent: feature.properties.continent,
                region: feature.properties.region,
                coordinates: feature.geometry.coordinates,
                center: feature.properties.geo_point_2d,
                geometry: feature.geometry
            })).filter(country => 
                country.name && 
                country.center && 
                country.geometry &&
                country.geometry.type === 'Polygon' || country.geometry.type === 'MultiPolygon'
            );

            console.log(`Lastet ${this.countries.length} land fra datasettet`);
        } catch (error) {
            console.error('Feil ved lasting av datasett:', error);
            // Fallback til eksempel-data hvis datasettet ikke kan lastes
            this.countries = this.getSampleCountries();
        }
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
            this.showSuggestions(query);
        });

        countryInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                this.submitGuess();
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
            this.submitGuess();
        });

        // Nytt spill-knapp
        document.getElementById('new-game-btn').addEventListener('click', () => {
            this.startNewGame();
        });

        // Klikk utenfor for å lukke forslag
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.input-container')) {
                suggestionsList.innerHTML = '';
            }
        });
    }

    showSuggestions(query) {
        const suggestionsList = document.getElementById('suggestions');
        suggestionsList.innerHTML = '';

        if (query.length < 2) return;

        const matches = this.countries
            .filter(country => 
                country.name.toLowerCase().includes(query) ||
                country.iso3.toLowerCase().includes(query)
            )
            .slice(0, 10);

        matches.forEach(country => {
            const item = document.createElement('div');
            item.className = 'suggestion-item';
            item.textContent = country.name;
            suggestionsList.appendChild(item);
        });
    }

    startNewGame() {
        this.attempts = 0;
        this.isGameActive = true;
        this.gamesPlayed++;
        
        // Velg et tilfeldig land
        this.currentCountry = this.countries[Math.floor(Math.random() * this.countries.length)];
        
        console.log(`Nytt spill startet med: ${this.currentCountry.name}`);
        
        this.updateStats();
        this.displayCountryOutline();
        this.resetUI();
    }

    displayCountryOutline() {
        const canvas = document.getElementById('country-canvas');
        const ctx = canvas.getContext('2d');
        
        // Tøm canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Sett opp transformasjon for å vise landet
        this.setupCanvasTransform(ctx);
        
        // Tegn omrisset
        ctx.strokeStyle = '#000';
        ctx.lineWidth = 2;
        ctx.fillStyle = '#000';
        
        if (this.currentCountry.geometry.type === 'Polygon') {
            this.drawPolygon(ctx, this.currentCountry.geometry.coordinates[0]);
        } else if (this.currentCountry.geometry.type === 'MultiPolygon') {
            this.currentCountry.geometry.coordinates.forEach(polygon => {
                this.drawPolygon(ctx, polygon[0]);
            });
        }
    }

    setupCanvasTransform(ctx) {
        const canvas = document.getElementById('country-canvas');
        
        // Beregn bounding box for landet
        let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
        
        const coordinates = this.currentCountry.geometry.type === 'Polygon' 
            ? [this.currentCountry.geometry.coordinates[0]]
            : this.currentCountry.geometry.coordinates.flat();
        
        coordinates.forEach(coord => {
            coord.forEach(point => {
                minX = Math.min(minX, point[0]);
                minY = Math.min(minY, point[1]);
                maxX = Math.max(maxX, point[0]);
                maxY = Math.max(maxY, point[1]);
            });
        });
        
        // Beregn skala og offset
        const countryWidth = maxX - minX;
        const countryHeight = maxY - minY;
        const canvasWidth = canvas.width;
        const canvasHeight = canvas.height;
        
        const scaleX = (canvasWidth * 0.8) / countryWidth;
        const scaleY = (canvasHeight * 0.8) / countryHeight;
        const scale = Math.min(scaleX, scaleY);
        
        const offsetX = (canvasWidth - countryWidth * scale) / 2;
        const offsetY = (canvasHeight - countryHeight * scale) / 2;
        
        ctx.save();
        ctx.translate(offsetX, offsetY);
        ctx.scale(scale, scale);
        ctx.translate(-minX, -minY);
    }

    drawPolygon(ctx, coordinates) {
        ctx.beginPath();
        coordinates.forEach((coord, index) => {
            if (index === 0) {
                ctx.moveTo(coord[0], coord[1]);
            } else {
                ctx.lineTo(coord[0], coord[1]);
            }
        });
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
        ctx.restore();
    }

    submitGuess() {
        if (!this.isGameActive) return;

        const countryInput = document.getElementById('country-input');
        const guessedCountryName = countryInput.value.trim();
        
        if (!guessedCountryName) {
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
            this.showMessage(`Gratulerer! Du gjettet riktig på forsøk ${this.attempts}!`, 'success');
            this.endGame(true);
        } else {
            const distance = this.calculateDistance(
                this.currentCountry.center.lat, this.currentCountry.center.lon,
                guessedCountry.center.lat, guessedCountry.center.lon
            );
            
            const direction = this.getDirection(
                this.currentCountry.center.lat, this.currentCountry.center.lon,
                guessedCountry.center.lat, guessedCountry.center.lon
            );

            const message = `Feil! ${guessedCountry.name} er ${Math.round(distance)} km ${direction} fra riktig land.`;
            this.showMessage(message, 'info');

            if (this.attempts >= this.maxAttempts) {
                this.showMessage(`Spillet er slutt! Riktig land var: ${this.currentCountry.name}`, 'error');
                this.endGame(false);
            }
        }

        this.updateStats();
        countryInput.value = '';
        document.getElementById('suggestions').innerHTML = '';
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
        
        let direction = '';
        
        if (Math.abs(dLat) > Math.abs(dLon)) {
            direction += dLat > 0 ? 'nord' : 'sør';
        } else {
            direction += dLon > 0 ? 'øst' : 'vest';
        }
        
        if (Math.abs(dLat) > 0 && Math.abs(dLon) > 0) {
            direction += dLat > 0 ? 'øst' : 'vest';
        }
        
        return direction;
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
}

// Initialiser spillet når DOM er lastet
document.addEventListener('DOMContentLoaded', () => {
    window.game = new GeographyGame();
});
