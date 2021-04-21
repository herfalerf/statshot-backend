"""User API tests."""
from flask import session
import os
from unittest import TestCase
from models import db, connect_db, User, Preference

os.environ['DATABASE_URL'] = "postgresql:///statshot_test"

from app import app

db.create_all()

class PrefsAPITestCase(TestCase):
    """Test API for prefs"""

    def setUp(self):
        """Create test client, add sample data"""

        db.drop_all()
        db.create_all()

        app.config['SECRET_KEY'] = 'testsecretkey'

        self.client = app.test_client()

        db.session.commit()

    def tearDown(self):
        """Tear down after tests run"""
        resp = super().tearDown()
        db.session.rollback()
        return resp
    
    def test_valid_set_prefs_response(self):
        """Test json response from valid user prefs POST call"""

        with self.client as c:
            reg = c.post('/api/users/register', json={
                                                "username": "validreg", 
                                                "password": "validpass"})

            user = User.query.filter_by(username='validreg').first()
            resp = c.post(f'/api/users/{user.id}/prefs', json={"favTeamId": 25})

            json_data = resp.get_json()

            self.assertEqual(resp.status_code, 200)
            self.assertIn("'favTeam': '25'", str(json_data))
            
    def test_unauthorized_user_set_prefs_response(self):
        """Test json response from unathorized user prefs POST call"""

        with self.client as c:
            reg = c.post('/api/users/register', json={  
                                                "username": "validreg", 
                                                "password": "validpass"})

            resp = c.post('/api/users/9999/prefs', json={"favTeamId": 25})

            json_data = resp.get_json()

            self.assertEqual(resp.status_code, 403)
            self.assertIn("'access': 'Please log in to access this page'", str(json_data))
            self.assertNotIn("'favTeam': '25'", str(json_data))

    def test_no_user_set_prefs_response(self):
        """Test json response when no user is logged in on prefs POST call"""

        with self.client as c:
            reg = c.post('/api/users/register', json={
                                                "username": "validreg", 
                                                "password": "validpass"})

            user = User.query.filter_by(username='validreg').first()
           
            logout = c.post('/api/users/logout')
            
            resp = c.post(f'/api/users/{user.id}/prefs', json={"favTeamId": 25})
            
            json_data = resp.get_json()

            self.assertEqual(resp.status_code, 403)
            self.assertIn("'access': 'Please log in to access this page'", str(json_data))
            self.assertNotIn("'favTeam': '25'", str(json_data))

    def test_valid_user_get_prefs(self):
        """Test that prefs are returned for valid user on GET request"""

        with self.client as c:
            reg = c.post('/api/users/register', json={
                                                "username": "validreg", 
                                                "password": "validpass"})

            user = User.query.filter_by(username='validreg').first()

            set_prefs = c.post(f'/api/users/{user.id}/prefs', json={"favTeamId": 25})

            resp = c.get(f'/api/users/{user.id}/prefs')

            json_data = resp.get_json()

            self.assertEqual(resp.status_code, 200)
            self.assertIn("'favTeam': '25'", str(json_data))

    def test_unathorized_user_get_prefs(self):
        """Test response from user prefs GET call with unauthorized user"""
        with self.client as c:
            reg = c.post('/api/users/register', json={
                                                "username": "validreg", 
                                                "password": "validpass"})

            user = User.query.filter_by(username='validreg').first()

            set_prefs = c.post(f'/api/users/{user.id}/prefs', json={"favTeamId": 25})

            resp = c.get(f'/api/users/9999/prefs')

            json_data = resp.get_json()

            self.assertEqual(resp.status_code, 403)
            self.assertIn("'access': 'Please log in to access this page'", str(json_data))
            self.assertNotIn("'favTeam': '25'", str(json_data))

    def test_no_user_get_prefs(self):
        """Test user prefs GET request with no user"""
        with self.client as c:
            reg = c.post('/api/users/register', json={
                                                "username": "validreg", 
                                                "password": "validpass"})
            
            user = User.query.filter_by(username='validreg').first()

            set_prefs = c.post(f'/api/users/{user.id}/prefs', json={"favTeamId": 25})
           
            logout = c.post('/api/users/logout')
            
            resp = c.get(f'/api/users/{user.id}/prefs')
            
            json_data = resp.get_json()

            self.assertEqual(resp.status_code, 403)
            self.assertIn("'access': 'Please log in to access this page'", str(json_data))
            self.assertNotIn("'favTeam': '25'", str(json_data))

    def test_prefs_in_session_on_post(self):
        """Test that user prefs are added to session on valid POST request"""
        with self.client as c:
            reg = c.post('/api/users/register', json={
                                                "username": "validreg", 
                                                "password": "validpass"})

            user = User.query.filter_by(username='validreg').first()
            
            resp = c.post(f'/api/users/{user.id}/prefs', json={"favTeamId": 25})
            
            prefs = Preference.query.get(user.id)

            self.assertEqual(session['fav_team'], prefs.fav_team_id)
    
    def test_prefs_in_session_on_get(self):
        """Test that user prefs are added to session on valid GET request"""
        with self.client as c:
            reg = c.post('/api/users/register', json={
                                                "username": "validreg", 
                                                "password": "validpass"})

            user = User.query.filter_by(username='validreg').first()
            
            set_prefs = c.post(f'/api/users/{user.id}/prefs', json={"favTeamId": 25})

            session.pop("fav_team", None)

            resp = c.get(f'/api/users/{user.id}/prefs')

            prefs = Preference.query.get(user.id)

            self.assertEqual(session['fav_team'], prefs.fav_team_id)

    def test_no_prefs_in_session_on_logout(self):
        """Test that user prefs are removed from session on logout"""
        with self.client as c:
            reg = c.post('/api/users/register', json={
                                                "username": "validreg", 
                                                "password": "validpass"})

            user = User.query.filter_by(username='validreg').first()
            
            set_prefs = c.post(f'/api/users/{user.id}/prefs', json={"favTeamId": 25})

            prefs = Preference.query.get(user.id)

            self.assertNotIn(str(session), 'fav_team')