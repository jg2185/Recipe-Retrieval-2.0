
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
        // Hidden loaded state
        document.getElementById('loading').style.display = 'none';
        displayRecipes(data);
    })
    .catch((error) => {
        console.error('Error:', error);
        // You can display some error messages on the page
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


function displayRecipes(recipes) {
    const output = document.getElementById('recipeOutput');
    output.innerHTML = ''; 
    recipes.forEach(recipe => {
        const recipeElement = document.createElement('div');
        recipeElement.innerHTML = `
            <h3>${recipe.title}</h3>
            <p>${recipe.description}</p>
        `;
        output.appendChild(recipeElement);
    });
}

