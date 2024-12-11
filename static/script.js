   let currentAirports = {};
let currentRound = 0; // Initialize round counter
const maxRounds = 10; // Maximum number of rounds

async function fetchAirports() {
    const response = await fetch('/get_airports');
    const data = await response.json();

    if (data.error) {
        alert(data.error);
        return;
    }

    // Store the fetched airports for later comparison
    currentAirports = data;

    // Update button labels with airport names
    document.getElementById("btn1").textContent = `Choose: ${data.airport1.name}`;
    document.getElementById("btn2").textContent = `Choose: ${data.airport2.name}`;

    alert(`Airport 1: ${data.airport1.name} (Elevation: ${data.airport1.elevation.toFixed(2)} m),
           Airport 2: ${data.airport2.name} (Elevation: ${data.airport2.elevation.toFixed(2)} m)`);
}

async function playGame() {
    for (currentRound = 1; currentRound <= maxRounds; currentRound++) {
        alert(`Round ${currentRound}/${maxRounds}`);
        await fetchAirports(); // Fetch new airport pair for the round

        // Clear previous button handlers
        document.getElementById("btn1").onclick = null;
        document.getElementById("btn2").onclick = null;

        // Wait for the user to make a selection (handled by button clicks)
        await new Promise((resolve) => {
            document.getElementById("btn1").onclick = () => resolve(playRound("1"));
            document.getElementById("btn2").onclick = () => resolve(playRound("2"));
        });
    }

    // End the game after the loop
    alert(`Game over! Thanks for playing. Your final score is: ${document.getElementById('currentScore').textContent}`);
    document.getElementById('gameContent').style.display = 'none';
    document.getElementById('usernameForm').style.display = 'block';
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

document.getElementById('usernameForm').addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevent the default form submission behavior

    const username = document.getElementById('username').value;

    if (!username) {
        alert("Please enter a username.");
        return;
    }

    try {
        // Send username to the backend
        const response = await fetch('/start_game', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username }), // Only pass username here
        });

        const data = await response.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        // Save the user_id and game_id in localStorage/sessionStorage
        localStorage.setItem('user_id', data.user_id);
        localStorage.setItem('game_id', data.game_id);

        // Redirect to the game page
        window.location.href = '/play.html';
    } catch (err) {
        console.error("Error starting the game:", err);
        alert("Something went wrong. Please try again.");
    }

    document.getElementById('displayUsername').textContent = username;
    document.getElementById('usernameForm').style.display = 'none';
    document.getElementById('gameContent').style.display = 'block';

    await playGame(); // Start the game
});