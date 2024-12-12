"use strict"
let currentAirports = {};
let currentRound = 0; // Initialize round counter
const maxRounds = 10; // Maximum number of rounds
let airport1Coordinates, airport1Country;
let airport2Coordinates, airport2Country;
let leftMap;
let rightMap;
let leftMarker;
let rightMarker;

function createLeftMap(elementId, coordinates, zoomLevel = 5) { // Default zoom level to 13

     // Avoid modifying the original coordinates array
      const adjustedCoordinates = [coordinates[0], coordinates[1]]; // Add offset to create a new array

      const mapOptions = {
        center: adjustedCoordinates,
        zoom: zoomLevel
      };

      // Create the map instance
      leftMap = L.map(elementId, mapOptions);

      // Add the tile layer with attribution
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(leftMap);
    }

    function createRightMap(elementId, coordinates, zoomLevel = 5) { // Default zoom level to 13

     // Avoid modifying the original coordinates array
      const adjustedCoordinates = [coordinates[0], coordinates[1]]; // Add offset to create a new array

      const mapOptions = {
        center: adjustedCoordinates,
        zoom: zoomLevel
      };

      // Create the map instance
      rightMap = L.map(elementId, mapOptions);

      // Add the tile layer with attribution
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(rightMap);
    }

    function updateLeftMap(elementId, coordinates, zoomLevel = 5){

    if (leftMarker) {
        leftMap.removeLayer(leftMarker);
    }
    // Avoid modifying the original coordinates array
      const adjustedCoordinates = [coordinates[0], coordinates[1]]; // Add offset to create a new array

      const mapOptions = {
        center: adjustedCoordinates,
        zoom: zoomLevel
      };

      leftMap = leftMap.setView(mapOptions.center, mapOptions.zoom);

      leftMarker = L.marker(coordinates).addTo(leftMap);
    }
    function updateRightMap(elementId, coordinates, zoomLevel = 5){

    if (rightMarker) {
        rightMap.removeLayer(rightMarker);
    }
    // Avoid modifying the original coordinates array
      const adjustedCoordinates = [coordinates[0], coordinates[1]]; // Add offset to create a new array

      const mapOptions = {
        center: adjustedCoordinates,
        zoom: zoomLevel
      };

      rightMap = rightMap.setView(mapOptions.center, mapOptions.zoom);

      rightMarker = L.marker(coordinates).addTo(rightMap);
    }

function fetchCountryInfo(countryCode, infoBoxContentId) {
    console.log(countryCode)
            const url = `https://restcountries.com/v3.1/name/${countryCode}`;

            fetch(url).then(response => response.json()).then(data => {
                if (data.length > 0) {
                    const countryData = data[0];
                    const infoBoxContent = document.getElementById(infoBoxContentId);
                    infoBoxContent.textContent = formatCountryInfo(countryData);
                } else {
                    console.error(`No country found for code: ${countryCode}`);
                }
            }).catch(error => console.error(error));
        }

        function formatCountryInfo(countryData) {
            return `
            Country: ${countryData.name.common}
            Capital: ${countryData.capital[0]}
            Population: ${countryData.population.toLocaleString()}
            `;
        }

async function fetchAirports() {
    const response = await fetch('/get_airports');
    const data = await response.json();

    if (data.error) {
        alert(data.error);
        return;
    }

    // Store airport details in variables
        airport1Coordinates = data.airport1.coordinates; // [latitude, longitude]
        airport1Country = data.airport1.country;

        airport2Coordinates = data.airport2.coordinates; // [latitude, longitude]
        airport2Country = data.airport2.country;

    // Store the fetched airports for later comparison
    currentAirports = data;

    // Update button labels with airport names
    document.getElementById("btn1").textContent = `Choose: ${data.airport1.name}`;
    document.getElementById("btn2").textContent = `Choose: ${data.airport2.name}`;

    // Fetch and update country information
    fetchCountryInfo(airport1Country, 'info-left');  // Update left info box
    fetchCountryInfo(airport2Country, 'info-right'); // Update right info box

    console.log('Airport 1 Coordinates:', airport1Coordinates);
    console.log('Airport 1 Country:', airport1Country);
    console.log('Airport 2 Coordinates:', airport2Coordinates);
    console.log('Airport 2 Country:', airport2Country);

    // Ensure the maps are created after the DOM is fully loaded
      updateLeftMap('map-left', airport1Coordinates);
      updateRightMap('map-right', airport2Coordinates);

    //alert(`Airport 1: ${data.airport1.name} (Elevation: ${data.airport1.elevation.toFixed(2)} m),
      //     Airport 2: ${data.airport2.name} (Elevation: ${data.airport2.elevation.toFixed(2)} m)`);
}

async function playGame() {
    console.log("Juuh");
    createLeftMap('map-left', [0, 0]);
    createRightMap('map-right', [0, 0]);
    for (currentRound = 1; currentRound <= maxRounds; currentRound++) {
        //alert(`Round ${currentRound}/${maxRounds}`);
        await fetchAirports(); // Fetch new airport pair for the round

        // Wait for the user to make a selection (handled by button clicks)
        await new Promise((resolve) => {
            document.getElementById("btn1").onclick = () => resolve(playRound("1"));
            document.getElementById("btn2").onclick = () => resolve(playRound("2"));
        });
    }

    // End the game after the loop
    alert(`Game over! Thanks for playing. Your final score is: ${document.getElementById('currentScore').textContent}`);
    await fetch('/save_scores', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
    });
    window.location.href = '/';

}

async function playRound(answer) {
    if (!currentAirports.airport1 || !currentAirports.airport2) {
        alert("No airport combination available. Please try again.");
        return;
    }

    const selectedAirport = answer; // "1" for the first airport, "2" for the second airport
    const response = await fetch('/submit_answer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ selected_airport: selectedAirport })
    });

    const data = await response.json();
    if (data.error) {
        alert(data.error);
        return;
    }

    if (data.correct) {
        alert(`Correct! The higher elevation airport was: Airport ${data.correct_answer}`);
    } else {
        alert(`Wrong! The correct answer was: Airport ${data.correct_answer}`);
    }

    document.getElementById('currentScore').textContent = data.score;
}

console.log(document.getElementById('usernameForm'));
document.getElementsByClassName('username-form')[0].addEventListener('submit', async (e) => {
    e.preventDefault();
    console.log("Juuh")

    const username = document.getElementById('username').value;
    if (!username) {
        alert("Please enter a username.");
        return;
    }

    try {
        const response = await fetch('/start_game', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username })
        });

        const data = await response.json();
        if (data.error) {
            alert(data.error);
            return;
        }

        window.location.href = `/play?username=${username}`;
        // Redirect or update UI if needed
    } catch (err) {
        console.error('Error:', err);
        alert('Something went wrong.');
    }
});