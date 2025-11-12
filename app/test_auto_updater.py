"""
Unit tests for auto_updater module.
"""

import unittest
import os
import sys
import subprocess
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from auto_updater import AutoUpdater, setup_auto_updater


class TestAutoUpdater(unittest.TestCase):
    """Test cases for AutoUpdater class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.updater = AutoUpdater(check_interval_hours=1)
    
    def test_init(self):
        """Test AutoUpdater initialization."""
        self.assertEqual(self.updater.check_interval_seconds, 3600)
        self.assertFalse(self.updater.running)
        self.assertIsNone(self.updater.update_thread)
    
    def test_custom_interval(self):
        """Test AutoUpdater with custom interval."""
        updater = AutoUpdater(check_interval_hours=2)
        self.assertEqual(updater.check_interval_seconds, 7200)
    
    @patch('subprocess.run')
    def test_git_pull_up_to_date(self, mock_run):
        """Test git_pull when repository is up to date."""
        # Mock git fetch
        mock_run.return_value = MagicMock(returncode=0, stdout='', stderr='')
        
        # First call is fetch, second is status
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout='', stderr=''),  # fetch
            MagicMock(returncode=0, stdout='Your branch is up to date', stderr='')  # status
        ]
        
        result = self.updater.git_pull()
        self.assertFalse(result)
        self.assertEqual(mock_run.call_count, 2)
    
    @patch('subprocess.run')
    def test_git_pull_with_updates(self, mock_run):
        """Test git_pull when updates are available."""
        # Mock git operations
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout='', stderr=''),  # fetch
            MagicMock(returncode=0, stdout='Your branch is behind', stderr=''),  # status
            MagicMock(returncode=0, stdout='Updated successfully', stderr='')  # pull
        ]
        
        result = self.updater.git_pull()
        self.assertTrue(result)
        self.assertEqual(mock_run.call_count, 3)
    
    @patch('subprocess.run')
    def test_git_pull_fetch_failure(self, mock_run):
        """Test git_pull when fetch fails."""
        mock_run.return_value = MagicMock(returncode=1, stdout='', stderr='fetch failed')
        
        result = self.updater.git_pull()
        self.assertFalse(result)
    
    @patch('subprocess.run')
    def test_git_pull_pull_failure(self, mock_run):
        """Test git_pull when pull fails."""
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout='', stderr=''),  # fetch
            MagicMock(returncode=0, stdout='Your branch is behind', stderr=''),  # status
            MagicMock(returncode=1, stdout='', stderr='pull failed')  # pull
        ]
        
        result = self.updater.git_pull()
        self.assertFalse(result)
    
    @patch('subprocess.run')
    def test_git_pull_timeout(self, mock_run):
        """Test git_pull when operation times out."""
        mock_run.side_effect = subprocess.TimeoutExpired('git', 30)
        
        result = self.updater.git_pull()
        self.assertFalse(result)
    
    def test_start_stop_scheduled_updates(self):
        """Test starting and stopping scheduled updates."""
        self.updater.start_scheduled_updates()
        self.assertTrue(self.updater.running)
        self.assertIsNotNone(self.updater.update_thread)
        self.assertTrue(self.updater.update_thread.is_alive())
        
        self.updater.stop_scheduled_updates()
        self.assertFalse(self.updater.running)
    
    @patch('auto_updater.AutoUpdater.git_pull')
    @patch('auto_updater.AutoUpdater.restart_program')
    def test_check_and_update_with_updates(self, mock_restart, mock_git_pull):
        """Test check_and_update when updates are available."""
        mock_git_pull.return_value = True
        
        self.updater.check_and_update()
        
        mock_git_pull.assert_called_once()
        mock_restart.assert_called_once()
    
    @patch('auto_updater.AutoUpdater.git_pull')
    @patch('auto_updater.AutoUpdater.restart_program')
    def test_check_and_update_no_updates(self, mock_restart, mock_git_pull):
        """Test check_and_update when no updates available."""
        mock_git_pull.return_value = False
        
        self.updater.check_and_update()
        
        mock_git_pull.assert_called_once()
        mock_restart.assert_not_called()


class TestSetupAutoUpdater(unittest.TestCase):
    """Test cases for setup_auto_updater function."""
    
    @patch('auto_updater.AutoUpdater.check_and_update')
    @patch('auto_updater.AutoUpdater.start_scheduled_updates')
    def test_setup_auto_updater_with_startup_pull(self, mock_start, mock_check):
        """Test setup_auto_updater with pull_on_startup=True."""
        updater = setup_auto_updater(check_interval_hours=2, pull_on_startup=True)
        
        self.assertIsInstance(updater, AutoUpdater)
        mock_check.assert_called_once()
        mock_start.assert_called_once()
    
    @patch('auto_updater.AutoUpdater.check_and_update')
    @patch('auto_updater.AutoUpdater.start_scheduled_updates')
    def test_setup_auto_updater_without_startup_pull(self, mock_start, mock_check):
        """Test setup_auto_updater with pull_on_startup=False."""
        updater = setup_auto_updater(check_interval_hours=2, pull_on_startup=False)
        
        self.assertIsInstance(updater, AutoUpdater)
        mock_check.assert_not_called()
        mock_start.assert_called_once()


if __name__ == '__main__':
    unittest.main()
