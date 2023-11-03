import unittest
from app import app, db
from models import User

class UserViewsTests(unittest.TestCase):

    def setUp(self):
        """Set up test client and make a context."""
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        self.client = app.test_client()

        with app.app_context():
            db.create_all()
            test_user = User(first_name="Test", last_name="User")
            db.session.add(test_user)
            db.session.commit()

    def tearDown(self):
        """Tear down test client and database."""
        with app.app_context():
            db.drop_all()

    def test_user_list(self):
        """Test that the user list page shows all users."""
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test User', response.data)

    def test_user_profile(self):
        """Test that the user profile page shows the correct user."""
        response = self.client.get('/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test User', response.data)

    def test_new_user_form(self):
        """Test that the new user form page shows up."""
        response = self.client.get('/users/new')
        self.assertEqual(response.status_code, 200)

    def test_edit_user_form(self):
        """Test that the edit user form page shows up."""
        response = self.client.get('/users/1/edit')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
