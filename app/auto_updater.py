"""
Auto-updater module for PrivacyBot.
Handles git pull on startup and every 24 hours with program restart.
"""

import subprocess
import os
import sys
import time
import threading
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AutoUpdater:
    """Handles automatic git pull and program restart."""
    
    def __init__(self, check_interval_hours=24):
        """
        Initialize the auto-updater.
        
        Args:
            check_interval_hours: Hours between update checks (default: 24)
        """
        self.check_interval_seconds = check_interval_hours * 3600
        self.running = False
        self.update_thread = None
        
    def git_pull(self):
        """
        Perform git pull to update the repository.
        
        Returns:
            bool: True if updates were pulled, False otherwise
        """
        try:
            # Get current directory
            repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            logger.info(f"Checking for updates in {repo_dir}")
            
            # Fetch latest changes
            fetch_result = subprocess.run(
                ['git', 'fetch'],
                cwd=repo_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if fetch_result.returncode != 0:
                logger.warning(f"Git fetch failed: {fetch_result.stderr}")
                return False
            
            # Check if there are updates
            status_result = subprocess.run(
                ['git', 'status', '-uno'],
                cwd=repo_dir,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if 'Your branch is behind' in status_result.stdout:
                logger.info("Updates available, pulling changes...")
                
                # Pull the updates
                pull_result = subprocess.run(
                    ['git', 'pull'],
                    cwd=repo_dir,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if pull_result.returncode == 0:
                    logger.info(f"Successfully pulled updates: {pull_result.stdout}")
                    return True
                else:
                    logger.error(f"Git pull failed: {pull_result.stderr}")
                    return False
            else:
                logger.info("Already up to date")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("Git operation timed out")
            return False
        except Exception as e:
            logger.error(f"Error during git pull: {e}")
            return False
    
    def restart_program(self):
        """Restart the current program."""
        logger.info("Restarting program...")
        try:
            # Use os.execv to replace the current process
            python = sys.executable
            os.execv(python, [python] + sys.argv)
        except Exception as e:
            logger.error(f"Error restarting program: {e}")
            # Fallback to exit if exec fails
            sys.exit(0)
    
    def check_and_update(self):
        """Check for updates and restart if needed."""
        if self.git_pull():
            logger.info("Updates pulled, restarting program...")
            self.restart_program()
    
    def update_loop(self):
        """Background thread that checks for updates periodically."""
        while self.running:
            time.sleep(self.check_interval_seconds)
            if self.running:  # Check again in case we stopped during sleep
                logger.info("Scheduled update check triggered")
                self.check_and_update()
    
    def start_scheduled_updates(self):
        """Start the background thread for scheduled updates."""
        if not self.running:
            self.running = True
            self.update_thread = threading.Thread(target=self.update_loop, daemon=True)
            self.update_thread.start()
            logger.info(f"Scheduled updates started (every {self.check_interval_seconds/3600} hours)")
    
    def stop_scheduled_updates(self):
        """Stop the background thread for scheduled updates."""
        self.running = False
        if self.update_thread:
            self.update_thread.join(timeout=5)
            logger.info("Scheduled updates stopped")

def setup_auto_updater(check_interval_hours=24, pull_on_startup=True):
    """
    Set up auto-updater with git pull on startup and scheduled updates.
    
    Args:
        check_interval_hours: Hours between update checks (default: 24)
        pull_on_startup: Whether to pull on initial startup (default: True)
    
    Returns:
        AutoUpdater: The configured auto-updater instance
    """
    updater = AutoUpdater(check_interval_hours)
    
    if pull_on_startup:
        logger.info("Performing initial git pull...")
        updater.check_and_update()
    
    # Start scheduled updates
    updater.start_scheduled_updates()
    
    return updater
