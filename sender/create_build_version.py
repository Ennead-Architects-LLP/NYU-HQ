#!/usr/bin/env python
"""
Creates a build version of send_report.py with embedded configuration.
This script is used by build.bat to embed the config into the compiled .exe.
"""

import json
from pathlib import Path

def create_build_version():
    """Creates send_report_build.py with embedded configuration."""
    
    # Read the config
    config_file = Path("config.json")
    if not config_file.exists():
        raise FileNotFoundError("config.json not found")
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    # Read the template
    template_file = Path("send_report.py")
    with open(template_file, 'r', encoding='utf-8') as f:
        template_code = f.read()
    
    # Create the embedded config code
    embedded_config = f'''{{
    "github_token": "{config['github_token']}",
    "repo_owner": "{config['repo_owner']}",
    "repo_name": "{config['repo_name']}"
}}'''
    
    # Replace the read_config function to return embedded config
    old_function = '''def read_config():
    """Reads configuration from config.json file."""
    script_dir = get_script_dir()
    config_file = script_dir / "config.json"
    
    if not config_file.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_file}\\n"
            f"Please create config.json with your GitHub token and repository info."
        )
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        required_fields = ['github_token', 'repo_owner', 'repo_name']
        missing = [field for field in required_fields if field not in config]
        if missing:
            raise ValueError(f"Missing required fields in config.json: {', '.join(missing)}")
        
        return config
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config.json: {e}")'''
    
    new_function = f'''def read_config():
    """Returns embedded configuration."""
    # Configuration embedded at build time
    config_json = """{embedded_config}"""
    config = json.loads(config_json)
    return config'''
    
    # Replace in the template
    build_code = template_code.replace(old_function, new_function)
    
    # Write the build version
    build_file = Path("send_report_build.py")
    with open(build_file, 'w', encoding='utf-8') as f:
        f.write(build_code)
    
    print(f"Created {build_file} with embedded configuration")
    print(f"Repository: {config['repo_owner']}/{config['repo_name']}")

if __name__ == "__main__":
    try:
        create_build_version()
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

