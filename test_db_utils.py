import unittest
from db_utils import fetch_dataframe, add_publication, assign_author
from datetime import date

class TestDBUtils(unittest.TestCase):

    def test_fetch_dataframe_success(self):
        query = "SELECT * FROM publication FETCH FIRST 1 ROWS ONLY"
        df = fetch_dataframe(query)
        self.assertIsNotNone(df)
        self.assertTrue(len(df.columns) > 0)

    def test_add_publication_success(self):
        pub_id = "TEST_PUB_001"
        title = "Test Publication"
        summary = "This is a test summary."
        category = "Testing"
        pub_type = "Journal"
        pub_date = date.today()
        status = "Draft"

        result = add_publication(pub_id, title, summary, category, pub_type, pub_date, status)
        self.assertTrue(result)

    def test_assign_author_success(self):
        pub_id = "TEST_PUB_001"  # Use the same test publication
        author_id = 1            # Must be a valid faculty_id or student_id in your DB
        author_type = "faculty"

        result = assign_author(pub_id, author_id, author_type)
        self.assertTrue(result)

    def test_invalid_query(self):
        df = fetch_dataframe("SELECT * FROM non_existing_table")
        self.assertEqual(len(df), 0)

if __name__ == '__main__':
    unittest.main()
