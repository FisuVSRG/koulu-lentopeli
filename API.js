const fetch = require('node-fetch');

// Define API endpoint and parameters
const apiKey = "f0a0c00723497a92e619abf61b4ff01748795261f30982390113af56fed5ff8c";
const query = "cats";
const url = `https://serpapi.com/search.json?q=${query}&tbm=isch&api_key=${apiKey}`;

// Make API request
fetch(url)
  .then((response) => response.json())
  .then((data) => {
    // Handle response
    const images = data.images_results;
    images.forEach((image, index) => {
      console.log(`Image ${index + 1}:`, image.original); // Image URL
    });
  })
  .catch((error) => {
    console.error("Error:", error);
  });
