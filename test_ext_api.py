"""external API tests."""
from flask import session
import os
from unittest import TestCase
from models import db, connect_db



os.environ['DATABASE_URL'] = "postgresql:///statshot_test"

from app import app

db.create_all()

class ExtAPITestCase(TestCase):
    """Test external API calls."""
    
    def setUp(self):
        """Create test client, add sample data"""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()
    
    def tearDown(self):
        """Tear down after tests run"""
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_valid_teams_response(self):
        """Test that external api call for teams list is functioning properly"""

        with self.client as c:
            reg = c.post('/api/users/register', json={
                                                "username": "validreg", 
                                                "password": "validpass"})
            resp = c.get('api/teams')

            json_data = resp.get_json()

            self.assertEqual(resp.status_code, 200)
            self.assertIn("'teamName': 'Stars'", str(json_data))
    
    def test_unauthorized_teams_response(self):
        """Test that teams api call is not accessible by when not logged in"""

        with self.client as c:
            resp = c.get('api/teams')

            json_data = resp.get_json()

            self.assertEqual(resp.status_code, 403)
            self.assertIn('Please log in to access this feature', str(json_data))
    
    def test_valid_specific_team_response(self):
        """Test that external api call for specific team is functioning properly"""
        
        with self.client as c:
            reg = c.post('/api/users/register', json={
                                                "username": "validreg", 
                                                "password": "validpass"})
            resp = c.get('api/teams/25')

            json_data = resp.get_json()

            self.assertEqual(resp.status_code, 200)
            self.assertIn("'teamName': 'Stars'", str(json_data))

    def test_unauthorized_specific_teams_response(self):
        """Test that teams api call is not accessible by when not logged in"""

        with self.client as c:
            resp = c.get('api/teams/25')

            json_data = resp.get_json()

            self.assertEqual(resp.status_code, 403)
            self.assertIn('Please log in to access this feature', str(json_data))