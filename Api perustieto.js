const countryName = "Finland";
const apiUrl = `https://restcountries.com/v3.1/name/${countryName}`;

fetch(apiUrl)
  .then(response => {
    if (!response.ok) {
      throw new Error("Network response was not ok " + response.statusText);
    }
    return response.json();
  })
  .then(data => {
    const country = data[0];
    console.log("Country:", country.name.common);
    console.log("Capital:", country.capital[0]);
    console.log("Region:", country.region);
    console.log("Population:", country.population);
    console.log("Flag:", country.flags.svg);
    document.body.innerHTML = `
      <h1>${country.name.common}</h1>
      <p><strong>Capital:</strong> ${country.capital[0]}</p>
      <p><strong>Region:</strong> ${country.region}</p>
      <p><strong>Population:</strong> ${country.population}</p>
      <img src="${country.flags.svg}" alt="Flag of ${country.name.common}" width="200">
    `;
  })
  .catch(error => {
    console.error("Error fetching country data:", error);
  });
