$(document).ready(function () {
    // Fetch cupcakes from the API and display them on page load
    axios.get('/api/cupcakes')
      .then(response => {
        const cupcakes = response.data.cupcakes;
        displayCupcakes(cupcakes);
      })
      .catch(error => {
        console.error('Error fetching cupcakes:', error);
      });
  
    // Handle form submission to add a new cupcake
    $('#cupcake-form').submit(function (event) {
      event.preventDefault();
  
      const flavor = $('#flavor').val();
      const size = $('#size').val();
      const rating = $('#rating').val();
      const image = $('#image').val();
  
      // Make API request to add new cupcake
      axios.post('/api/cupcakes', {
        flavor: flavor,
        size: size,
        rating: rating,
        image: image
      })
        .then(response => {
          const newCupcake = response.data.cupcake;
          // Add the new cupcake to the list on the page
          addCupcakeToList(newCupcake);
          // Clear the form fields
          $('#flavor').val('');
          $('#size').val('');
          $('#rating').val('');
          $('#image').val('');
        })
        .catch(error => {
          console.error('Error adding cupcake:', error);
        });
    });
  
    // Helper function to display cupcakes on the page
    function displayCupcakes(cupcakes) {
      const cupcakeList = $('#cupcake-list');
      cupcakeList.empty();
  
      cupcakes.forEach(cupcake => {
        cupcakeList.append(`<li class="list-group-item d-flex justify-content-between align-items-center">
        ${cupcake.flavor} - Size: ${cupcake.size} - Rating: ${cupcake.rating}
        </li>`);
      });
    }

    // Helper function to add a new cupcake to the list on the page
    function addCupcakeToList(cupcake) {
      const cupcakeList = $('#cupcake-list');
      cupcakeList.append(`<li class="list-group-item d-flex justify-content-between align-items-center">
        ${cupcake.flavor} - Size: ${cupcake.size} - Rating: ${cupcake.rating}
      </li>`);
    }
  });
  