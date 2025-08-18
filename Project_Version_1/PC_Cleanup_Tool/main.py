#!/usr/bin/env python3
"""
Professional PC Cleanup & Optimization Tool
Industry-standard system maintenance utility for Windows systems
Suitable for personal use and small business deployment

Author: Nick P
Version: 1.0.0
"""

import os
import sys
import shutil
import tempfile
import logging
import subprocess
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import threading
import time
from browser_cleaner import BrowserCacheCleaner

class PCCleanupTool:
    """
    Professional PC cleanup and optimization utility with enterprise-grade features
    """
    
    def __init__(self):
        self.version = "1.0.0"
        self.author = "Nick P"
        self.cleanup_stats = {
            'temp_files_deleted': 0,
            'temp_size_freed': 0,
            'browser_caches_cleared': 0,
            'errors_encountered': 0,
            'start_time': None,
            'end_time': None
        }
        self.setup_logging()
        self.browser_cleaner = BrowserCacheCleaner(self.logger)
        
    def setup_logging(self):
        """Initialize comprehensive logging system"""
        # Try Desktop first, fallback to user directory if Desktop doesn't exist
        desktop_path = Path.home() / "Desktop"
        if desktop_path.exists():
            log_dir = desktop_path / "PC_Cleanup_Logs"
        else:
            log_dir = Path.home() / "PC_Cleanup_Logs"
        
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f"cleanup_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"PC Cleanup Tool v{self.version} initialized")
        
    def is_file_in_use(self, filepath: Path) -> bool:
        """
        Check if a file is currently in use by another process
        Uses Windows-specific method for accurate detection
        """
        try:
            # Try to rename the file to itself (Windows-specific check)
            os.rename(str(filepath), str(filepath))
            return False
        except (OSError, PermissionError):
            return True
            
    def safe_delete_file(self, filepath: Path) -> bool:
        """
        Safely delete a file with proper error handling
        Returns True if successful, False otherwise
        """
        try:
            if not filepath.exists():
                return False
                
            if self.is_file_in_use(filepath):
                self.logger.warning(f"File in use, skipping: {filepath}")
                return False
                
            file_size = filepath.stat().st_size
            filepath.unlink()
            
            self.cleanup_stats['temp_files_deleted'] += 1
            self.cleanup_stats['temp_size_freed'] += file_size
            self.logger.info(f"Deleted: {filepath} ({file_size} bytes)")
            return True
            
        except (PermissionError, OSError) as e:
            self.cleanup_stats['errors_encountered'] += 1
            self.logger.error(f"Failed to delete {filepath}: {e}")
            return False
            
    def clean_temp_files(self) -> Dict[str, int]:
        """
        Clean temporary files from standard Windows temp directories
        Returns statistics about the cleanup operation
        """
        self.logger.info("Starting temporary file cleanup...")
        
        temp_dirs = [
            Path(os.environ.get('TEMP', '')),
            Path(os.environ.get('TMP', '')),
            Path('C:/Windows/Temp'),
            Path('C:/Windows/Prefetch'),
            Path.home() / 'AppData/Local/Temp'
        ]
        
        # Remove duplicates and invalid paths
        temp_dirs = [d for d in set(temp_dirs) if d.exists() and d.is_dir()]
        
        initial_stats = self.cleanup_stats.copy()
        
        for temp_dir in temp_dirs:
            self.logger.info(f"Cleaning directory: {temp_dir}")
            self._clean_directory_recursive(temp_dir)
            
        files_deleted = self.cleanup_stats['temp_files_deleted'] - initial_stats['temp_files_deleted']
        size_freed = self.cleanup_stats['temp_size_freed'] - initial_stats['temp_size_freed']
        
        self.logger.info(f"Temp cleanup complete: {files_deleted} files, {size_freed / 1024 / 1024:.2f} MB freed")
        
        return {
            'files_deleted': files_deleted,
            'size_freed_mb': size_freed / 1024 / 1024,
            'directories_processed': len(temp_dirs)
        }
        
    def _clean_directory_recursive(self, directory: Path, max_depth: int = 3, current_depth: int = 0):
        """
        Recursively clean a directory with depth limiting for safety
        """
        if current_depth > max_depth:
            return
            
        try:
            for item in directory.iterdir():
                if item.is_file():
                    self.safe_delete_file(item)
                elif item.is_dir() and current_depth < max_depth:
                    # Clean subdirectory contents first
                    self._clean_directory_recursive(item, max_depth, current_depth + 1)
                    # Try to remove empty directory
                    try:
                        if not any(item.iterdir()):  # Check if empty
                            item.rmdir()
                            self.logger.info(f"Removed empty directory: {item}")
                    except (OSError, PermissionError):
                        pass  # Directory not empty or permission denied
                        
        except (PermissionError, OSError) as e:
            self.logger.error(f"Error accessing directory {directory}: {e}")
            self.cleanup_stats['errors_encountered'] += 1
            
    def clean_browser_caches(self) -> Dict:
        """
        Clean browser caches using the BrowserCacheCleaner module
        """
        self.logger.info("Starting browser cache cleanup...")
        
        try:
            # Get browser info first
            browser_info = self.browser_cleaner.get_browser_info()
            self.logger.info(f"Detected browsers: {list(browser_info.keys())}")
            
            # Clean all browsers (don't force if running)
            cleanup_results = self.browser_cleaner.clean_all_browsers(force=False)
            
            # Update main cleanup stats
            self.cleanup_stats['browser_caches_cleared'] = cleanup_results['browsers_processed']
            
            return {
                'browsers_detected': len(browser_info),
                'browsers_cleaned': cleanup_results['browsers_processed'],
                'total_cache_freed_mb': cleanup_results['total_size_freed_mb'],
                'browser_details': cleanup_results['browser_results'],
                'browser_info': browser_info
            }
            
        except Exception as e:
            self.logger.error(f"Browser cache cleanup failed: {e}")
            self.cleanup_stats['errors_encountered'] += 1
            return {
                'browsers_detected': 0,
                'browsers_cleaned': 0,
                'total_cache_freed_mb': 0,
                'error': str(e)
            }
            
    def check_windows_updates(self) -> Dict:
        """
        Check Windows Update status using PowerShell commands
        """
        self.logger.info("Checking Windows Update status...")
        
        try:
            # Use PowerShell to check for updates
            powershell_cmd = [
                "powershell", "-Command",
                "Get-WUList -MicrosoftUpdate | Select-Object Title, Size | ConvertTo-Json"
            ]
            
            # Fallback command if PSWindowsUpdate module not available
            fallback_cmd = [
                "powershell", "-Command",
                "$UpdateSession = New-Object -ComObject Microsoft.Update.Session; "
                "$UpdateSearcher = $UpdateSession.CreateUpdateSearcher(); "
                "$SearchResult = $UpdateSearcher.Search('IsInstalled=0'); "
                "$SearchResult.Updates.Count"
            ]
            
            try:
                # Try the advanced command first
                result = subprocess.run(
                    powershell_cmd,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                
                if result.returncode != 0:
                    # Fall back to basic command
                    result = subprocess.run(
                        fallback_cmd,
                        capture_output=True,
                        text=True,
                        timeout=30,
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                    
                if result.returncode == 0:
                    output = result.stdout.strip()
                    
                    try:
                        # Try to parse as number (fallback command)
                        update_count = int(output)
                        status = "Updates Available" if update_count > 0 else "System Up to Date"
                        
                        return {
                            'status': status,
                            'updates_available': update_count,
                            'details': f"{update_count} updates pending" if update_count > 0 else "No updates needed",
                            'last_checked': datetime.now().isoformat()
                        }
                    except ValueError:
                        # Try to parse as JSON (advanced command)
                        try:
                            updates = json.loads(output) if output else []
                            update_count = len(updates) if isinstance(updates, list) else 0
                            
                            return {
                                'status': "Updates Available" if update_count > 0 else "System Up to Date",
                                'updates_available': update_count,
                                'details': updates if update_count > 0 else "No updates needed",
                                'last_checked': datetime.now().isoformat()
                            }
                        except json.JSONDecodeError:
                            return {
                                'status': "Check Complete",
                                'updates_available': 0,
                                'details': "Update status retrieved",
                                'raw_output': output,
                                'last_checked': datetime.now().isoformat()
                            }
                else:
                    self.logger.warning(f"PowerShell command failed: {result.stderr}")
                    return {
                        'status': "Check Failed",
                        'updates_available': -1,
                        'details': "Could not determine update status",
                        'error': result.stderr,
                        'last_checked': datetime.now().isoformat()
                    }
                    
            except subprocess.TimeoutExpired:
                self.logger.warning("Windows Update check timed out")
                return {
                    'status': "Check Timeout",
                    'updates_available': -1,
                    'details': "Update check timed out after 30 seconds",
                    'last_checked': datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"Windows Update check failed: {e}")
            self.cleanup_stats['errors_encountered'] += 1
            return {
                'status': "Check Error",
                'updates_available': -1,
                'details': f"Error checking updates: {str(e)}",
                'last_checked': datetime.now().isoformat()
            }
            
    def run_full_cleanup(self) -> Dict:
        """
        Execute complete cleanup routine with comprehensive reporting
        """
        self.cleanup_stats['start_time'] = datetime.now()
        self.logger.info("=== Starting Full PC Cleanup ===")
        
        results = {}
        
        # Temporary files cleanup
        results['temp_cleanup'] = self.clean_temp_files()
        
        # Browser cache cleanup
        results['browser_cleanup'] = self.clean_browser_caches()
        
        # Windows update check
        results['windows_updates'] = self.check_windows_updates()
        
        # TODO: Add registry cleanup
        
        self.cleanup_stats['end_time'] = datetime.now()
        duration = (self.cleanup_stats['end_time'] - self.cleanup_stats['start_time']).total_seconds()
        
        results['summary'] = {
            'total_files_deleted': self.cleanup_stats['temp_files_deleted'],
            'total_size_freed_mb': self.cleanup_stats['temp_size_freed'] / 1024 / 1024,
            'total_errors': self.cleanup_stats['errors_encountered'],
            'duration_seconds': duration,
            'completion_time': self.cleanup_stats['end_time'].isoformat()
        }
        
        self.logger.info("=== Cleanup Complete ===")
        self.generate_report(results)
        
        return results
        
    def generate_report(self, results: Dict):
        """
        Generate comprehensive cleanup report for user and audit purposes
        """
        # Use same logic as logging for report path
        desktop_path = Path.home() / "Desktop"
        if desktop_path.exists():
            report_path = desktop_path / f"PC_Cleanup_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        else:
            report_path = Path.home() / f"PC_Cleanup_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(report_path, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write(f"PC CLEANUP & OPTIMIZATION REPORT\n")
            f.write(f"Generated by: {self.author}'s PC Cleanup Tool v{self.version}\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"Cleanup Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"System: {os.environ.get('COMPUTERNAME', 'Unknown')}\n")
            f.write(f"User: {os.environ.get('USERNAME', 'Unknown')}\n\n")
            
            if 'temp_cleanup' in results:
                temp = results['temp_cleanup']
                f.write("TEMPORARY FILES CLEANUP:\n")
                f.write(f"  Files Deleted: {temp['files_deleted']}\n")
                f.write(f"  Space Freed: {temp['size_freed_mb']:.2f} MB\n")
                f.write(f"  Directories Processed: {temp['directories_processed']}\n\n")
            
            if 'browser_cleanup' in results:
                browser = results['browser_cleanup']
                f.write("BROWSER CACHE CLEANUP:\n")
                f.write(f"  Browsers Detected: {browser['browsers_detected']}\n")
                f.write(f"  Browsers Cleaned: {browser['browsers_cleaned']}\n")
                f.write(f"  Cache Space Freed: {browser['total_cache_freed_mb']:.2f} MB\n\n")
            
            if 'windows_updates' in results:
                updates = results['windows_updates']
                f.write("WINDOWS UPDATE STATUS:\n")
                f.write(f"  Status: {updates['status']}\n")
                f.write(f"  Updates Available: {updates['updates_available']}\n")
                f.write(f"  Details: {updates['details']}\n")
                f.write(f"  Last Checked: {updates['last_checked']}\n\n")
            
            if 'summary' in results:
                summary = results['summary']
                f.write("OVERALL SUMMARY:\n")
                f.write(f"  Total Files Deleted: {summary['total_files_deleted']}\n")
                f.write(f"  Total Space Freed: {summary['total_size_freed_mb']:.2f} MB\n")
                f.write(f"  Errors Encountered: {summary['total_errors']}\n")
                f.write(f"  Operation Duration: {summary['duration_seconds']:.1f} seconds\n\n")
            
            f.write("=" * 60 + "\n")
            f.write("For technical support or custom solutions:\n")
            f.write(f"Contact: {self.author}\n")
            f.write("Professional PC maintenance and optimization services available\n")
            
        self.logger.info(f"Report generated: {report_path}")


def main():
    """
    Main entry point for the PC Cleanup Tool
    """
    print(f"PC Cleanup & Optimization Tool v1.0.0")
    print(f"Professional system maintenance utility")
    print("=" * 50)
    
    try:
        cleanup_tool = PCCleanupTool()
        results = cleanup_tool.run_full_cleanup()
        
        print("\nCleanup completed successfully!")
        print(f"Files deleted: {results['summary']['total_files_deleted']}")
        print(f"Space freed: {results['summary']['total_size_freed_mb']:.2f} MB")
        print(f"Check Desktop for detailed report")
        
    except Exception as e:
        print(f"Error during cleanup: {e}")
        logging.error(f"Unexpected error: {e}", exc_info=True)
        return 1
        
    return 0


if __name__ == "__main__":
    sys.exit(main())
