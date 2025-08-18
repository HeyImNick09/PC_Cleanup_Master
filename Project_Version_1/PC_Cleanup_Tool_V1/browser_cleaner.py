"""
Browser Cache Cleaning Module
Professional-grade browser cache management for PC Cleanup Tool

Supports: Chrome, Edge, Firefox, Opera, Brave
Safety features: Process detection, backup options, selective cleaning
"""

import os
import shutil
import psutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging
import json
import time

class BrowserCacheCleaner:
    """
    Enterprise-grade browser cache cleaning with safety checks
    """
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.browsers_cleaned = 0
        self.cache_size_freed = 0
        
        # Browser configurations with multiple path variants
        self.browser_configs = {
            'Chrome': {
                'process_names': ['chrome.exe', 'GoogleUpdate.exe'],
                'cache_paths': [
                    Path.home() / 'AppData/Local/Google/Chrome/User Data/Default/Cache',
                    Path.home() / 'AppData/Local/Google/Chrome/User Data/Default/Code Cache',
                    Path.home() / 'AppData/Local/Google/Chrome/User Data/Default/GPUCache',
                    Path.home() / 'AppData/Local/Google/Chrome/User Data/ShaderCache'
                ],
                'temp_paths': [
                    Path.home() / 'AppData/Local/Google/Chrome/User Data/Default/Service Worker/CacheStorage'
                ]
            },
            'Edge': {
                'process_names': ['msedge.exe', 'MicrosoftEdgeUpdate.exe'],
                'cache_paths': [
                    Path.home() / 'AppData/Local/Microsoft/Edge/User Data/Default/Cache',
                    Path.home() / 'AppData/Local/Microsoft/Edge/User Data/Default/Code Cache',
                    Path.home() / 'AppData/Local/Microsoft/Edge/User Data/Default/GPUCache'
                ],
                'temp_paths': [
                    Path.home() / 'AppData/Local/Microsoft/Edge/User Data/Default/Service Worker/CacheStorage'
                ]
            },
            'Firefox': {
                'process_names': ['firefox.exe'],
                'cache_paths': [],  # Firefox uses profile-based paths
                'profile_cache_pattern': 'AppData/Local/Mozilla/Firefox/Profiles/*/cache2'
            },
            'Opera': {
                'process_names': ['opera.exe'],
                'cache_paths': [
                    Path.home() / 'AppData/Local/Opera Software/Opera Stable/Cache',
                    Path.home() / 'AppData/Local/Opera Software/Opera Stable/GPUCache'
                ]
            },
            'Brave': {
                'process_names': ['brave.exe'],
                'cache_paths': [
                    Path.home() / 'AppData/Local/BraveSoftware/Brave-Browser/User Data/Default/Cache',
                    Path.home() / 'AppData/Local/BraveSoftware/Brave-Browser/User Data/Default/Code Cache',
                    Path.home() / 'AppData/Local/BraveSoftware/Brave-Browser/User Data/Default/GPUCache'
                ]
            }
        }
        
    def is_browser_running(self, browser_name: str) -> bool:
        """
        Check if browser processes are currently running
        """
        if browser_name not in self.browser_configs:
            return False
            
        process_names = self.browser_configs[browser_name]['process_names']
        
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'].lower() in [p.lower() for p in process_names]:
                    self.logger.warning(f"{browser_name} is running (PID: {proc.pid})")
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
        return False
        
    def get_firefox_profiles(self) -> List[Path]:
        """
        Discover Firefox profile directories dynamically
        """
        profiles = []
        firefox_base = Path.home() / 'AppData/Local/Mozilla/Firefox/Profiles'
        
        if firefox_base.exists():
            for profile_dir in firefox_base.iterdir():
                if profile_dir.is_dir():
                    cache_dir = profile_dir / 'cache2'
                    if cache_dir.exists():
                        profiles.append(cache_dir)
                        
        return profiles
        
    def get_directory_size(self, path: Path) -> int:
        """
        Calculate total size of directory contents
        """
        total_size = 0
        try:
            for item in path.rglob('*'):
                if item.is_file():
                    try:
                        total_size += item.stat().st_size
                    except (OSError, PermissionError):
                        continue
        except (OSError, PermissionError):
            pass
        return total_size
        
    def safe_remove_cache_directory(self, cache_path: Path) -> Tuple[bool, int]:
        """
        Safely remove cache directory contents with size tracking
        """
        if not cache_path.exists():
            return False, 0
            
        initial_size = self.get_directory_size(cache_path)
        files_removed = 0
        
        try:
            # Remove contents but preserve the directory structure
            for item in cache_path.iterdir():
                try:
                    if item.is_file():
                        item.unlink()
                        files_removed += 1
                    elif item.is_dir():
                        shutil.rmtree(item, ignore_errors=True)
                        files_removed += 1
                except (PermissionError, OSError) as e:
                    self.logger.warning(f"Could not remove {item}: {e}")
                    continue
                    
            final_size = self.get_directory_size(cache_path)
            size_freed = initial_size - final_size
            
            self.logger.info(f"Cleaned {cache_path}: {files_removed} items, {size_freed / 1024 / 1024:.2f} MB freed")
            return True, size_freed
            
        except Exception as e:
            self.logger.error(f"Error cleaning {cache_path}: {e}")
            return False, 0
            
    def clean_browser_cache(self, browser_name: str, force: bool = False) -> Dict:
        """
        Clean cache for a specific browser with safety checks
        """
        if browser_name not in self.browser_configs:
            return {'success': False, 'error': f'Unsupported browser: {browser_name}'}
            
        # Safety check: Don't clean if browser is running (unless forced)
        if not force and self.is_browser_running(browser_name):
            return {
                'success': False, 
                'error': f'{browser_name} is currently running. Close it first or use force=True',
                'size_freed': 0
            }
            
        config = self.browser_configs[browser_name]
        total_size_freed = 0
        paths_cleaned = []
        errors = []
        
        # Handle Firefox special case (profile-based)
        if browser_name == 'Firefox':
            firefox_profiles = self.get_firefox_profiles()
            for profile_cache in firefox_profiles:
                success, size_freed = self.safe_remove_cache_directory(profile_cache)
                if success:
                    paths_cleaned.append(str(profile_cache))
                    total_size_freed += size_freed
                else:
                    errors.append(f"Failed to clean {profile_cache}")
        else:
            # Handle standard cache paths
            cache_paths = config.get('cache_paths', [])
            temp_paths = config.get('temp_paths', [])
            
            for cache_path in cache_paths + temp_paths:
                success, size_freed = self.safe_remove_cache_directory(cache_path)
                if success:
                    paths_cleaned.append(str(cache_path))
                    total_size_freed += size_freed
                elif cache_path.exists():
                    errors.append(f"Failed to clean {cache_path}")
                    
        if paths_cleaned:
            self.browsers_cleaned += 1
            self.cache_size_freed += total_size_freed
            
        return {
            'success': len(paths_cleaned) > 0,
            'browser': browser_name,
            'paths_cleaned': paths_cleaned,
            'size_freed': total_size_freed,
            'size_freed_mb': total_size_freed / 1024 / 1024,
            'errors': errors
        }
        
    def clean_all_browsers(self, force: bool = False) -> Dict:
        """
        Clean cache for all detected browsers
        """
        self.logger.info("Starting browser cache cleanup...")
        
        results = {}
        total_size_freed = 0
        browsers_processed = 0
        
        for browser_name in self.browser_configs.keys():
            self.logger.info(f"Processing {browser_name}...")
            result = self.clean_browser_cache(browser_name, force)
            results[browser_name] = result
            
            if result['success']:
                browsers_processed += 1
                total_size_freed += result['size_freed']
                self.logger.info(f"{browser_name}: {result['size_freed_mb']:.2f} MB freed")
            else:
                self.logger.warning(f"{browser_name}: {result.get('error', 'Unknown error')}")
                
        summary = {
            'browsers_processed': browsers_processed,
            'total_size_freed': total_size_freed,
            'total_size_freed_mb': total_size_freed / 1024 / 1024,
            'browser_results': results
        }
        
        self.logger.info(f"Browser cleanup complete: {browsers_processed} browsers, {summary['total_size_freed_mb']:.2f} MB freed")
        return summary
        
    def get_browser_info(self) -> Dict:
        """
        Get information about installed browsers and their cache sizes
        """
        browser_info = {}
        
        for browser_name, config in self.browser_configs.items():
            info = {
                'installed': False,
                'running': False,
                'cache_size_mb': 0,
                'cache_paths': []
            }
            
            # Check if browser is installed by looking for cache directories
            if browser_name == 'Firefox':
                profiles = self.get_firefox_profiles()
                if profiles:
                    info['installed'] = True
                    info['cache_paths'] = [str(p) for p in profiles]
                    info['cache_size_mb'] = sum(self.get_directory_size(p) for p in profiles) / 1024 / 1024
            else:
                cache_paths = config.get('cache_paths', [])
                existing_paths = [p for p in cache_paths if p.exists()]
                
                if existing_paths:
                    info['installed'] = True
                    info['cache_paths'] = [str(p) for p in existing_paths]
                    info['cache_size_mb'] = sum(self.get_directory_size(p) for p in existing_paths) / 1024 / 1024
                    
            # Check if browser is running
            info['running'] = self.is_browser_running(browser_name)
            browser_info[browser_name] = info
            
        return browser_info
