import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db


class TestConfig(unittest.TestCase):
   def setUp(self):
    # Set up the Flask application and database for testing
    self.app = create_app()
    self.app.config['TESTING'] = True
    self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database for testing
    self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    self.client = self.app.test_client()

    with self.app.app_context():
        db.create_all()


    def tearDown(self):
        # Clean up the database after each test
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_database(self):
        # Example test to check database connection
        with self.app.app_context():
            self.assertTrue(db.session.query('1').scalar() == 1)

if __name__ == '__main__':
    unittest.main()
