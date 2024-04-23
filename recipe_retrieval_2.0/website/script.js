// 这是前端的JavaScript，用于处理用户输入和与后端通信

function submitText() {
    // 获取文本输入并发送到后端
    var ingredients = document.getElementById('textInput').value;
    // 这里应发送请求到后端并处理响应
    fetch('/generate_recipe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ingredients: ingredients})
    })
    .then(response => response.json())
    .then(data => {
        // 用返回的数据做一些事情，比如显示生成的食谱
        console.log(data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
function submitIngredients() {
    var includeIngredients = document.getElementById('includeIngredients').value;
    var excludeIngredients = document.getElementById('excludeIngredients').value;

    fetch('/generate_recipe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            include: includeIngredients, // 包含的成分
            exclude: excludeIngredients  // 排除的成分
        })
    })
    .then(response => response.json())
    .then(data => {
        // 使用返回的数据来展示食谱
        // console.log(data); // 将返回的数据打印到浏览器的控制台中
        displayRecipes(data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}


function submitAudio() {
    // 获取音频并发送到后端
    let audio = document.getElementById('audioInput').files[0];
    // 这里应发送请求到后端并处理响应
}

// 显示多个食谱信息的函数，根据从后端获取的数据
function displayRecipes(recipes) {
    // 先清空现有的食谱输出
    const recipeOutput = document.getElementById('recipeOutput');
    recipeOutput.innerHTML = '';

    // 迭代所有食谱，并为每个食谱创建HTML内容
    recipes.forEach((recipe) => {
        recipeOutput.innerHTML += `
            <div class="recipe">
                <h1>${recipe.title}</h1>
                <h2>成分</h2>
                <ul>${recipe.ingredients.map(i => `<li>${i}</li>`).join('')}</ul>
                <h2>做法</h2>
                <ol>${recipe.instructions.map(step => `<li>${step}</li>`).join('')}</ol>
            </div>
        `;
    });
}

