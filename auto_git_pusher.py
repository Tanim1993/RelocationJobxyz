import os
import subprocess
import datetime
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import atexit

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AutoGitPusher:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        atexit.register(lambda: self.scheduler.shutdown())
    
    def git_add_commit_push(self):
        """Perform git add, commit, and push operations"""
        try:
            # Get current timestamp for commit message
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_message = f"Daily auto-commit: {timestamp}"
            
            # Change to project directory
            project_dir = os.path.dirname(os.path.abspath(__file__))
            os.chdir(project_dir)
            
            # Check if there are changes to commit
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                logger.error(f"Git status failed: {result.stderr}")
                return False
            
            # If no changes, skip
            if not result.stdout.strip():
                logger.info("No changes to commit")
                return True
            
            logger.info(f"Found changes to commit: {len(result.stdout.strip().split(chr(10)))} files")
            
            # Add all changes
            add_result = subprocess.run(['git', 'add', '.'], 
                                      capture_output=True, text=True, timeout=30)
            
            if add_result.returncode != 0:
                logger.error(f"Git add failed: {add_result.stderr}")
                return False
            
            # Commit changes
            commit_result = subprocess.run(['git', 'commit', '-m', commit_message], 
                                         capture_output=True, text=True, timeout=30)
            
            if commit_result.returncode != 0:
                logger.error(f"Git commit failed: {commit_result.stderr}")
                return False
            
            # Push to remote
            push_result = subprocess.run(['git', 'push'], 
                                       capture_output=True, text=True, timeout=60)
            
            if push_result.returncode != 0:
                logger.error(f"Git push failed: {push_result.stderr}")
                return False
            
            logger.info(f"Successfully pushed daily commit: {commit_message}")
            return True
            
        except subprocess.TimeoutExpired:
            logger.error("Git operation timed out")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during git operations: {str(e)}")
            return False
    
    def schedule_daily_push(self, hour=2, minute=0):
        """Schedule daily push at specified time (default: 2:00 AM)"""
        try:
            # Schedule daily push
            self.scheduler.add_job(
                func=self.git_add_commit_push,
                trigger=CronTrigger(hour=hour, minute=minute),
                id='daily_git_push',
                name='Daily Git Push',
                replace_existing=True
            )
            
            logger.info(f"Scheduled daily Git push at {hour:02d}:{minute:02d}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to schedule daily push: {str(e)}")
            return False
    
    def manual_push(self):
        """Trigger manual push for testing"""
        logger.info("Triggering manual Git push...")
        return self.git_add_commit_push()
    
    def get_scheduler_status(self):
        """Get current scheduler status and jobs"""
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append({
                'id': job.id,
                'name': job.name,
                'next_run': job.next_run_time.strftime("%Y-%m-%d %H:%M:%S") if job.next_run_time else "Not scheduled"
            })
        
        return {
            'running': self.scheduler.running,
            'jobs': jobs
        }

# Global instance
auto_pusher = AutoGitPusher()

def init_auto_git_pusher(app=None, daily_hour=2, daily_minute=0):
    """Initialize the auto git pusher with Flask app context"""
    try:
        # Schedule daily push
        auto_pusher.schedule_daily_push(hour=daily_hour, minute=daily_minute)
        
        if app:
            # Add route for manual testing
            @app.route('/admin/manual-git-push')
            def manual_git_push():
                from flask import jsonify
                try:
                    success = auto_pusher.manual_push()
                    return jsonify({
                        'success': success,
                        'message': 'Manual git push completed' if success else 'Manual git push failed'
                    })
                except Exception as e:
                    return jsonify({
                        'success': False,
                        'message': f'Error: {str(e)}'
                    })
            
            # Add route to check scheduler status
            @app.route('/admin/git-scheduler-status')
            def git_scheduler_status():
                from flask import jsonify
                return jsonify(auto_pusher.get_scheduler_status())
        
        logger.info("Auto Git Pusher initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize Auto Git Pusher: {str(e)}")
        return False

if __name__ == "__main__":
    # Test the functionality
    pusher = AutoGitPusher()
    pusher.schedule_daily_push(hour=2, minute=0)  # 2:00 AM daily
    
    print("Auto Git Pusher is running...")
    print("Scheduled daily push at 2:00 AM")
    print("Status:", pusher.get_scheduler_status())
    
    # Keep the script running
    try:
        import time
        while True:
            time.sleep(60)  # Sleep for 1 minute
    except KeyboardInterrupt:
        print("Shutting down Auto Git Pusher...")
        pusher.scheduler.shutdown()