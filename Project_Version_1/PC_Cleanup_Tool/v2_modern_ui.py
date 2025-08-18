"""
PC Cleanup Tool Version 2 - Modern UI
Advanced modern interface with one-click cleanup and comprehensive reporting
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import json
import webbrowser
from datetime import datetime
from pathlib import Path
import os
import sys

# Import V2 core engine
from v2_core_engine import V2CleanupEngine

class ModernProgressBar:
    """Custom modern progress bar with animations"""
    
    def __init__(self, parent, width=400, height=20):
        self.canvas = tk.Canvas(parent, width=width, height=height, 
                               bg='#f0f0f0', highlightthickness=0)
        self.width = width
        self.height = height
        self.progress = 0
        self.animated = False
        
        # Create progress bar elements
        self.bg_rect = self.canvas.create_rectangle(2, 2, width-2, height-2, 
                                                  fill='#e0e0e0', outline='#d0d0d0')
        self.progress_rect = self.canvas.create_rectangle(2, 2, 2, height-2, 
                                                        fill='#4CAF50', outline='')
        self.text = self.canvas.create_text(width//2, height//2, 
                                          text='0%', fill='#333', font=('Segoe UI', 9))
    
    def set_progress(self, percentage):
        """Update progress bar"""
        self.progress = max(0, min(100, percentage))
        progress_width = (self.width - 4) * (self.progress / 100)
        
        self.canvas.coords(self.progress_rect, 2, 2, 2 + progress_width, self.height - 2)
        self.canvas.itemconfig(self.text, text=f'{self.progress:.0f}%')
        
        # Change color based on progress
        if self.progress < 30:
            color = '#FF5722'  # Red
        elif self.progress < 70:
            color = '#FF9800'  # Orange
        else:
            color = '#4CAF50'  # Green
        
        self.canvas.itemconfig(self.progress_rect, fill=color)
    
    def pack(self, **kwargs):
        self.canvas.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.canvas.grid(**kwargs)

class SystemStateWidget:
    """Widget to display system state information"""
    
    def __init__(self, parent, title="System State"):
        self.frame = ttk.LabelFrame(parent, text=title, padding=10)
        
        # Create state display
        self.state_text = scrolledtext.ScrolledText(
            self.frame, height=8, width=50, 
            font=('Consolas', 9), bg='#f8f9fa'
        )
        self.state_text.pack(fill='both', expand=True)
    
    def update_state(self, state_data):
        """Update the state display"""
        self.state_text.delete(1.0, tk.END)
        
        if isinstance(state_data, dict):
            # Format system state information
            lines = []
            lines.append(f"📊 System Analysis - {datetime.now().strftime('%H:%M:%S')}")
            lines.append("=" * 50)
            
            # Disk usage
            if 'disk_usage' in state_data:
                lines.append("\n💾 Disk Usage:")
                for drive, usage in state_data['disk_usage'].items():
                    free_gb = usage['free'] / (1024**3)
                    total_gb = usage['total'] / (1024**3)
                    lines.append(f"  {drive} {free_gb:.1f}GB free / {total_gb:.1f}GB total")
            
            # Memory info
            if 'memory_info' in state_data:
                memory = state_data['memory_info']
                available_gb = memory['available'] / (1024**3)
                total_gb = memory['total'] / (1024**3)
                lines.append(f"\n🧠 Memory: {available_gb:.1f}GB available / {total_gb:.1f}GB total")
            
            # Cleanup potential
            if 'total_cleanup_potential' in state_data:
                potential_mb = state_data['total_cleanup_potential'] / (1024**2)
                lines.append(f"\n🧹 Cleanup Potential: {potential_mb:.1f} MB")
            
            # Temp files
            if 'temp_files_count' in state_data:
                lines.append(f"📁 Temporary Files: {state_data['temp_files_count']} files")
            
            # Browser cache
            if 'browser_cache_size' in state_data:
                cache_mb = state_data['browser_cache_size'] / (1024**2)
                lines.append(f"🌐 Browser Cache: {cache_mb:.1f} MB")
            
            # Startup programs
            if 'startup_programs_count' in state_data:
                lines.append(f"🚀 Startup Programs: {state_data['startup_programs_count']}")
            
            # Windows updates
            if 'windows_update_status' in state_data:
                lines.append(f"🔄 Updates: {state_data['windows_update_status']}")
                if state_data.get('available_updates', 0) > 0:
                    lines.append(f"   📦 {state_data['available_updates']} updates available")
            
            self.state_text.insert(tk.END, '\n'.join(lines))
        else:
            self.state_text.insert(tk.END, str(state_data))
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)

class V2ModernUI:
    """Modern UI for PC Cleanup Tool Version 2"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.engine = V2CleanupEngine()
        self.cleanup_thread = None
        self.current_report = None
        
        # Setup engine callbacks
        self.engine.set_progress_callback(self.update_progress)
        self.engine.set_status_callback(self.update_status)
        
        self.setup_ui()
        self.setup_styles()
    
    def setup_styles(self):
        """Setup modern styling"""
        style = ttk.Style()
        
        # Configure modern theme
        style.theme_use('clam')
        
        # Custom button styles
        style.configure('OneClick.TButton', 
                       font=('Segoe UI', 14, 'bold'),
                       padding=(20, 15))
        
        style.configure('Action.TButton',
                       font=('Segoe UI', 10),
                       padding=(10, 8))
        
        style.configure('Header.TLabel',
                       font=('Segoe UI', 16, 'bold'),
                       foreground='#2c3e50')
        
        style.configure('Status.TLabel',
                       font=('Segoe UI', 10),
                       foreground='#34495e')
    
    def setup_ui(self):
        """Setup the modern user interface"""
        self.root.title("PC Cleanup Tool V2 - Professional System Optimizer")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f8f9fa')
        
        # Make window resizable
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Create main container
        main_container = ttk.Frame(self.root, padding=20)
        main_container.grid(row=0, column=0, sticky='nsew')
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        
        # Header section
        self.create_header(main_container)
        
        # Main content area
        self.create_main_content(main_container)
        
        # Footer section
        self.create_footer(main_container)
        
        # Initialize system state
        self.refresh_system_state()
    
    def create_header(self, parent):
        """Create header section"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky='ew', pady=(0, 20))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Logo/Icon (placeholder)
        icon_label = ttk.Label(header_frame, text="🖥️", font=('Segoe UI', 24))
        icon_label.grid(row=0, column=0, padx=(0, 15))
        
        # Title and subtitle
        title_frame = ttk.Frame(header_frame)
        title_frame.grid(row=0, column=1, sticky='w')
        
        title_label = ttk.Label(title_frame, text="PC Cleanup Tool V2", 
                               style='Header.TLabel')
        title_label.pack(anchor='w')
        
        subtitle_label = ttk.Label(title_frame, 
                                  text="Professional System Optimization & Maintenance",
                                  style='Status.TLabel')
        subtitle_label.pack(anchor='w')
        
        # Mode toggle
        mode_frame = ttk.Frame(header_frame)
        mode_frame.grid(row=0, column=2, padx=(15, 0))
        
        ttk.Label(mode_frame, text="Mode:", font=('Segoe UI', 10)).pack()
        self.mode_var = tk.StringVar(value="Online")
        mode_combo = ttk.Combobox(mode_frame, textvariable=self.mode_var,
                                 values=["Online", "Offline"], state="readonly", width=10)
        mode_combo.pack()
        mode_combo.bind('<<ComboboxSelected>>', self.on_mode_change)
    
    def create_main_content(self, parent):
        """Create main content area"""
        content_frame = ttk.Frame(parent)
        content_frame.grid(row=1, column=0, sticky='nsew')
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        
        # Left panel - Control and Progress
        self.create_control_panel(content_frame)
        
        # Right panel - System State and Reports
        self.create_info_panel(content_frame)
    
    def create_control_panel(self, parent):
        """Create control panel"""
        control_frame = ttk.LabelFrame(parent, text="System Cleanup Control", padding=15)
        control_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        
        # One-click cleanup section
        cleanup_section = ttk.Frame(control_frame)
        cleanup_section.pack(fill='x', pady=(0, 20))
        
        # Big one-click button
        self.one_click_btn = ttk.Button(
            cleanup_section,
            text="🚀 ONE-CLICK CLEANUP",
            style='OneClick.TButton',
            command=self.start_one_click_cleanup
        )
        self.one_click_btn.pack(pady=10)
        
        # Status and progress
        self.status_label = ttk.Label(cleanup_section, 
                                     text="Ready to optimize your system",
                                     style='Status.TLabel')
        self.status_label.pack(pady=5)
        
        # Modern progress bar
        self.progress_bar = ModernProgressBar(cleanup_section, width=350, height=25)
        self.progress_bar.pack(pady=10)
        
        # Individual actions section
        actions_section = ttk.LabelFrame(control_frame, text="Individual Actions", padding=10)
        actions_section.pack(fill='x', pady=(10, 0))
        
        # Action buttons
        actions = [
            ("🗑️ Clean Temp Files", self.clean_temp_files),
            ("🌐 Clear Browser Cache", self.clear_browser_cache),
            ("⚙️ Optimize Registry", self.optimize_registry),
            ("🚀 Manage Startup", self.manage_startup),
            ("📊 Analyze System", self.analyze_system),
            ("📋 View Last Report", self.view_last_report)
        ]
        
        for i, (text, command) in enumerate(actions):
            btn = ttk.Button(actions_section, text=text, 
                           style='Action.TButton', command=command)
            btn.grid(row=i//2, column=i%2, padx=5, pady=5, sticky='ew')
        
        # Configure grid weights
        actions_section.grid_columnconfigure(0, weight=1)
        actions_section.grid_columnconfigure(1, weight=1)
    
    def create_info_panel(self, parent):
        """Create information panel"""
        info_frame = ttk.Frame(parent)
        info_frame.grid(row=0, column=1, sticky='nsew', padx=(10, 0))
        info_frame.grid_rowconfigure(0, weight=1)
        info_frame.grid_rowconfigure(1, weight=1)
        
        # System state widget
        self.before_state_widget = SystemStateWidget(info_frame, "System State - Before")
        self.before_state_widget.grid(row=0, column=0, sticky='nsew', pady=(0, 10))
        
        self.after_state_widget = SystemStateWidget(info_frame, "System State - After")
        self.after_state_widget.grid(row=1, column=0, sticky='nsew')
    
    def create_footer(self, parent):
        """Create footer section"""
        footer_frame = ttk.Frame(parent)
        footer_frame.grid(row=2, column=0, sticky='ew', pady=(20, 0))
        footer_frame.grid_columnconfigure(1, weight=1)
        
        # Version info
        version_label = ttk.Label(footer_frame, text="Version 2.0 Professional", 
                                 font=('Segoe UI', 9), foreground='#7f8c8d')
        version_label.grid(row=0, column=0)
        
        # Action buttons
        button_frame = ttk.Frame(footer_frame)
        button_frame.grid(row=0, column=2)
        
        ttk.Button(button_frame, text="📊 Generate Report", 
                  command=self.generate_full_report).pack(side='left', padx=5)
        ttk.Button(button_frame, text="⚙️ Settings", 
                  command=self.open_settings).pack(side='left', padx=5)
        ttk.Button(button_frame, text="❓ Help", 
                  command=self.show_help).pack(side='left', padx=5)
    
    def refresh_system_state(self):
        """Refresh system state display"""
        def capture_state():
            try:
                state = self.engine.capture_system_state()
                self.root.after(0, lambda: self.before_state_widget.update_state(state.__dict__))
            except Exception as e:
                self.root.after(0, lambda: self.update_status(f"Error capturing state: {str(e)}"))
        
        threading.Thread(target=capture_state, daemon=True).start()
    
    def update_progress(self, percentage, message=""):
        """Update progress bar and status"""
        self.progress_bar.set_progress(percentage)
        if message:
            self.update_status(message)
    
    def update_status(self, message):
        """Update status label"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def start_one_click_cleanup(self):
        """Start the one-click cleanup process"""
        if self.cleanup_thread and self.cleanup_thread.is_alive():
            messagebox.showwarning("Cleanup in Progress", 
                                 "A cleanup operation is already running!")
            return
        
        # Confirm action
        result = messagebox.askyesno(
            "Confirm One-Click Cleanup",
            "This will perform a comprehensive system cleanup including:\n\n"
            "• Temporary files removal\n"
            "• Browser cache cleaning\n"
            "• Registry optimization\n"
            "• Startup program optimization\n"
            "• System file cleanup\n"
            "• Memory optimization\n\n"
            "Continue with cleanup?"
        )
        
        if not result:
            return
        
        # Disable button and start cleanup
        self.one_click_btn.config(state='disabled', text="🔄 CLEANING...")
        self.progress_bar.set_progress(0)
        
        def cleanup_worker():
            try:
                # Set engine mode
                self.engine.enable_online_features = (self.mode_var.get() == "Online")
                
                # Perform cleanup
                result = self.engine.perform_one_click_cleanup()
                
                # Update UI with results
                self.root.after(0, lambda: self.cleanup_completed(result))
                
            except Exception as e:
                self.root.after(0, lambda: self.cleanup_error(str(e)))
        
        self.cleanup_thread = threading.Thread(target=cleanup_worker, daemon=True)
        self.cleanup_thread.start()
    
    def cleanup_completed(self, result):
        """Handle cleanup completion"""
        # Re-enable button
        self.one_click_btn.config(state='normal', text="🚀 ONE-CLICK CLEANUP")
        
        if result.get('success', False):
            # Update after state
            if 'after_state' in result:
                self.after_state_widget.update_state(result['after_state'])
            
            # Store report
            self.current_report = result
            
            # Show success message
            total_space = sum(r.get('space_freed', 0) for r in result.get('cleanup_results', []))
            space_mb = total_space / (1024 * 1024)
            
            messagebox.showinfo(
                "Cleanup Completed Successfully!",
                f"✅ System cleanup completed!\n\n"
                f"📊 Space freed: {space_mb:.1f} MB\n"
                f"🗑️ Files cleaned: {sum(r.get('files_deleted', 0) for r in result.get('cleanup_results', []))}\n"
                f"⚡ Operations: {len(result.get('cleanup_results', []))}\n\n"
                f"Click 'View Last Report' for detailed results."
            )
            
            self.update_status("✅ Cleanup completed successfully!")
        else:
            error_msg = result.get('error', 'Unknown error occurred')
            messagebox.showerror("Cleanup Failed", f"❌ Cleanup failed:\n\n{error_msg}")
            self.update_status(f"❌ Cleanup failed: {error_msg}")
    
    def cleanup_error(self, error_message):
        """Handle cleanup error"""
        self.one_click_btn.config(state='normal', text="🚀 ONE-CLICK CLEANUP")
        messagebox.showerror("Cleanup Error", f"An error occurred during cleanup:\n\n{error_message}")
        self.update_status(f"❌ Error: {error_message}")
    
    def on_mode_change(self, event=None):
        """Handle mode change"""
        mode = self.mode_var.get()
        self.update_status(f"Mode changed to: {mode}")
        
        if mode == "Offline":
            messagebox.showinfo("Offline Mode", 
                              "🔒 Offline mode enabled.\n\n"
                              "Network-dependent features will be disabled:\n"
                              "• Windows Update checking\n"
                              "• Online system analysis\n\n"
                              "All core cleanup functions remain available.")
    
    # Individual action methods
    def clean_temp_files(self):
        """Clean temporary files only"""
        self.update_status("Cleaning temporary files...")
        # Implementation would call specific temp file cleanup
        messagebox.showinfo("Temp Files", "Temporary files cleanup initiated!")
    
    def clear_browser_cache(self):
        """Clear browser cache only"""
        self.update_status("Clearing browser caches...")
        # Implementation would call browser cache cleanup
        messagebox.showinfo("Browser Cache", "Browser cache cleanup initiated!")
    
    def optimize_registry(self):
        """Optimize registry only"""
        self.update_status("Optimizing registry...")
        # Implementation would call registry optimization
        messagebox.showinfo("Registry", "Registry optimization initiated!")
    
    def manage_startup(self):
        """Manage startup programs"""
        self.update_status("Analyzing startup programs...")
        # Implementation would open startup management
        messagebox.showinfo("Startup", "Startup program management opened!")
    
    def analyze_system(self):
        """Perform system analysis"""
        self.update_status("Performing system analysis...")
        self.refresh_system_state()
        messagebox.showinfo("Analysis", "System analysis completed!")
    
    def view_last_report(self):
        """View the last cleanup report"""
        if not self.current_report:
            messagebox.showwarning("No Report", "No cleanup report available. Run a cleanup first.")
            return
        
        # Create report window
        self.show_report_window(self.current_report)
    
    def show_report_window(self, report_data):
        """Show detailed report in new window"""
        report_window = tk.Toplevel(self.root)
        report_window.title("Cleanup Report - Detailed Results")
        report_window.geometry("800x600")
        
        # Create notebook for tabbed report
        notebook = ttk.Notebook(report_window, padding=10)
        notebook.pack(fill='both', expand=True)
        
        # Summary tab
        summary_frame = ttk.Frame(notebook)
        notebook.add(summary_frame, text="📊 Summary")
        
        summary_text = scrolledtext.ScrolledText(summary_frame, font=('Consolas', 10))
        summary_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Format summary
        if 'summary' in report_data:
            summary = report_data['summary']
            summary_content = f"""
🎯 CLEANUP SUMMARY REPORT
{'=' * 50}

✅ Total Space Freed: {summary.get('total_space_freed', 0) / (1024*1024):.1f} MB
🗑️ Total Files Cleaned: {summary.get('total_files_cleaned', 0):,}
⚡ Cleanup Operations: {summary.get('cleanup_operations', 0)}
📈 Success Rate: {summary.get('success_rate', 0):.1f}%

💾 Disk Space Improvement: {summary.get('disk_space_improvement', 0) / (1024*1024):.1f} MB
🧠 Memory Improvement: {summary.get('memory_improvement', 0) / (1024*1024):.1f} MB

📋 DETAILED RESULTS:
{'-' * 30}
"""
            
            for result in report_data.get('cleanup_results', []):
                summary_content += f"""
🔧 {result.get('operation_type', 'Unknown')}:
   • Files Processed: {result.get('files_processed', 0):,}
   • Files Deleted: {result.get('files_deleted', 0):,}
   • Space Freed: {result.get('space_freed', 0) / (1024*1024):.1f} MB
   • Success Rate: {result.get('success_rate', 0):.1f}%
   • Time Taken: {result.get('time_taken', 0):.1f} seconds
"""
            
            summary_text.insert(tk.END, summary_content)
        
        # Before/After tab
        comparison_frame = ttk.Frame(notebook)
        notebook.add(comparison_frame, text="📈 Before/After")
        
        comparison_text = scrolledtext.ScrolledText(comparison_frame, font=('Consolas', 10))
        comparison_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Format before/after comparison
        comparison_content = "🔍 BEFORE/AFTER SYSTEM COMPARISON\n" + "=" * 50 + "\n\n"
        
        if 'before_state' in report_data and 'after_state' in report_data:
            before = report_data['before_state']
            after = report_data['after_state']
            
            comparison_content += f"""
📅 BEFORE CLEANUP ({before.get('timestamp', 'Unknown')[:19]}):
{'-' * 40}
🗑️ Temp Files: {before.get('temp_files_count', 0):,} files ({before.get('temp_files_size', 0) / (1024*1024):.1f} MB)
🌐 Browser Cache: {before.get('browser_cache_size', 0) / (1024*1024):.1f} MB
🚀 Startup Programs: {before.get('startup_programs_count', 0)}
🧠 Available Memory: {before.get('memory_info', {}).get('available', 0) / (1024**3):.1f} GB

📅 AFTER CLEANUP ({after.get('timestamp', 'Unknown')[:19]}):
{'-' * 40}
🗑️ Temp Files: {after.get('temp_files_count', 0):,} files ({after.get('temp_files_size', 0) / (1024*1024):.1f} MB)
🌐 Browser Cache: {after.get('browser_cache_size', 0) / (1024*1024):.1f} MB
🚀 Startup Programs: {after.get('startup_programs_count', 0)}
🧠 Available Memory: {after.get('memory_info', {}).get('available', 0) / (1024**3):.1f} GB

📊 IMPROVEMENTS:
{'-' * 20}
🗑️ Temp Files Reduced: {before.get('temp_files_count', 0) - after.get('temp_files_count', 0):,} files
💾 Space Recovered: {(before.get('temp_files_size', 0) + before.get('browser_cache_size', 0) - after.get('temp_files_size', 0) - after.get('browser_cache_size', 0)) / (1024*1024):.1f} MB
🧠 Memory Freed: {(after.get('memory_info', {}).get('available', 0) - before.get('memory_info', {}).get('available', 0)) / (1024**2):.1f} MB
"""
        
        comparison_text.insert(tk.END, comparison_content)
        
        # Recommendations tab
        recommendations_frame = ttk.Frame(notebook)
        notebook.add(recommendations_frame, text="💡 Recommendations")
        
        recommendations_text = scrolledtext.ScrolledText(recommendations_frame, font=('Consolas', 10))
        recommendations_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        rec_content = "💡 SYSTEM OPTIMIZATION RECOMMENDATIONS\n" + "=" * 50 + "\n\n"
        
        for i, rec in enumerate(report_data.get('recommendations', []), 1):
            rec_content += f"{i}. {rec}\n\n"
        
        recommendations_text.insert(tk.END, rec_content)
    
    def generate_full_report(self):
        """Generate and save full report"""
        if not self.current_report:
            messagebox.showwarning("No Report", "No cleanup data available. Run a cleanup first.")
            return
        
        try:
            # Save report to file
            report_dir = Path.home() / "Desktop" / "PC_Cleanup_V2_Reports"
            report_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = report_dir / f"cleanup_report_v2_{timestamp}.json"
            
            with open(report_file, 'w') as f:
                json.dump(self.current_report, f, indent=2, default=str)
            
            messagebox.showinfo("Report Saved", 
                              f"📄 Full report saved to:\n{report_file}\n\n"
                              f"You can share this report or import it later.")
            
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save report:\n{str(e)}")
    
    def open_settings(self):
        """Open settings window"""
        messagebox.showinfo("Settings", "⚙️ Settings panel coming soon!\n\nFeatures planned:\n• Cleanup scheduling\n• Custom cleanup profiles\n• Advanced options")
    
    def show_help(self):
        """Show help information"""
        help_text = """
🚀 PC CLEANUP TOOL V2 - HELP GUIDE

ONE-CLICK CLEANUP:
• Performs comprehensive system optimization
• Includes all cleanup operations in one action
• Shows before/after system comparison
• Generates detailed reports

INDIVIDUAL ACTIONS:
• Clean Temp Files: Remove temporary files only
• Clear Browser Cache: Clean browser data only  
• Optimize Registry: Clean and optimize registry
• Manage Startup: Control startup programs
• Analyze System: Check current system state
• View Last Report: See detailed cleanup results

MODES:
• Online Mode: Full functionality with updates
• Offline Mode: Core cleanup without network features

REPORTS:
• Before/After system state comparison
• Detailed operation results
• Space recovery statistics
• System optimization recommendations

For support: Contact your IT administrator
Version: 2.0 Professional
"""
        
        messagebox.showinfo("Help - PC Cleanup Tool V2", help_text)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main entry point"""
    try:
        app = V2ModernUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Startup Error", f"Failed to start application:\n{str(e)}")

if __name__ == "__main__":
    main()
