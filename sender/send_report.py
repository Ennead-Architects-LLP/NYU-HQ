#!/usr/bin/env python
"""
HTML Report Sender
Sends the latest HTML report and associated files (CSS, JS, JSON, images) from local folder to GitHub repository.
"""

import os
import sys
import base64
import json
from pathlib import Path
import urllib.request
import urllib.error
from datetime import datetime
import ctypes
import mimetypes


def get_script_dir():
    """Gets the directory where this script/exe is located."""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        return Path(sys.executable).parent
    else:
        # Running as script
        return Path(__file__).parent


def read_config():
    """Reads configuration from config.json file."""
    script_dir = get_script_dir()
    config_file = script_dir / "config.json"
    
    if not config_file.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_file}\n"
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
        raise ValueError(f"Invalid JSON in config.json: {e}")


def get_reports_folder():
    """Constructs the reports folder path using the current Windows username."""
    username = os.getenv('USERNAME')
    if not username:
        raise EnvironmentError("Could not detect Windows USERNAME environment variable")
    
    reports_path = (
        f"C:\\Users\\{username}\\Documents\\EnneadTab Ecosystem\\EA_Dist\\Apps\\_revit\\"
        f"EnneaDuck.extension\\EnneadTab Tailor.tab\\Proj. 2534.panel\\"
        f"NYU HQ.pulldown\\monitor_area.pushbutton\\reports"
    )
    
    return Path(reports_path)


def find_report_files(reports_folder):
    """Finds all report files (HTML, CSS, JS, JSON, images) in the reports folder.
    
    Returns:
        tuple: (latest_html_file, other_files_list)
            - latest_html_file: Path to the most recent HTML file (will become index.html)
            - other_files_list: List of other supporting files (CSS, JS, JSON, PNG, JPG)
    """
    if not reports_folder.exists():
        raise FileNotFoundError(f"Reports folder not found: {reports_folder}")
    
    # Find HTML files
    html_files = list(reports_folder.glob("*.html"))
    
    if not html_files:
        raise FileNotFoundError(f"No HTML files found in {reports_folder}")
    
    # Get the latest HTML file by modification time
    latest_html = max(html_files, key=lambda f: f.stat().st_mtime)
    
    # Find supporting files (CSS, JS, JSON, images)
    supporting_extensions = ['.css', '.js', '.json', '.png', '.jpg', '.jpeg']
    supporting_files = []
    for ext in supporting_extensions:
        files = list(reports_folder.glob(f"*{ext}"))
        supporting_files.extend(files)
    
    # Sort supporting files by modification time for display
    supporting_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    
    return latest_html, supporting_files


def read_file_content(file_path):
    """Reads a file and returns its content."""
    try:
        # Try UTF-8 first (for text files)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content, 'text'
    except UnicodeDecodeError:
        # If UTF-8 fails, read as binary
        with open(file_path, 'rb') as f:
            content = f.read()
        return content, 'binary'
    except Exception as e:
        raise IOError(f"Error reading file {file_path}: {e}")


def get_file_sha(config, file_path):
    """Gets the SHA of the current file in the repository."""
    token = config['github_token']
    repo_owner = config['repo_owner']
    repo_name = config['repo_name']
    
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'NYU-HQ-Report-Sender'
    }
    
    try:
        req = urllib.request.Request(url, headers=headers, method='GET')
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('sha')
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None  # File doesn't exist yet
        raise


def update_github_file(file_path, content, content_type, config, file_number, total_files, target_name=None):
    """Updates a single file on GitHub using the Contents API.
    
    Args:
        file_path: Local file path
        content: File content
        content_type: 'text' or 'binary'
        config: Configuration dict
        file_number: Current file number for progress display
        total_files: Total number of files
        target_name: Optional target filename (if None, uses original name)
    """
    token = config['github_token']
    repo_owner = config['repo_owner']
    repo_name = config['repo_name']
    
    # Use target_name if provided, otherwise use original filename
    filename = target_name if target_name else file_path.name
    github_path = f"docs/{filename}"
    
    # Show what we're uploading
    if target_name and target_name != file_path.name:
        print(f"\n   [{file_number}/{total_files}] {file_path.name} → {target_name}")
    else:
        print(f"\n   [{file_number}/{total_files}] {file_path.name}")
    
    # Get current file SHA (needed for update)
    sha = get_file_sha(config, github_path)
    
    # Encode content as base64
    if content_type == 'text':
        content_base64 = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    else:
        content_base64 = base64.b64encode(content).decode('utf-8')
    
    # Prepare the request
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    commit_message = f"Update {github_path} - {timestamp}"
    
    payload = {
        'message': commit_message,
        'content': content_base64,
        'branch': 'main'
    }
    
    if sha:
        payload['sha'] = sha
    
    data = json.dumps(payload).encode('utf-8')
    
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{github_path}"
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json',
        'User-Agent': 'NYU-HQ-Report-Sender'
    }
    
    try:
        req = urllib.request.Request(url, data=data, headers=headers, method='PUT')
        with urllib.request.urlopen(req, timeout=30) as response:
            if response.status in [200, 201]:
                result = json.loads(response.read().decode('utf-8'))
                print(f"      ✓ SUCCESS - Commit: {result['commit']['sha'][:7]}")
                return True, None
            else:
                response_body = response.read().decode('utf-8')
                error_msg = f"Unexpected response code: {response.status}"
                print(f"      ✕ FAILED - {error_msg}")
                return False, error_msg
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        error_msg = f"HTTP Error {e.code}: {e.reason}"
        print(f"      ✕ FAILED - {error_msg}")
        return False, error_msg
    except urllib.error.URLError as e:
        error_msg = f"Network error: {e.reason}"
        print(f"      ✕ FAILED - {error_msg}")
        return False, error_msg
    except Exception as e:
        error_msg = f"Unexpected error: {e}"
        print(f"      ✕ FAILED - {error_msg}")
        return False, error_msg


def update_all_files(latest_html, supporting_files, config):
    """Updates all report files on GitHub.
    
    Args:
        latest_html: Path to the latest HTML file (will be uploaded as index.html)
        supporting_files: List of supporting files (CSS, JS, JSON) to upload with original names
        config: Configuration dict
    """
    total_files = 1 + len(supporting_files)  # HTML + supporting files
    
    print(f"\nUploading {total_files} file(s) to GitHub...")
    print(f"Repository: {config['repo_owner']}/{config['repo_name']}")
    print(f"Target folder: docs/")
    
    success_count = 0
    failed_files = []
    current_file = 0
    
    # Upload the latest HTML as index.html
    current_file += 1
    try:
        content, content_type = read_file_content(latest_html)
        success, error = update_github_file(
            latest_html, content, content_type, config, 
            current_file, total_files, target_name="index.html"
        )
        
        if success:
            success_count += 1
        else:
            failed_files.append(("index.html (from " + latest_html.name + ")", error))
            
    except Exception as e:
        error_msg = str(e)
        print(f"\n   [{current_file}/{total_files}] {latest_html.name} → index.html")
        print(f"      ✕ FAILED - {error_msg}")
        failed_files.append(("index.html (from " + latest_html.name + ")", error_msg))
    
    # Upload supporting files with their original names
    for file_path in supporting_files:
        current_file += 1
        try:
            content, content_type = read_file_content(file_path)
            success, error = update_github_file(
                file_path, content, content_type, config, 
                current_file, total_files
            )
            
            if success:
                success_count += 1
            else:
                failed_files.append((file_path.name, error))
                
        except Exception as e:
            error_msg = str(e)
            print(f"\n   [{current_file}/{total_files}] {file_path.name}")
            print(f"      ✕ FAILED - {error_msg}")
            failed_files.append((file_path.name, error_msg))
    
    # Summary
    print(f"\n{'='*60}")
    if success_count == total_files:
        print(f"✓ ALL {success_count} FILE(S) UPLOADED SUCCESSFULLY!")
    else:
        print(f"PARTIAL SUCCESS: {success_count}/{total_files} file(s) uploaded")
        if failed_files:
            print(f"\nFailed files:")
            for filename, error in failed_files:
                print(f"  ✕ {filename}: {error}")
    print(f"{'='*60}")
    
    return success_count == total_files, success_count, failed_files


def show_notification(title, message, icon_type=0):
    """Placeholder for notifications (disabled for silent operation)."""
    pass  # Completely silent - no popups


def main():
    """Main execution function."""
    is_frozen = getattr(sys, 'frozen', False)
    
    if not is_frozen:
        print("=" * 60)
        print("Multi-File Report Sender")
        print("Supports: HTML, CSS, JS, JSON, Images (PNG/JPG)")
        print("=" * 60)
    
    try:
        # Step 1: Read configuration
        if not is_frozen:
            print("\n1. Reading configuration...")
        config = read_config()
        if not is_frozen:
            print(f"   Repository: {config['repo_owner']}/{config['repo_name']}")
        
        # Step 2: Get reports folder path
        if not is_frozen:
            print("\n2. Locating reports folder...")
        reports_folder = get_reports_folder()
        if not is_frozen:
            print(f"   Reports folder: {reports_folder}")
        
        # Step 3: Find all report files
        if not is_frozen:
            print("\n3. Finding report files (HTML, CSS, JS, JSON, images)...")
        latest_html, supporting_files = find_report_files(reports_folder)
        
        if not is_frozen:
            # Show the HTML file that will become index.html
            html_mod_time = datetime.fromtimestamp(latest_html.stat().st_mtime)
            html_size = latest_html.stat().st_size
            print(f"   Latest HTML (→ index.html):")
            print(f"      • {latest_html.name} ({html_size:,} bytes, modified: {html_mod_time.strftime('%Y-%m-%d %H:%M:%S')})")
            
            # Show supporting files
            if supporting_files:
                print(f"   Supporting files ({len(supporting_files)}):")
                for file in supporting_files:
                    mod_time = datetime.fromtimestamp(file.stat().st_mtime)
                    file_size = file.stat().st_size
                    print(f"      • {file.name} ({file_size:,} bytes, modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')})")
            else:
                print(f"   Supporting files: None found")
        
        # Step 4: Upload all files to GitHub
        if not is_frozen:
            print("\n4. Updating GitHub repository...")
        success, success_count, failed_files = update_all_files(latest_html, supporting_files, config)
        
        total_files = 1 + len(supporting_files)  # HTML + supporting files
        
        if success:
            if not is_frozen:
                print("\nSUCCESS! All report files have been updated in the repository.")
            else:
                # Show success notification when running as exe
                show_notification(
                    "NYU-HQ Report Sender",
                    f"Successfully uploaded {success_count} file(s) to GitHub Pages",
                    1  # Info icon
                )
            return 0
        else:
            if not is_frozen:
                print(f"\nPARTIAL SUCCESS: {success_count}/{total_files} file(s) uploaded.")
                print("Please check the error messages above.")
            else:
                show_notification(
                    "NYU-HQ Report Sender - Partial Success",
                    f"Uploaded {success_count}/{total_files} file(s).\nSome files failed to upload.",
                    2  # Warning icon
                )
            return 1
            
    except Exception as e:
        if not is_frozen:
            print(f"\n[ERROR] {e}")
            print("\n" + "=" * 60)
            print("FAILED!")
            print("=" * 60)
        else:
            show_notification(
                "NYU-HQ Report Sender - Error",
                f"Error: {str(e)[:200]}",
                3  # Error icon
            )
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
