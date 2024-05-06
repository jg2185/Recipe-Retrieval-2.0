import pytest
from unittest.mock import MagicMock, patch

from utils.recipe_searcher import RecipeSearcher

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

#pytest tests/test_recipe_searcher.py
# use the command above within terminal to run pytest