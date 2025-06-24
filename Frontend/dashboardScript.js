let jwtToken = null;
let tokenExpiry = null; 

const CSHARP_API_BASE_URL = 'https://monitoringapi.yellowtree-67f8ca27.northeurope.azurecontainerapps.io'; 

document.addEventListener('DOMContentLoaded', () => {
    login().catch(err => console.error("Initial login on page load failed:", err.message));
});


async function login() {
    const username = "admin";
    const password = "password123";

    try {
        console.log("Attempting to log in...");
        const response = await fetch(`${CSHARP_API_BASE_URL}/api/Auth/login`, { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Login failed: ${response.status} - ${JSON.stringify(errorData)}`);
        }

        const data = await response.json();
        jwtToken = data.accessToken;
        tokenExpiry = new Date(data.expiresAt);

        console.log("Login successful! Token acquired. Expires at:", tokenExpiry);

    } catch (error) {
        console.error('Login error:', error);
        alert(`Authentication required: ${error.message}\nPlease ensure the C# API is running and credentials are correct.`);
        jwtToken = null;
        tokenExpiry = null;
        throw error; 
    }
}


async function predict() {
    const category = document.getElementById('category').value;
    const dayOfWeek = document.getElementById('day').value;
    const predictionType = document.getElementById('prediction').value;
    const predictionResultLabel = document.getElementById('predictionResult');

    predictionResultLabel.textContent = "Loading prediction...";

    if (!jwtToken || (tokenExpiry && new Date() >= tokenExpiry)) {
        console.log("No valid JWT found or token expired. Attempting to re-login...");
        try {
            await login(); 
        } catch (authError) {
            predictionResultLabel.textContent = `Error: Authentication failed. ${authError.message}`;
            return;
        }
    }

    try {
        const headers = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${jwtToken}` 
        };

        const response = await fetch(`${CSHARP_API_BASE_URL}/api/Monitoring/predict/${predictionType}`, {
            method: 'POST',
            headers: headers, 
            body: JSON.stringify({
                category: category,
                day_of_week: dayOfWeek
            })
        });

        if (!response.ok) {
            const errorData = await response.json(); 
            if (response.status === 401) {
                alert("Your session has expired or is invalid. Please refresh the page to re-authenticate.");
                jwtToken = null; 
                tokenExpiry = null; 
            }
            throw new Error(`C# API Error: ${response.status} - ${errorData.detail || JSON.stringify(errorData)}`);
        }

        const data = await response.json();
        console.log("Prediction data from C# API:", data); 

        if (predictionType === 'location') {
            const { latitude, longitude, address } = data; 
            predictionResultLabel.textContent = `Most common location: ${address}`;

        } else if (predictionType === 'temperature') {
            const { prediction, unit } = data;
            predictionResultLabel.textContent = `Most common temperature: ${prediction.toFixed(2)} ${unit}`;
        }

    } catch (error) {
        console.error("Error during prediction:", error);
        predictionResultLabel.textContent = `Error: ${error.message}`;
    }
}