import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import glob

def get_meeting_notes(meeting_dir: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
    """
    Get meeting notes for a project within an optional date range.
    
    Args:
        meeting_dir: Path to the meeting notes directory
        start_date: Optional start date filter
        end_date: Optional end date filter
        
    Returns:
        List of meeting notes with metadata
    """
    
    meeting_notes = []
    
    if not os.path.exists(meeting_dir):
        return []
    
    # Get all markdown files in the meeting directory
    files = glob.glob(os.path.join(meeting_dir, "*.md"))
    
    for file_path in files:
        try:
            # Get file modification time as a proxy for meeting date
            file_stat = os.stat(file_path)
            file_date = datetime.fromtimestamp(file_stat.st_mtime)
            
            # Apply date filters if provided
            if start_date and file_date < start_date:
                continue
            if end_date and file_date > end_date:
                continue
            
            # Read the meeting notes
            with open(file_path, 'r') as f:
                content = f.read()
            
            meeting_notes.append({
                'file_path': file_path,
                'file_name': os.path.basename(file_path),
                'date': file_date,
                'content': content
            })
            
        except Exception as e:
            # Skip files that can't be read
            continue
    
    # Sort by date (newest first)
    meeting_notes.sort(key=lambda x: x['date'], reverse=True)
    
    return meeting_notes