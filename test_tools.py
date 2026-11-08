
import unittest
import tempfile
from pathlib import Path

import pandas as pd
import tools


class TestStudentDataTools(unittest.TestCase):

    def setUp(self):
        # Save the original data file setting
        self.original_data_file = tools.CURRENT_DATA_FILE

        # Create temporary test data
        self.temp_dir = tempfile.TemporaryDirectory()
        self.csv_path = Path(self.temp_dir.name) / "test_students.csv"

        self.test_data = pd.DataFrame({
            "Student_ID": [1, 2, 3, 4],
            "Name": ["Ali", "Huda", "Sara", "Omar"],
            "GPA": [3.2, 3.9, 2.8, 3.9]
        })

        self.test_data.to_csv(self.csv_path, index=False)

    def tearDown(self):
        # Restore original settings
        tools.set_data_file(self.original_data_file)
        self.temp_dir.cleanup()

    def test_set_data_file(self):
        tools.set_data_file(str(self.csv_path))
        self.assertEqual(
            tools.CURRENT_DATA_FILE,
            str(self.csv_path)
        )

    def test_load_data(self):
        df = tools.load_data(str(self.csv_path))

        self.assertEqual(len(df), 4)
        self.assertIn("GPA", df.columns)

    def test_load_data_uses_current_file(self):
        tools.set_data_file(str(self.csv_path))

        df = tools.load_data()

        self.assertEqual(len(df), 4)

    def test_calculate_statistics(self):
        stats = tools.calculate_statistics(self.test_data)

        self.assertEqual(stats["count"], 4)
        self.assertAlmostEqual(stats["average_gpa"], 3.45)
        self.assertAlmostEqual(stats["maximum_gpa"], 3.9)
        self.assertAlmostEqual(stats["minimum_gpa"], 2.8)

    def test_filter_students(self):
        result = tools.filter_students(
            self.test_data,
            "GPA > 3.5"
        )

        self.assertEqual(len(result), 2)

    def test_count_students(self):
        result = tools.count_students(self.test_data)

        self.assertEqual(result, 4)

    def test_highest_gpa(self):
        result = tools.highest_gpa(self.test_data)

        self.assertEqual(len(result), 2)
        self.assertTrue((result["GPA"] == 3.9).all())
        self.assertEqual(
            set(result["Name"]),
            {"Huda", "Omar"}
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
