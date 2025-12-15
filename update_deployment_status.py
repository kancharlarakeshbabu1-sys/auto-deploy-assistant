#!/usr/bin/env python3
"""
Update Airtable Deployment Status after GitHub Actions completes
"""

import os
import sys
import time
from pyairtable import Api
from datetime import datetime

def find_deployment_record(table, commit_sha, max_attempts=6, wait_seconds=10):
    """
    Find the deployment record by timestamp (most recent within last 5 minutes)
    
    Args:
        table: Airtable table object
        commit_sha: Commit SHA (for logging only)
        max_attempts: Number of retry attempts
        wait_seconds: Seconds to wait between attempts
    """
    
    from datetime import datetime, timedelta
    import time
    
    short_sha = commit_sha[:7]
    
    for attempt in range(1, max_attempts + 1):
        print(f"Attempt {attempt}/{max_attempts}: Looking for recent deployment...")
        
        # Get all records
        all_records = table.all()
        
        if not all_records:
            print("  No records found")
            if attempt < max_attempts:
                print(f"  Waiting {wait_seconds} seconds for Zapier...")
                time.sleep(wait_seconds)
                continue
            return None
        
        # Sort by created time (most recent first)
        sorted_records = sorted(
            all_records,
            key=lambda x: x['createdTime'],
            reverse=True
        )
        
        # Get the most recent record (created in last 2 minutes)
        most_recent = sorted_records[0]
        created_time = datetime.fromisoformat(most_recent['createdTime'].replace('Z', '+00:00'))
        now = datetime.now(created_time.tzinfo)
        age_seconds = (now - created_time).total_seconds()
        
        print(f"  Most recent record age: {age_seconds:.1f} seconds")
        print(f"  Record ID: {most_recent['id']}")
        
        # If record is less than 5 minutes old, it's probably ours
        if age_seconds < 300:  
            print(f"  Found recent record (created {age_seconds:.1f}s ago)")
            return most_recent
        
        # Wait and retry
        if attempt < max_attempts:
            print(f"  No recent record found, waiting {wait_seconds} seconds...")
            time.sleep(wait_seconds)
    
    print("WARNING: Could not find recent deployment record")
    return None


def update_deployment_status(status, commit_sha):
    """
    Update the deployment record in Airtable with build status
    
    Args:
        status: "Success" or "Failed"
        commit_sha: The commit SHA to find the record
    """
    
    api_key = os.getenv('AIRTABLE_API_KEY')
    base_id = os.getenv('AIRTABLE_BASE_ID')
    table_id = os.getenv('AIRTABLE_DEPLOYMENTS_TABLE_ID')
    
    if not all([api_key, base_id, table_id]):
        print("ERROR: Missing Airtable credentials")
        return False
    
    try:
        # Initialize Airtable API
        api = Api(api_key)
        table = api.table(base_id, table_id)
        
        # Find the record with retries
        target_record = find_deployment_record(table, commit_sha)
        
        if not target_record:
            print("ERROR: Could not find deployment record")
            return False
        
        # Update the record
        record_id = target_record['id']
        
        table.update(record_id, {'Build Status': status})
        
        print(f"\n✓ Successfully updated deployment status to: {status}")
        print(f"  Record ID: {record_id}")
        print(f"  Commit SHA: {commit_sha[:7]}")
        
        return True
        
    except Exception as e:
        print(f"ERROR updating Airtable: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python update_deployment_status.py <status> <commit_sha>")
        sys.exit(1)
    
    status = sys.argv[1]
    commit_sha = sys.argv[2]
    
    if status not in ["Success", "Failed"]:
        print(f"ERROR: Invalid status '{status}'")
        sys.exit(1)
    
    success = update_deployment_status(status, commit_sha)
    sys.exit(0 if success else 1)