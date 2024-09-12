import json

from app.backend.models.ImageFilter import FilterSpec


class FilterHandler:
    def __init__(self, recipe_path: str):
        self.recipe_path = recipe_path
        self.filters_list = []
        self.filter_specs = []

    def load_filters(self):
        """Carrega os filtros de um arquivo JSON."""
        try:
            with open(self.recipe_path, "r") as file:
                self.filters_list = json.load(file)
        except:
            self.filters_list = []
        finally:
            self.filter_specs = [FilterSpec(**filter) for filter in self.filters_list]
