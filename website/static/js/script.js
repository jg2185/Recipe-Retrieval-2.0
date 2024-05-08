
function submitIngredients() {
    var includeIngredients = document.getElementById('includeIngredients').value.trim();
    var excludeIngredients = document.getElementById('excludeIngredients').value.trim();

    if (!includeIngredients && !excludeIngredients) {
        alert('Please enter at least one ingredient.');
        return;
    }

    // Show loading status
    document.getElementById('loading').style.display = 'block';

    fetch('/generate_recipe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            include: includeIngredients,
            exclude: excludeIngredients
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Hidden loading status
        console.log(data)
        document.getElementById('loading').style.display = 'none';
        displayRecipes(data.data);
    })
    .catch((error) => {
        console.error('Error:', error);
        // display some error messages on the page
        document.getElementById('error').innerText = 'Failed to load data: ' + error.message;
    });
}


function submit_voice(text) {
    fetch('/submit_voice', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: text })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data.message);
        displayRecipes(data.recipe);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// displays multiple recipe information based on data obtained from the back end
function displayRecipes(recipes) {
    // Clear the existing recipe output first
    const recipeOutput = document.getElementById('recipeOutput');
    recipeOutput.innerHTML = '';

    // Check if recipes is a string (single recipe in text form)
    if (typeof recipes === 'string') {
        recipeOutput.innerHTML += `
            <div class="recipe">
                ${recipes}$
            </div>
        `;
    } else if (Array.isArray(recipes)) {
        // Handle an array of recipe objects
        recipes.forEach(recipe => {
            const ingredientsHtml = recipe.ingredients.map(ingredient => `<li>${ingredient}</li>`).join('');
            const instructionsHtml = recipe.instructions.split('\n').map(step => `<li>${step}</li>`).join('');

            recipeOutput.innerHTML += `
                <div class="recipe">
                    <h2>${recipe.title}</h2>
                    <h2>Ingredients:</h2>
                    <ul>${ingredientsHtml}</ul>
                    <h2>Instructions:</h2>
                    <ol>${instructionsHtml}</ol>
                </div>
            `;
        });
    }
}



