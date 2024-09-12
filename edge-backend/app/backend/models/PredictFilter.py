from typing import Dict, Union

from pydantic import BaseModel


class FilterDataModel(BaseModel):
    filter_value: int


class PredictFilter(FilterDataModel):
    filter_value: int = 5
    filter_counter: int = 5
    static_result: dict = {"classification": "", "confidence-score": 0}

    def set_filter(self, new_value: dict) -> None:
        """
        Updates the filter value using a provided dictionary.

        Args:
            new_value (dict): A dictionary containing a new 'filter_value'.
        """
        self.filter_value = new_value.get("filter_value", self.filter_value)

    def get_filter(self) -> int:
        """
        Retrieves the current filter value.

        Returns:
            int: The current filter value.
        """
        return self.filter_value

    def compare_results(self, new_result) -> Dict[str, Union[str, float]]:
        """
        Compares new results with the static result and updates the static result based on the filter logic.

        Args:
            new_result (dict): A dictionary containing the latest result with 'classification' and 'confidence-score'.

        Returns:
            dict: The result to be used, based on comparison logic.
        """
        if self.static_result["classification"] == new_result["classification"]:
            self.static_result = new_result
            self._reset_filter_counter()
            return new_result
        if self._check_filter_counter():
            self.static_result = new_result
            self._reset_filter_counter()
            return new_result
        self._increase_filter_counter()
        return self.static_result

    def _reset_filter_counter(self) -> None:
        """
        Resets the internal filter counter to zero.
        """
        self.filter_counter = 0

    def _increase_filter_counter(self) -> None:
        """
        Increments the internal filter counter by one.
        """
        self.filter_counter += 1

    def _check_filter_counter(self) -> bool:
        """
        Checks if the filter counter has reached or exceeded the set filter value.

        Returns:
            bool: True if the counter is equal to or exceeds the filter value, otherwise False.
        """
        return self.filter_counter >= self.filter_value

    def reset_filter_result(self) -> None:
        """
        Resets the static results to their default values and sets the filter counter to zero.
        """
        self.static_result = {"classification": "", "confidence-score": 0}
        self.filter_counter = 5
