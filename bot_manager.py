import os
import asyncio
import subprocess
import shutil
import uuid
from datetime import datetime
from typing import Dict, Tuple, Optional
import logging
from storage import Storage

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BotManager:
    def __init__(self):
        self.bots: Dict[str, dict] = {}
        self.deployment_states: Dict[int, dict] = {}
        self.base_dir = os.path.join(os.getcwd(), "deployed_bots")
        self.storage = Storage()
        self.auto_update_task = None
        self.auto_update_enabled = False
        self.auto_update_interval = 300  # 5 minutes
        
        # Create base directory for deployed bots
        try:
            os.makedirs(self.base_dir, exist_ok=True)
            logger.info(f"Base directory created/verified: {self.base_dir}")
        except Exception as e:
            logger.error(f"Error creating base directory: {str(e)}")
        
        # Auto-restart saved bots on startup
        asyncio.create_task(self._restore_bots())
    
    async def _restore_bots(self):
        """Restore previously deployed bots from storage"""
        try:
            await asyncio.sleep(5)  # Wait for bot to fully initialize
            saved_bots = self.storage.get_all_bots()
            
            if not saved_bots:
                logger.info("No bots to restore")
                return
            
            logger.info(f"Restoring {len(saved_bots)} bots from storage...")
            
            for bot_id, bot_info in saved_bots.items():
                try:
                    # Check if bot directory still exists
                    if not os.path.exists(bot_info["bot_dir"]):
                        logger.warning(f"Bot {bot_id} directory not found, skipping")
                        continue
                    
                    # Try to restart the bot
                    success, msg, process = await self._start_bot_process(
                        bot_id,
                        bot_info["bot_dir"],
                        bot_info["bot_token"]
                    )
                    
                    if success:
                        self.bots[bot_id] = {
                            "process": process,
                            "bot_token": bot_info["bot_token"],
                            "repo_url": bot_info["repo_url"],
                            "bot_dir": bot_info["bot_dir"],
                            "status": "running",
                            "started_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "log_file": bot_info["log_file"]
                        }
                        logger.info(f"Bot {bot_id} restored successfully")
                    else:
                        logger.error(f"Failed to restore bot {bot_id}: {msg}")
                
                except Exception as e:
                    logger.error(f"Error restoring bot {bot_id}: {str(e)}")
            
            logger.info("Bot restoration complete")
        
        except Exception as e:
            logger.error(f"Error in bot restoration: {str(e)}")
    
    async def deploy_bot(self, bot_token: str, repo_url: str, github_token: Optional[str] = None) -> Tuple[bool, str, Optional[str]]:
        """Deploy a new bot from GitHub repository"""
        bot_id = str(uuid.uuid4())[:8]
        bot_dir = os.path.join(self.base_dir, bot_id)
        
        try:
            logger.info(f"Starting deployment for bot {bot_id}")
            
            # Clone repository
            success, msg = await self._clone_repo(repo_url, bot_dir, github_token)
            if not success:
                return False, f"Clone failed: {msg}", None
            
            # Install requirements
            success, msg = await self._install_requirements(bot_dir)
            if not success:
                return False, f"Requirements installation failed: {msg}", None
            
            # Start bot process
            success, msg, process = await self._start_bot_process(bot_id, bot_dir, bot_token)
            if not success:
                return False, f"Bot start failed: {msg}", None
            
            # Store bot info
            self.bots[bot_id] = {
                "process": process,
                "bot_token": bot_token,
                "repo_url": repo_url,
                "bot_dir": bot_dir,
                "status": "running",
                "started_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "log_file": os.path.join(bot_dir, f"{bot_id}.log")
            }
            
            # Save to storage
            self.storage.save_bot(bot_id, self.bots[bot_id])
            
            logger.info(f"Bot {bot_id} deployed successfully")
            return True, "Bot deployed successfully!", bot_id
        
        except Exception as e:
            logger.error(f"Deployment error for bot {bot_id}: {str(e)}")
            # Cleanup on failure
            try:
                if os.path.exists(bot_dir):
                    shutil.rmtree(bot_dir)
            except Exception as cleanup_err:
                logger.error(f"Cleanup error: {str(cleanup_err)}")
            
            return False, f"Deployment error: {str(e)}", None
    
    async def _clone_repo(self, repo_url: str, bot_dir: str, github_token: Optional[str] = None) -> Tuple[bool, str]:
        """Clone GitHub repository"""
        try:
            logger.info(f"Cloning repository: {repo_url}")
            
            # Prepare git clone command
            if github_token:
                # For private repos, inject token into URL
                if "github.com" in repo_url:
                    repo_url = repo_url.replace("https://", f"https://{github_token}@")
            
            # Clone repository
            process = await asyncio.create_subprocess_exec(
                "git", "clone", repo_url, bot_dir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unknown error"
                logger.error(f"Git clone failed: {error_msg}")
                return False, error_msg
            
            logger.info(f"Repository cloned successfully to {bot_dir}")
            return True, "Repository cloned successfully"
        
        except Exception as e:
            logger.error(f"Clone error: {str(e)}")
            return False, str(e)
    
    async def _install_requirements(self, bot_dir: str) -> Tuple[bool, str]:
        """Install requirements from requirements.txt"""
        try:
            req_file = os.path.join(bot_dir, "requirements.txt")
            
            if not os.path.exists(req_file):
                logger.warning(f"No requirements.txt found in {bot_dir}")
                return True, "No requirements.txt found (skipped)"
            
            logger.info(f"Installing requirements from {req_file}")
            
            # Install requirements
            process = await asyncio.create_subprocess_exec(
                "pip", "install", "-r", req_file, "--no-cache-dir",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unknown error"
                logger.error(f"Requirements installation failed: {error_msg}")
                return False, error_msg
            
            logger.info("Requirements installed successfully")
            return True, "Requirements installed successfully"
        
        except Exception as e:
            logger.error(f"Requirements installation error: {str(e)}")
            return False, str(e)
    
    async def _start_bot_process(self, bot_id: str, bot_dir: str, bot_token: str) -> Tuple[bool, str, Optional[asyncio.subprocess.Process]]:
        """Start the bot process"""
        try:
            # Prepare environment variables
            env = os.environ.copy()
            env["BOT_TOKEN"] = bot_token
            
            # Open log file
            log_file_path = os.path.join(bot_dir, f"{bot_id}.log")
            log_file = open(log_file_path, "w")
            
            # Strategy 1: Check for shell scripts (start.sh, run.sh)
            shell_scripts = ["start.sh", "run.sh", "startup.sh"]
            for script_name in shell_scripts:
                script_path = os.path.join(bot_dir, script_name)
                if os.path.exists(script_path):
                    logger.info(f"Found shell script: {script_name}, making it executable")
                    os.chmod(script_path, 0o755)
                    
                    process = await asyncio.create_subprocess_exec(
                        "bash", script_path,
                        cwd=bot_dir,
                        env=env,
                        stdout=log_file,
                        stderr=log_file
                    )
                    
                    await asyncio.sleep(2)
                    if process.returncode is None:
                        logger.info(f"Bot {bot_id} started via {script_name} with PID {process.pid}")
                        return True, f"Bot started successfully via {script_name}", process
            
            # Strategy 2: Check for Python files
            python_files = ["bot.py", "main.py", "app.py", "__main__.py", "run.py"]
            for filename in python_files:
                filepath = os.path.join(bot_dir, filename)
                if os.path.exists(filepath):
                    logger.info(f"Starting bot from {filename}")
                    
                    process = await asyncio.create_subprocess_exec(
                        "python", "-m", filename.replace(".py", ""),
                        cwd=bot_dir,
                        env=env,
                        stdout=log_file,
                        stderr=log_file
                    )
                    
                    await asyncio.sleep(2)
                    if process.returncode is None:
                        logger.info(f"Bot {bot_id} started from {filename} with PID {process.pid}")
                        return True, f"Bot started successfully from {filename}", process
            
            # Strategy 3: Check for Python package (__init__.py)
            init_file = os.path.join(bot_dir, "__init__.py")
            if os.path.exists(init_file):
                logger.info(f"Detected Python package, running as module")
                
                process = await asyncio.create_subprocess_exec(
                    "python", "-m", os.path.basename(bot_dir),
                    cwd=os.path.dirname(bot_dir),
                    env=env,
                    stdout=log_file,
                    stderr=log_file
                )
                
                await asyncio.sleep(2)
                if process.returncode is None:
                    logger.info(f"Bot {bot_id} started as package with PID {process.pid}")
                    return True, "Bot started successfully as Python package", process
            
            # Strategy 4: Check for Procfile (Heroku-style)
            procfile = os.path.join(bot_dir, "Procfile")
            if os.path.exists(procfile):
                logger.info(f"Found Procfile, parsing start command")
                with open(procfile, "r") as f:
                    for line in f:
                        if line.startswith("worker:") or line.startswith("bot:"):
                            command = line.split(":", 1)[1].strip()
                            logger.info(f"Executing Procfile command: {command}")
                            
                            process = await asyncio.create_subprocess_shell(
                                command,
                                cwd=bot_dir,
                                env=env,
                                stdout=log_file,
                                stderr=log_file
                            )
                            
                            await asyncio.sleep(2)
                            if process.returncode is None:
                                logger.info(f"Bot {bot_id} started via Procfile with PID {process.pid}")
                                return True, "Bot started successfully via Procfile", process
            
            # Strategy 5: Look for any .py file with "bot" or "main" in subdirectories
            for root, dirs, files in os.walk(bot_dir):
                for file in files:
                    if file.endswith(".py") and ("bot" in file.lower() or "main" in file.lower()):
                        filepath = os.path.join(root, file)
                        logger.info(f"Trying to start from {filepath}")
                        
                        process = await asyncio.create_subprocess_exec(
                            "python", filepath,
                            cwd=bot_dir,
                            env=env,
                            stdout=log_file,
                            stderr=log_file
                        )
                        
                        await asyncio.sleep(2)
                        if process.returncode is None:
                            logger.info(f"Bot {bot_id} started from {filepath} with PID {process.pid}")
                            return True, f"Bot started successfully from {file}", process
            
            # If nothing worked
            log_file.close()
            logger.error(f"No valid startup method found in {bot_dir}")
            return False, "No valid startup file found. Supported: bot.py, main.py, start.sh, Procfile, or Python package", None
        
        except Exception as e:
            logger.error(f"Error starting bot process: {str(e)}")
            return False, str(e), None
    
    async def stop_bot(self, bot_id: str) -> Tuple[bool, str]:
        """Stop a running bot"""
        try:
            if bot_id not in self.bots:
                return False, f"Bot {bot_id} not found"
            
            bot_info = self.bots[bot_id]
            
            if bot_info["status"] == "stopped":
                return False, f"Bot {bot_id} is already stopped"
            
            logger.info(f"Stopping bot {bot_id}")
            
            # Terminate process
            process = bot_info["process"]
            process.terminate()
            
            try:
                await asyncio.wait_for(process.wait(), timeout=10)
            except asyncio.TimeoutError:
                logger.warning(f"Bot {bot_id} didn't stop gracefully, killing...")
                process.kill()
                await process.wait()
            
            bot_info["status"] = "stopped"
            logger.info(f"Bot {bot_id} stopped successfully")
            
            # Remove from storage
            self.storage.remove_bot(bot_id)
            
            return True, f"Bot {bot_id} stopped successfully"
        
        except Exception as e:
            logger.error(f"Error stopping bot {bot_id}: {str(e)}")
            return False, f"Error stopping bot: {str(e)}"
    
    async def restart_bot(self, bot_id: str) -> Tuple[bool, str]:
        """Restart a bot"""
        try:
            if bot_id not in self.bots:
                return False, f"Bot {bot_id} not found"
            
            logger.info(f"Restarting bot {bot_id}")
            
            bot_info = self.bots[bot_id]
            
            # Stop the bot first
            if bot_info["status"] == "running":
                success, msg = await self.stop_bot(bot_id)
                if not success:
                    return False, f"Failed to stop bot before restart: {msg}"
            
            # Start it again
            success, msg, process = await self._start_bot_process(
                bot_id,
                bot_info["bot_dir"],
                bot_info["bot_token"]
            )
            
            if not success:
                return False, f"Failed to restart bot: {msg}"
            
            bot_info["process"] = process
            bot_info["status"] = "running"
            bot_info["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            logger.info(f"Bot {bot_id} restarted successfully")
            return True, f"Bot {bot_id} restarted successfully"
        
        except Exception as e:
            logger.error(f"Error restarting bot {bot_id}: {str(e)}")
            return False, f"Error restarting bot: {str(e)}"
    
    async def update_bot(self, bot_id: str) -> Tuple[bool, str]:
        """Update bot from GitHub (git pull) and restart"""
        try:
            if bot_id not in self.bots:
                return False, f"Bot {bot_id} not found"
            
            logger.info(f"Updating bot {bot_id} from GitHub")
            
            bot_info = self.bots[bot_id]
            bot_dir = bot_info["bot_dir"]
            
            # Git pull latest changes
            process = await asyncio.create_subprocess_exec(
                "git", "-C", bot_dir, "pull",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unknown error"
                logger.error(f"Git pull failed: {error_msg}")
                return False, f"Git pull failed: {error_msg}"
            
            output = stdout.decode()
            
            # Check if there were any updates
            if "Already up to date" in output or "Already up-to-date" in output:
                logger.info(f"Bot {bot_id} is already up to date")
                return True, f"Bot {bot_id} is already up to date. No restart needed."
            
            # Reinstall requirements in case they changed
            success, msg = await self._install_requirements(bot_dir)
            if not success:
                logger.warning(f"Requirements update failed: {msg}")
                # Continue anyway, old requirements might still work
            
            # Restart the bot to apply changes
            success, msg = await self.restart_bot(bot_id)
            
            if success:
                logger.info(f"Bot {bot_id} updated and restarted successfully")
                return True, f"Bot {bot_id} updated successfully! Changes:\n{output}"
            else:
                return False, f"Bot updated but restart failed: {msg}"
        
        except Exception as e:
            logger.error(f"Error updating bot {bot_id}: {str(e)}")
            return False, f"Error updating bot: {str(e)}"
    
    def list_bots(self) -> Dict[str, dict]:
        """List all deployed bots"""
        try:
            result = {}
            for bot_id, info in self.bots.items():
                result[bot_id] = {
                    "status": info["status"],
                    "repo_url": info["repo_url"],
                    "started_at": info["started_at"]
                }
            return result
        except Exception as e:
            logger.error(f"Error listing bots: {str(e)}")
            return {}
    
    def get_logs(self, bot_id: str, lines: int = 50) -> Optional[str]:
        """Get recent logs for a bot"""
        try:
            if bot_id not in self.bots:
                return None
            
            log_file = self.bots[bot_id]["log_file"]
            
            if not os.path.exists(log_file):
                return "No logs available yet"
            
            # Read last N lines
            with open(log_file, "r") as f:
                all_lines = f.readlines()
                recent_lines = all_lines[-lines:]
                return "".join(recent_lines)
        
        except Exception as e:
            logger.error(f"Error reading logs for bot {bot_id}: {str(e)}")
            return f"Error reading logs: {str(e)}"
    
    async def _auto_update_checker(self):
        """Background task to check for updates"""
        logger.info("Auto-update checker started")
        
        while self.auto_update_enabled:
            try:
                await asyncio.sleep(self.auto_update_interval)
                
                logger.info("Checking for bot updates...")
                
                for bot_id in list(self.bots.keys()):
                    try:
                        bot_info = self.bots[bot_id]
                        
                        if bot_info["status"] != "running":
                            continue
                        
                        bot_dir = bot_info["bot_dir"]
                        
                        # Check if there are updates
                        process = await asyncio.create_subprocess_exec(
                            "git", "-C", bot_dir, "fetch",
                            stdout=asyncio.subprocess.PIPE,
                            stderr=asyncio.subprocess.PIPE
                        )
                        await process.communicate()
                        
                        # Check if local is behind remote
                        process = await asyncio.create_subprocess_exec(
                            "git", "-C", bot_dir, "status", "-uno",
                            stdout=asyncio.subprocess.PIPE,
                            stderr=asyncio.subprocess.PIPE
                        )
                        stdout, _ = await process.communicate()
                        output = stdout.decode()
                        
                        if "Your branch is behind" in output:
                            logger.info(f"Updates available for bot {bot_id}, updating...")
                            success, msg = await self.update_bot(bot_id)
                            
                            if success:
                                logger.info(f"Bot {bot_id} auto-updated successfully")
                            else:
                                logger.error(f"Auto-update failed for bot {bot_id}: {msg}")
                    
                    except Exception as e:
                        logger.error(f"Error checking updates for bot {bot_id}: {str(e)}")
                        continue
            
            except Exception as e:
                logger.error(f"Error in auto-update checker: {str(e)}")
                await asyncio.sleep(60)
    
    def enable_auto_update(self, interval_minutes: int = 5):
        """Enable auto-update checker"""
        if self.auto_update_enabled:
            return False, "Auto-update is already enabled"
        
        self.auto_update_interval = interval_minutes * 60
        self.auto_update_enabled = True
        self.auto_update_task = asyncio.create_task(self._auto_update_checker())
        
        logger.info(f"Auto-update enabled with {interval_minutes} minute interval")
        return True, f"Auto-update enabled! Checking every {interval_minutes} minutes"
    
    def disable_auto_update(self):
        """Disable auto-update checker"""
        if not self.auto_update_enabled:
            return False, "Auto-update is not enabled"
        
        self.auto_update_enabled = False
        
        if self.auto_update_task:
            self.auto_update_task.cancel()
        
        logger.info("Auto-update disabled")
        return True, "Auto-update disabled"
