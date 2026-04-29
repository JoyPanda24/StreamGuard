"""
Test suite for StreamGuard backend modules.
Tests basic functionality of anomaly detection, session tracking, and API endpoints.
"""

import unittest
import sys
import os
import time
import json
from unittest.mock import patch, MagicMock

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from session_tracker import haversine_distance, log_session, get_recent_sessions
from anomaly_detector import (
    check_simultaneous_streams,
    check_impossible_travel,
    check_device_anomaly,
    check_proxy_vpn,
    run_full_analysis
)
from geo_locator import _make_unknown
from ml_model import extract_features, generate_normal_training_data, generate_attack_training_data
from database import init_db, save_session, get_sessions


class TestGeolocation(unittest.TestCase):
    """Test geolocation utilities"""
    
    def test_make_unknown_location(self):
        """Test creation of unknown location"""
        result = _make_unknown("192.168.1.1")
        self.assertEqual(result["country"], "Unknown")
        self.assertEqual(result["countryCode"], "??")
        self.assertEqual(result["lat"], 0.0)

    def test_localhost_detection(self):
        """Test localhost IP handling"""
        from geo_locator import get_location
        result = get_location("127.0.0.1")
        self.assertEqual(result["country"], "LOCAL")
        self.assertEqual(result["city"], "Localhost")


class TestSessionTracking(unittest.TestCase):
    """Test session tracking functionality"""
    
    def test_haversine_distance_calculation(self):
        """Test distance calculation between coordinates"""
        # Distance from New York to London (approx 5570 km)
        distance = haversine_distance(40.7128, -74.0060, 51.5074, -0.1278)
        # Allow some margin (5000-6000 km)
        self.assertGreater(distance, 5000)
        self.assertLess(distance, 6000)

    def test_haversine_same_location(self):
        """Test distance between same locations"""
        distance = haversine_distance(40.7128, -74.0060, 40.7128, -74.0060)
        self.assertAlmostEqual(distance, 0.0, places=1)

    def test_haversine_opposite_poles(self):
        """Test distance between opposite poles"""
        distance = haversine_distance(90, 0, -90, 0)
        # Earth's circumference is ~40075 km, half is ~20037 km
        self.assertGreater(distance, 19900)
        self.assertLess(distance, 20100)


class TestAnomalyDetection(unittest.TestCase):
    """Test anomaly detection algorithms"""
    
    @patch('anomaly_detector.get_recent_sessions')
    def test_check_simultaneous_streams(self, mock_sessions):
        """Test detection of simultaneous streams"""
        mock_sessions.return_value = [
            {"ip": "192.168.1.1", "timestamp": time.time()},
            {"ip": "192.168.1.2", "timestamp": time.time()},
            {"ip": "192.168.1.3", "timestamp": time.time()},
        ]
        result = check_simultaneous_streams("user1", max_allowed=2)
        self.assertTrue(result["flag"])
        self.assertEqual(result["severity"], "HIGH")

    @patch('anomaly_detector.get_recent_sessions')
    def test_no_simultaneous_streams(self, mock_sessions):
        """Test normal stream (single IP)"""
        mock_sessions.return_value = [
            {"ip": "192.168.1.1", "timestamp": time.time()},
        ]
        result = check_simultaneous_streams("user1", max_allowed=2)
        self.assertFalse(result["flag"])

    @patch('anomaly_detector.get_recent_sessions')
    def test_check_device_anomaly(self, mock_sessions):
        """Test detection of unknown devices"""
        mock_sessions.return_value = [
            {"device": "mobile_android", "timestamp": time.time()},
            {"device": "unknown_device", "timestamp": time.time()},
        ]
        result = check_device_anomaly("user1", known_devices=["mobile_android", "web_chrome"])
        self.assertTrue(result["flag"])
        self.assertEqual(result["severity"], "MEDIUM")

    @patch('anomaly_detector.get_recent_sessions')
    def test_no_device_anomaly(self, mock_sessions):
        """Test normal devices"""
        mock_sessions.return_value = [
            {"device": "mobile_android", "timestamp": time.time()},
        ]
        result = check_device_anomaly("user1", known_devices=["mobile_android", "web_chrome"])
        self.assertFalse(result["flag"])


class TestMLModel(unittest.TestCase):
    """Test ML model utilities"""
    
    def test_generate_normal_training_data(self):
        """Test generation of normal behavior data"""
        data = generate_normal_training_data(100)
        self.assertEqual(data.shape[0], 100)
        self.assertEqual(data.shape[1], 8)  # 8 features

    def test_generate_attack_training_data(self):
        """Test generation of attack behavior data"""
        data = generate_attack_training_data(50)
        self.assertEqual(data.shape[0], 50)
        self.assertEqual(data.shape[1], 8)  # 8 features

    def test_extract_features_empty_sessions(self):
        """Test feature extraction with no sessions"""
        result = extract_features([])
        self.assertIsNone(result)

    def test_extract_features_single_session(self):
        """Test feature extraction with single session"""
        sessions = [{
            "timestamp": time.time(),
            "ip": "192.168.1.1",
            "country": "US",
            "device": "mobile_android",
            "proxy": 0,
            "hosting": 0,
            "lat": 40.7128,
            "lon": -74.0060
        }]
        result = extract_features(sessions)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 8)  # Should extract 8 features


class TestDatabase(unittest.TestCase):
    """Test database operations"""
    
    def setUp(self):
        """Initialize test database"""
        os.environ['TEST_DB'] = '1'
        from config import DB_PATH as test_db
        self.test_db = test_db
        init_db()

    def test_save_and_retrieve_session(self):
        """Test saving and retrieving sessions"""
        session_data = {
            "user_id": "test_user",
            "ip": "192.168.1.1",
            "country": "US",
            "city": "New York",
            "lat": 40.7128,
            "lon": -74.0060,
            "isp": "Test ISP",
            "proxy": 0,
            "hosting": 0,
            "device": "mobile_android",
            "timestamp": time.time()
        }
        save_session(session_data)
        
        # Retrieve and verify
        sessions = get_sessions("test_user", window_seconds=3600)
        self.assertGreater(len(sessions), 0)
        self.assertEqual(sessions[0]["user_id"], "test_user")


class TestFullAnalysis(unittest.TestCase):
    """Test full analysis pipeline"""
    
    @patch('anomaly_detector.check_simultaneous_streams')
    @patch('anomaly_detector.check_impossible_travel')
    @patch('anomaly_detector.check_device_anomaly')
    @patch('anomaly_detector.check_proxy_vpn')
    @patch('anomaly_detector.check_ml_anomaly')
    def test_full_analysis_low_risk(self, mock_ml, mock_proxy, mock_device, mock_travel, mock_streams):
        """Test full analysis with low-risk scenario"""
        # Mock all checks to return no flags
        mock_streams.return_value = {"flag": False}
        mock_travel.return_value = {"flag": False}
        mock_device.return_value = {"flag": False}
        mock_proxy.return_value = {"flag": False}
        mock_ml.return_value = {"flag": False}
        
        result = run_full_analysis("test_user")
        self.assertEqual(result["overall_risk"], "LOW")
        self.assertEqual(len(result["flags"]), 0)

    @patch('anomaly_detector.check_simultaneous_streams')
    @patch('anomaly_detector.check_impossible_travel')
    @patch('anomaly_detector.check_device_anomaly')
    @patch('anomaly_detector.check_proxy_vpn')
    @patch('anomaly_detector.check_ml_anomaly')
    def test_full_analysis_high_risk(self, mock_ml, mock_proxy, mock_device, mock_travel, mock_streams):
        """Test full analysis with high-risk scenario"""
        # Mock streams check to flag high risk
        mock_streams.return_value = {"flag": True, "severity": "HIGH", "reason": "Multiple streams"}
        mock_travel.return_value = {"flag": False}
        mock_device.return_value = {"flag": False}
        mock_proxy.return_value = {"flag": False}
        mock_ml.return_value = {"flag": False}
        
        result = run_full_analysis("test_user")
        self.assertEqual(result["overall_risk"], "HIGH")
        self.assertGreater(len(result["flags"]), 0)

    @patch('anomaly_detector.check_simultaneous_streams')
    @patch('anomaly_detector.check_impossible_travel')
    @patch('anomaly_detector.check_device_anomaly')
    @patch('anomaly_detector.check_proxy_vpn')
    @patch('anomaly_detector.check_ml_anomaly')
    def test_full_analysis_critical_risk(self, mock_ml, mock_proxy, mock_device, mock_travel, mock_streams):
        """Test full analysis with critical-risk scenario"""
        # Mock impossible travel check to flag critical risk
        mock_streams.return_value = {"flag": False}
        mock_travel.return_value = {"flag": True, "severity": "CRITICAL", "reason": "Impossible travel"}
        mock_device.return_value = {"flag": False}
        mock_proxy.return_value = {"flag": False}
        mock_ml.return_value = {"flag": False}
        
        result = run_full_analysis("test_user")
        self.assertEqual(result["overall_risk"], "CRITICAL")
        self.assertGreater(len(result["flags"]), 0)


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestGeolocation))
    suite.addTests(loader.loadTestsFromTestCase(TestSessionTracking))
    suite.addTests(loader.loadTestsFromTestCase(TestAnomalyDetection))
    suite.addTests(loader.loadTestsFromTestCase(TestMLModel))
    suite.addTests(loader.loadTestsFromTestCase(TestDatabase))
    suite.addTests(loader.loadTestsFromTestCase(TestFullAnalysis))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
