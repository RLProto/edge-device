import unittest

from app.backend.models.PredictFilter import PredictFilter


class TestPredictFilter(unittest.TestCase):
    def setUp(self):
        self.predict_filter = PredictFilter()

    def test_set_filter(self):
        new_value = {"filter_value": 10}
        self.predict_filter.set_filter(new_value)
        self.assertEqual(self.predict_filter.get_filter(), 10)

    def test_compare_results_same_classification(self):
        initial_result = {"classification": "A", "confidence-score": 0.9}
        self.predict_filter.static_result = initial_result

        new_result = {"classification": "A", "confidence-score": 0.95}
        result = self.predict_filter.compare_results(new_result)
        self.assertEqual(result, new_result)
        self.assertEqual(self.predict_filter.filter_counter, 0)

    def test_compare_results_different_classification_with_reset(self):
        initial_result = {"classification": "A", "confidence-score": 0.9}
        self.predict_filter.static_result = initial_result

        new_result = {"classification": "B", "confidence-score": 0.95}
        self.predict_filter.filter_counter = 5
        result = self.predict_filter.compare_results(new_result)
        self.assertEqual(result, new_result)
        self.assertEqual(self.predict_filter.filter_counter, 0)

    def test_compare_results_different_classification_without_reset(self):
        initial_result = {"classification": "A", "confidence-score": 0.9}
        self.predict_filter.static_result = initial_result

        new_result = {"classification": "B", "confidence-score": 0.95}
        self.predict_filter.filter_counter = 3
        result = self.predict_filter.compare_results(new_result)
        self.assertEqual(result, initial_result)
        self.assertEqual(self.predict_filter.filter_counter, 4)

    def test_reset_filter_result(self):
        self.predict_filter.static_result = {
            "classification": "B",
            "confidence-score": 0.95,
        }
        self.predict_filter.filter_counter = 3
        self.predict_filter.reset_filter_result()
        self.assertEqual(
            self.predict_filter.static_result,
            {"classification": "", "confidence-score": 0},
        )
        self.assertEqual(self.predict_filter.filter_counter, 5)


if __name__ == "__main__":
    unittest.main()
