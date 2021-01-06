const fetch = require("node-fetch");

fetch("https://newscast-api.herokuapp.com/api", {
  method: "GET",
})
  .then(function (response) {
    return response.json();
  })
  .then(function (data) {
    console.log("Request succeeded with JSON response", data);
  })
  .catch(function (error) {
    console.log("Request failed", error);
  });
