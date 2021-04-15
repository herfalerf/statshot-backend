"""Preference model tests."""

import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Preference

os.environ['DATABASE_URL'] = "postgresql:///statshot_test"

from app import app

db.create_all()

class PrefsModelTestCase(TestCase):
    """Tests for Preference model"""

    def setUp(self):
        """Create test client, add sample data"""
        db.drop_all()
        db.create_all()

        u1 = User.register("test1", "passwordtest1")
        uid1 = 1111
        u1.id = uid1

        db.session.commit()

        p1 = Preference(
             user_id = u1.id,
             fav_team_id = 25
        )

        db.session.commit()

        self.p1 = p1
        self.client = app.test_client()

    def tearDown(self):
        """Tear down after each test"""
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_prefs_models(self):
        """Test basic preference functionality"""
        u = User.register("testprefs", "prefsword")
        uid = 222
        u.id = uid
        db.session.add(u)
        db.session.commit()

        p = Preference(
            user_id = u.id,
            fav_team_id = 2
        )
        
        db.session.add(p)
        db.session.commit()

        ptest = Preference.query.get(p.user_id)

        self.assertEqual(ptest.fav_team_id, 2)

    def test_no_user_id(self):
        """Test for None value user id in prefs"""

        u2 = User.register("testprefs", "prefsword")
        uid2 = 222
        u2.id = uid2
        db.session.add(u2)
        db.session.commit()

        p2 = Preference(
            user_id = None,
            fav_team_id = 2
        )

        db.session.add(p2)
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_user_id(self):
        """Test for invalid user id in prefs"""

        u3 = User.register("testprefs", "prefsword")
        uid3 = 333
        u3.id = uid3
        db.session.add(u3)
        db.session.commit()

        p3 = Preference(
            user_id = 99999,
            fav_team_id = 2
        )

        db.session.add(p3)
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()