document.addEventListener('DOMContentLoaded', () => {
    const recipeForm = document.getElementById('recipe-form');
    const recipeList = document.getElementById('recipe-list');
    const searchInput = document.getElementById('search');

    recipeForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        const title = document.getElementById('title').value;
        const ingredients = document.getElementById('ingredients').value;
        const instructions = document.getElementById('instructions').value;
        const imageInput = document.getElementById('image').files[0];
        const reader = new FileReader();

        reader.onload = function(e) {
            const recipe = {
                title,
                ingredients,
                instructions,
                image: e.target.result
            };
            
            addRecipeToList(recipe);
        };

        if (imageInput) {
            reader.readAsDataURL(imageInput);
        }
    });

    searchInput.addEventListener('input', function() {
        const query = searchInput.value.toLowerCase();
        const recipes = document.querySelectorAll('.recipe');
        
        recipes.forEach(recipe => {
            const title = recipe.querySelector('h3').textContent.toLowerCase();
            if (title.includes(query)) {
                recipe.style.display = 'block';
            } else {
                recipe.style.display = 'none';
            }
        });
    });

    function addRecipeToList(recipe) {
        const recipeElement = document.createElement('div');
        recipeElement.className = 'recipe';
        recipeElement.innerHTML = `
            <h3>${recipe.title}</h3>
            <img src="${recipe.image}" alt="${recipe.title}">
            <p><strong>Ingredients:</strong> ${recipe.ingredients}</p>
            <p><strong>Instructions:</strong> ${recipe.instructions}</p>
        `;
        
        recipeList.appendChild(recipeElement);
    }
});
