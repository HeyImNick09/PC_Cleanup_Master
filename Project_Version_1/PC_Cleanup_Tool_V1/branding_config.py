"""
Branding and Customization System for PC Cleanup Tool
Easy white-label customization for business deployment

This module allows complete customization of:
- Company branding and logos
- Color schemes and themes
- Contact information
- Feature sets and pricing tiers
"""

import json
import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
from pathlib import Path
from typing import Dict, Any
import os

class BrandingManager:
    """
    Professional branding management system for white-label deployment
    """
    
    def __init__(self):
        self.config_file = Path("branding_config.json")
        self.default_config = {
            "company_info": {
                "name": "Nick P - IT Solutions",
                "website": "https://your-website.com",
                "support_email": "support@your-domain.com",
                "phone": "+1 (555) 123-4567",
                "address": "Your Business Address"
            },
            "application": {
                "title": "Nick's PC Optimization Suite",
                "subtitle": "Professional System Maintenance Tool",
                "version": "1.0.0",
                "description": "Industry-standard PC cleanup and optimization utility"
            },
            "colors": {
                "primary": "#2E86AB",
                "secondary": "#A23B72", 
                "success": "#F18F01",
                "background": "#F5F5F5",
                "card_bg": "#FFFFFF",
                "text_primary": "#2C3E50",
                "text_secondary": "#7F8C8D"
            },
            "features": {
                "temp_cleanup": True,
                "browser_cleanup": True,
                "registry_cleanup": True,
                "startup_optimization": True,
                "disk_analysis": True,
                "system_monitoring": True,
                "scheduled_maintenance": False,  # Premium feature
                "network_cleanup": False,       # Premium feature
                "advanced_reporting": False     # Premium feature
            },
            "pricing_tier": "professional",  # basic, professional, enterprise
            "custom_logo": "",
            "custom_icon": "",
            "license_key": "",
            "deployment_id": ""
        }
        
        self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load branding configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    self.config = {**self.default_config, **loaded_config}
            except (json.JSONDecodeError, FileNotFoundError):
                self.config = self.default_config.copy()
        else:
            self.config = self.default_config.copy()
        
        return self.config
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get_company_info(self) -> Dict[str, str]:
        """Get company information"""
        return self.config["company_info"]
    
    def get_application_info(self) -> Dict[str, str]:
        """Get application branding information"""
        return self.config["application"]
    
    def get_color_scheme(self) -> Dict[str, str]:
        """Get current color scheme"""
        return self.config["colors"]
    
    def get_enabled_features(self) -> Dict[str, bool]:
        """Get enabled features based on pricing tier"""
        return self.config["features"]
    
    def update_company_info(self, **kwargs):
        """Update company information"""
        self.config["company_info"].update(kwargs)
        self.save_config()
    
    def update_application_info(self, **kwargs):
        """Update application branding"""
        self.config["application"].update(kwargs)
        self.save_config()
    
    def update_colors(self, **kwargs):
        """Update color scheme"""
        self.config["colors"].update(kwargs)
        self.save_config()
    
    def set_pricing_tier(self, tier: str):
        """Set pricing tier and update available features"""
        tier_features = {
            "basic": {
                "temp_cleanup": True,
                "browser_cleanup": True,
                "registry_cleanup": False,
                "startup_optimization": False,
                "disk_analysis": False,
                "system_monitoring": False,
                "scheduled_maintenance": False,
                "network_cleanup": False,
                "advanced_reporting": False
            },
            "professional": {
                "temp_cleanup": True,
                "browser_cleanup": True,
                "registry_cleanup": True,
                "startup_optimization": True,
                "disk_analysis": True,
                "system_monitoring": True,
                "scheduled_maintenance": False,
                "network_cleanup": False,
                "advanced_reporting": False
            },
            "enterprise": {
                "temp_cleanup": True,
                "browser_cleanup": True,
                "registry_cleanup": True,
                "startup_optimization": True,
                "disk_analysis": True,
                "system_monitoring": True,
                "scheduled_maintenance": True,
                "network_cleanup": True,
                "advanced_reporting": True
            }
        }
        
        if tier in tier_features:
            self.config["pricing_tier"] = tier
            self.config["features"] = tier_features[tier]
            self.save_config()
    
    def create_branded_executable_name(self) -> str:
        """Generate branded executable name"""
        company = self.config["company_info"]["name"].replace(" ", "").replace("-", "")
        app_name = self.config["application"]["title"].replace(" ", "").replace("'", "")
        return f"{company}_{app_name}.exe"


class BrandingConfiguratorGUI:
    """
    GUI tool for easy branding configuration
    """
    
    def __init__(self):
        self.branding_manager = BrandingManager()
        self.root = tk.Tk()
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the branding configurator GUI"""
        self.root.title("PC Cleanup Tool - Branding Configurator")
        self.root.geometry("800x600")
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Company Info Tab
        self.create_company_tab(notebook)
        
        # Application Branding Tab
        self.create_application_tab(notebook)
        
        # Color Scheme Tab
        self.create_colors_tab(notebook)
        
        # Features Tab
        self.create_features_tab(notebook)
        
        # Preview Tab
        self.create_preview_tab(notebook)
        
        # Save/Load buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="Save Configuration", command=self.save_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Load Configuration", command=self.load_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset to Defaults", command=self.reset_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Generate Build", command=self.generate_build).pack(side=tk.RIGHT, padx=5)
    
    def create_company_tab(self, notebook):
        """Create company information tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Company Info")
        
        # Company name
        ttk.Label(frame, text="Company Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.company_name = tk.StringVar(value=self.branding_manager.config["company_info"]["name"])
        ttk.Entry(frame, textvariable=self.company_name, width=50).grid(row=0, column=1, padx=5, pady=5)
        
        # Website
        ttk.Label(frame, text="Website:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.website = tk.StringVar(value=self.branding_manager.config["company_info"]["website"])
        ttk.Entry(frame, textvariable=self.website, width=50).grid(row=1, column=1, padx=5, pady=5)
        
        # Support email
        ttk.Label(frame, text="Support Email:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.support_email = tk.StringVar(value=self.branding_manager.config["company_info"]["support_email"])
        ttk.Entry(frame, textvariable=self.support_email, width=50).grid(row=2, column=1, padx=5, pady=5)
        
        # Phone
        ttk.Label(frame, text="Phone:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.phone = tk.StringVar(value=self.branding_manager.config["company_info"]["phone"])
        ttk.Entry(frame, textvariable=self.phone, width=50).grid(row=3, column=1, padx=5, pady=5)
        
        # Address
        ttk.Label(frame, text="Address:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.address = tk.StringVar(value=self.branding_manager.config["company_info"]["address"])
        ttk.Entry(frame, textvariable=self.address, width=50).grid(row=4, column=1, padx=5, pady=5)
    
    def create_application_tab(self, notebook):
        """Create application branding tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Application")
        
        # Application title
        ttk.Label(frame, text="Application Title:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.app_title = tk.StringVar(value=self.branding_manager.config["application"]["title"])
        ttk.Entry(frame, textvariable=self.app_title, width=50).grid(row=0, column=1, padx=5, pady=5)
        
        # Subtitle
        ttk.Label(frame, text="Subtitle:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.app_subtitle = tk.StringVar(value=self.branding_manager.config["application"]["subtitle"])
        ttk.Entry(frame, textvariable=self.app_subtitle, width=50).grid(row=1, column=1, padx=5, pady=5)
        
        # Version
        ttk.Label(frame, text="Version:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.app_version = tk.StringVar(value=self.branding_manager.config["application"]["version"])
        ttk.Entry(frame, textvariable=self.app_version, width=50).grid(row=2, column=1, padx=5, pady=5)
        
        # Description
        ttk.Label(frame, text="Description:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.app_description = tk.StringVar(value=self.branding_manager.config["application"]["description"])
        ttk.Entry(frame, textvariable=self.app_description, width=50).grid(row=3, column=1, padx=5, pady=5)
    
    def create_colors_tab(self, notebook):
        """Create color scheme tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Colors")
        
        self.color_vars = {}
        colors = self.branding_manager.config["colors"]
        
        row = 0
        for color_name, color_value in colors.items():
            ttk.Label(frame, text=f"{color_name.replace('_', ' ').title()}:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
            
            # Color preview
            color_frame = tk.Frame(frame, bg=color_value, width=30, height=20, relief=tk.RAISED, bd=1)
            color_frame.grid(row=row, column=1, padx=5, pady=5)
            
            # Color value entry
            self.color_vars[color_name] = tk.StringVar(value=color_value)
            entry = ttk.Entry(frame, textvariable=self.color_vars[color_name], width=10)
            entry.grid(row=row, column=2, padx=5, pady=5)
            
            # Color picker button
            ttk.Button(frame, text="Pick", command=lambda cn=color_name, cf=color_frame: self.pick_color(cn, cf)).grid(row=row, column=3, padx=5, pady=5)
            
            row += 1
    
    def create_features_tab(self, notebook):
        """Create features configuration tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Features")
        
        # Pricing tier selection
        ttk.Label(frame, text="Pricing Tier:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.pricing_tier = tk.StringVar(value=self.branding_manager.config["pricing_tier"])
        tier_combo = ttk.Combobox(frame, textvariable=self.pricing_tier, values=["basic", "professional", "enterprise"])
        tier_combo.grid(row=0, column=1, padx=5, pady=5)
        tier_combo.bind('<<ComboboxSelected>>', self.update_features_for_tier)
        
        # Feature checkboxes
        self.feature_vars = {}
        features = self.branding_manager.config["features"]
        
        row = 2
        ttk.Label(frame, text="Available Features:", font=('TkDefaultFont', 10, 'bold')).grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=5, pady=(10, 5))
        
        for feature_name, enabled in features.items():
            self.feature_vars[feature_name] = tk.BooleanVar(value=enabled)
            cb = ttk.Checkbutton(frame, text=feature_name.replace('_', ' ').title(), variable=self.feature_vars[feature_name])
            cb.grid(row=row, column=0, columnspan=2, sticky=tk.W, padx=20, pady=2)
            row += 1
    
    def create_preview_tab(self, notebook):
        """Create preview tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Preview")
        
        # Preview area
        preview_text = tk.Text(frame, height=25, width=80)
        preview_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.preview_text = preview_text
        self.update_preview()
        
        # Update preview button
        ttk.Button(frame, text="Update Preview", command=self.update_preview).pack(pady=5)
    
    def pick_color(self, color_name, color_frame):
        """Open color picker dialog"""
        color = colorchooser.askcolor(initialcolor=self.color_vars[color_name].get())[1]
        if color:
            self.color_vars[color_name].set(color)
            color_frame.configure(bg=color)
    
    def update_features_for_tier(self, event=None):
        """Update features based on selected pricing tier"""
        tier = self.pricing_tier.get()
        self.branding_manager.set_pricing_tier(tier)
        
        # Update checkboxes
        for feature_name, var in self.feature_vars.items():
            var.set(self.branding_manager.config["features"][feature_name])
    
    def update_preview(self):
        """Update the preview text"""
        config = self.get_current_config()
        
        preview_content = f"""
BRANDING CONFIGURATION PREVIEW
{'=' * 50}

COMPANY INFORMATION:
Name: {config['company_info']['name']}
Website: {config['company_info']['website']}
Support Email: {config['company_info']['support_email']}
Phone: {config['company_info']['phone']}
Address: {config['company_info']['address']}

APPLICATION BRANDING:
Title: {config['application']['title']}
Subtitle: {config['application']['subtitle']}
Version: {config['application']['version']}
Description: {config['application']['description']}

COLOR SCHEME:
Primary: {config['colors']['primary']}
Secondary: {config['colors']['secondary']}
Success: {config['colors']['success']}
Background: {config['colors']['background']}
Card Background: {config['colors']['card_bg']}
Primary Text: {config['colors']['text_primary']}
Secondary Text: {config['colors']['text_secondary']}

PRICING TIER: {config['pricing_tier'].upper()}

ENABLED FEATURES:
"""
        
        for feature, enabled in config['features'].items():
            status = "✓" if enabled else "✗"
            preview_content += f"{status} {feature.replace('_', ' ').title()}\n"
        
        preview_content += f"""

EXECUTABLE NAME: {self.branding_manager.create_branded_executable_name()}

DEPLOYMENT READY: {'Yes' if self.validate_config(config) else 'No - Missing required fields'}
"""
        
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(1.0, preview_content)
    
    def get_current_config(self):
        """Get current configuration from GUI"""
        config = self.branding_manager.config.copy()
        
        # Update from GUI fields
        config['company_info']['name'] = self.company_name.get()
        config['company_info']['website'] = self.website.get()
        config['company_info']['support_email'] = self.support_email.get()
        config['company_info']['phone'] = self.phone.get()
        config['company_info']['address'] = self.address.get()
        
        config['application']['title'] = self.app_title.get()
        config['application']['subtitle'] = self.app_subtitle.get()
        config['application']['version'] = self.app_version.get()
        config['application']['description'] = self.app_description.get()
        
        for color_name, var in self.color_vars.items():
            config['colors'][color_name] = var.get()
        
        config['pricing_tier'] = self.pricing_tier.get()
        
        for feature_name, var in self.feature_vars.items():
            config['features'][feature_name] = var.get()
        
        return config
    
    def validate_config(self, config):
        """Validate configuration completeness"""
        required_fields = [
            config['company_info']['name'],
            config['application']['title'],
            config['application']['version']
        ]
        return all(field.strip() for field in required_fields)
    
    def save_config(self):
        """Save current configuration"""
        config = self.get_current_config()
        self.branding_manager.config = config
        
        if self.branding_manager.save_config():
            messagebox.showinfo("Success", "Configuration saved successfully!")
            self.update_preview()
        else:
            messagebox.showerror("Error", "Failed to save configuration!")
    
    def load_config(self):
        """Load configuration from file"""
        file_path = filedialog.askopenfilename(
            title="Load Branding Configuration",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    config = json.load(f)
                
                self.branding_manager.config = {**self.branding_manager.default_config, **config}
                self.refresh_gui()
                messagebox.showinfo("Success", "Configuration loaded successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load configuration: {e}")
    
    def reset_config(self):
        """Reset to default configuration"""
        if messagebox.askyesno("Confirm Reset", "Reset all settings to defaults?"):
            self.branding_manager.config = self.branding_manager.default_config.copy()
            self.refresh_gui()
    
    def refresh_gui(self):
        """Refresh GUI with current configuration"""
        config = self.branding_manager.config
        
        self.company_name.set(config['company_info']['name'])
        self.website.set(config['company_info']['website'])
        self.support_email.set(config['company_info']['support_email'])
        self.phone.set(config['company_info']['phone'])
        self.address.set(config['company_info']['address'])
        
        self.app_title.set(config['application']['title'])
        self.app_subtitle.set(config['application']['subtitle'])
        self.app_version.set(config['application']['version'])
        self.app_description.set(config['application']['description'])
        
        for color_name, var in self.color_vars.items():
            var.set(config['colors'][color_name])
        
        self.pricing_tier.set(config['pricing_tier'])
        
        for feature_name, var in self.feature_vars.items():
            var.set(config['features'][feature_name])
        
        self.update_preview()
    
    def generate_build(self):
        """Generate branded build"""
        config = self.get_current_config()
        
        if not self.validate_config(config):
            messagebox.showerror("Error", "Please fill in all required fields before generating build!")
            return
        
        # Save current config
        self.branding_manager.config = config
        self.branding_manager.save_config()
        
        messagebox.showinfo("Build Ready", 
                          f"Configuration saved! Ready to build:\n\n"
                          f"Executable: {self.branding_manager.create_branded_executable_name()}\n"
                          f"Company: {config['company_info']['name']}\n"
                          f"Application: {config['application']['title']}\n\n"
                          f"Run build_config.py to create the executable.")
    
    def run(self):
        """Start the branding configurator"""
        self.root.mainloop()


def main():
    """Main entry point for branding configurator"""
    app = BrandingConfiguratorGUI()
    app.run()


if __name__ == "__main__":
    main()
