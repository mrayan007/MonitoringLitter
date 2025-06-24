function getDateTime(isoDateTimeString) {
    const date = new Date(isoDateTimeString);

    if (isNaN(date.getTime())) {
        return "Invalid Date";
    }

    const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hourCycle: 'h23'
    };

    return new Intl.DateTimeFormat('en-EN', options).format(date);
}

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function getLocation(lat, lon) {
    const apiKey = 'pk.32eaabb50dc3f777286f5b10b72a7ea1';
    const locationApiUrl = `https://us1.locationiq.com/v1/reverse?key=${apiKey}&lat=${lat}&lon=${lon}&format=json`;

    try {
        const response = await fetch(locationApiUrl);

        if (!response.ok) {
            throw new Error('Error fetching location data.');
        }

        const data = await response.json();

        if (data && data.display_name) {
            return data.display_name;
        } else {
            return "Display name not found in the response.";
        }
    } catch (error) {
        console.error("Error fetching location data:", error);
        return `Failed to get display name: ${error.message}`;
    }
}

async function processLitterData() {
    try {
        const response = await fetch('data/sensoring_data.json');
        if (!response.ok) {
            throw new Error('Error loading JSON data.');
        }
        const litterData = await response.json();

        const tbody = document.querySelector('tbody');
        tbody.innerHTML = '';

        const apiCallDelayMs = 1000;

        for (const litter of litterData) {
            const row = document.createElement('tr');

            const litterLat = litter.locationLat;
            const litterLon = litter.locationLon;

            const litterLocation = await getLocation(litterLat, litterLon);

            const litterDate = getDateTime(litter.dateTime);

            row.innerHTML = `<td>${litter.category}</td>
                             <td>${litterLocation}</td>
                             <td>${litterDate}</td>
                             <td>${litter.temperature}</td>`;

            tbody.appendChild(row);

            let litterIcon;

            switch (litter.category) {
                case 'metaal':
                    litterIcon = L.icon({
                        iconUrl: 'Art/trashCan.png',
                        iconSize: [16, 16],    
                        iconAnchor: [8, 16],   
                        popupAnchor: [0, -16]
                    });
                    break;
                case 'papier-karton':
                    litterIcon = L.icon({
                        iconUrl: 'Art/paper.png',
                        iconSize: [16, 16],    
                        iconAnchor: [8, 16],   
                        popupAnchor: [0, -16]
                    });
                    break;
                case 'glas':
                    litterIcon = L.icon({
                        iconUrl: 'Art/glas.png',
                        iconSize: [16, 16],    
                        iconAnchor: [8, 16],   
                        popupAnchor: [0, -16]
                    });
                    break;
                case 'organisch':
                    litterIcon = L.icon({
                        iconUrl: 'Art/organic.png',
                        iconSize: [16, 16],    
                        iconAnchor: [8, 16],   
                        popupAnchor: [0, -16]
                    });
                    break;
            }

             if (map) {
                const markerLocation = [litterLat, litterLon];
                const newMarker = L.marker(markerLocation, {icon: litterIcon}).addTo(map);

                const popupContent = `
                    <b>Category:</b> ${litter.category}<br>
                    <b>Location:</b> ${litterLocation}<br>
                    <b>Date/Time:</b> ${litterDate}<br>
                    <b>Temperature:</b> ${litter.temperature}°C
                `;
                newMarker.bindPopup(popupContent);

            } else {
                console.warn("Map not initialized when trying to add marker.");
            }

            await delay(apiCallDelayMs);
        }

        if (map && litterData.length > 0) {
            const allLatLons = litterData.map(l => [l.locationLat, l.locationLon]);
            map.fitBounds(allLatLons, { padding: [50, 50] });
        }
    } catch (error) {
        console.error("Error processing data:", error);
        document.querySelector('tbody').innerHTML = `<tr><td colspan="4" style="color: red;">Failed to load data: ${error.message}</td></tr>`;
    }
}

let map = null; 
let marker = null;

document.addEventListener('DOMContentLoaded', () => {
    map = L.map('map', {
        center: [51.5891072, 4.7753679],
        zoom: 15,
        zoomControl: false 
    });

    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap, Carto'
    }).addTo(map);

    processLitterData();
});