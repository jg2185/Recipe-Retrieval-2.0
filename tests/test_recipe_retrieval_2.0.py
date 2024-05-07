import pytest
from unittest.mock import MagicMock, patch

from utils.recipe_searcher import RecipeSearcher
from src.recipe_retrieval_2.utils import preprocess


def test_load_index():
    with patch("builtins.open", new_callable=pytest.mock.mock_open, read_data='{"ingredient": ["1", "2"]}'):
        searcher = RecipeSearcher("inverted_index.json")
        assert searcher.load_index("inverted_index.json") == {"ingredient": ["1", "2"]}

def test_get_user_input():
    with patch("builtins.input", return_value="salt, pepper, olive oil,"):
        searcher = RecipeSearcher("inverted_index.json")
        assert searcher.get_user_input() == ["salt", "pepper", "oliv oil"]

def test_generate_recipe():
    with patch("transformers.pipeline") as mock_pipeline:
        mock_pipeline.return_value = MagicMock()
        mock_pipeline.return_value.__call__.return_value = [{'generated_text': 'Recipe: Use salt and pepper'}]
        searcher = RecipeSearcher("inverted_index.json")
        prompt = "Recipe with ingredients: salt, pepper"
        assert searcher.generate_recipe(prompt) == 'Recipe: Use salt and pepper'

def test_display_recipes_no_matches():
    with patch.object(RecipeSearcher, 'load_recipes', return_value={}),patch.object(RecipeSearcher, 'generate_recipe', return_value="Generated recipe for input ingredients") as mock_gen:
        searcher = RecipeSearcher("inverted_index.json")
        searcher.index = {'salt': ['1'], 'pepper': ['2']}
        searcher.display_recipes(['salt'], ['sugar'])
        mock_gen.assert_called_once_with("Recipe with ingredients: salt:")

def test_remove_duplicate_paragraphs():
    text = "Line1\nLine2\nLine1\nLine3"
    searcher = RecipeSearcher("inverted_index.json")
    assert searcher.remove_duplicate_paragraphs(text) == "Line1\nLine2\nLine3"

lobster_text = "{'title': 'Maine Lobster Rolls', 'ingredients': ['4 top--sliced hot-dog buns (or fashion your own top-sliced buns from bread)', '2 tablespoons unsalted butter, softened', '2 cups coarsely chopped cooked lobster (from about (3) 11/4 pound lobsters, cool but not cold', '4 tablespoons melted butter or 3 tablespoons mayonnaise mixed with 2 tablespoons minced celery'], 'instructions': 'If using top-sliced buns, spread softened butter on outsides; if using hamburger buns, butter insides. Heat a griddle or heavy skillet over moderately high heat until hot and toast buns, buttered sides only, until light brown. Divide lobster meat among buns and either drizzle melted butter over lobster or dollop with mayonnaise mixture.;'}"

def test_readable():
    readable_text = preprocess.FormatJson.readable("test_data.json")
    readable_lobster = readable_text[0]
    assert lobster_text == readable_lobster

lobster_ingredients = ['top hot-dog bun fashion own top-slic bun bread', 'unsalt butter', 'lobster lobster cool', 'butter mix celeri']

def test_preprocess():
    all_ingredients = preprocess.GetIngredients.get_ingredients("test_data.json")
    test_ingredients = all_ingredients[0]
    assert lobster_ingredients == test_ingredients

#pytest tests/test_recipe_searcher.py
# use the command above within terminal to run pytest
