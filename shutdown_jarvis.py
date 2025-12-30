#!/usr/bin/env python3
"""
JARVIS Shutdown Script - Properly close all JARVIS processes
"""

import psutil
import os
import sys
import json
import signal
import time
from datetime import datetime

def find_jarvis_processes():
    """Find all JARVIS related processes"""
    jarvis_processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
            
            # Check for JARVIS related processes
            if any(keyword in cmdline.lower() for keyword in [
                'jarvis', 'main.py', 'd:\\code\\jarvis'
            ]) or proc.info['name'].lower() in ['jarvis.exe', 'jarvis']:
                
                jarvis_processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'cmdline': cmdline
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    return jarvis_processes

def stop_monitoring():
    """Stop monitoring and clear session data"""
    try:
        session_file = "session_data.json"
        
        # Clear monitoring status
        session_data = {
            'monitoring_active': False,
            'last_session': datetime.now().isoformat(),
            'shutdown_time': datetime.now().isoformat()
        }
        
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print("[SHUTDOWN] Monitoring stopped and session cleared")
        return True
    
    except Exception as e:
        print(f"[ERROR] Could not stop monitoring: {e}")
        return False

def kill_process_tree(pid):
    """Kill process and all its children"""
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        
        # Kill children first
        for child in children:
            try:
                child.terminate()
                print(f"[KILLED] Child process PID {child.pid}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Kill parent
        parent.terminate()
        print(f"[KILLED] Parent process PID {pid}")
        
        # Wait for termination
        gone, alive = psutil.wait_procs([parent] + children, timeout=3)
        
        # Force kill if still alive
        for proc in alive:
            try:
                proc.kill()
                print(f"[FORCE KILLED] PID {proc.pid}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        return True
    
    except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
        print(f"[ERROR] Could not kill PID {pid}: {e}")
        return False

def shutdown_jarvis():
    """Complete JARVIS shutdown"""
    print("JARVIS SHUTDOWN SCRIPT")
    print("=" * 30)
    
    # Step 1: Stop monitoring
    print("\n[STEP 1] Stopping monitoring...")
    stop_monitoring()
    
    # Step 2: Find JARVIS processes
    print("\n[STEP 2] Finding JARVIS processes...")
    processes = find_jarvis_processes()
    
    if not processes:
        print("No JARVIS processes found running")
        return True
    
    print(f"Found {len(processes)} JARVIS processes:")
    for proc in processes:
        print(f"  PID {proc['pid']}: {proc['name']} - {proc['cmdline'][:60]}...")
    
    # Step 3: Graceful shutdown attempt
    print("\n[STEP 3] Attempting graceful shutdown...")
    
    for proc_info in processes:
        try:
            proc = psutil.Process(proc_info['pid'])
            
            # Send SIGTERM (graceful shutdown)
            proc.terminate()
            print(f"[TERMINATE] Sent SIGTERM to PID {proc_info['pid']}")
            
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            print(f"[SKIP] PID {proc_info['pid']} already gone or access denied")
    
    # Step 4: Wait for graceful shutdown
    print("\n[STEP 4] Waiting for graceful shutdown...")
    time.sleep(3)
    
    # Step 5: Force kill remaining processes
    print("\n[STEP 5] Force killing remaining processes...")
    
    remaining = find_jarvis_processes()
    killed_count = 0
    
    for proc_info in remaining:
        if kill_process_tree(proc_info['pid']):
            killed_count += 1
    
    # Step 6: Final verification
    print("\n[STEP 6] Final verification...")
    time.sleep(1)
    
    final_check = find_jarvis_processes()
    
    if final_check:
        print(f"WARNING: {len(final_check)} processes still running:")
        for proc in final_check:
            print(f"  PID {proc['pid']}: {proc['name']}")
        return False
    else:
        print("SUCCESS: All JARVIS processes terminated")
        return True

def emergency_shutdown():
    """Emergency shutdown - kill all Python processes in JARVIS directory"""
    print("\nEMERGENCY SHUTDOWN MODE")
    print("=" * 25)
    
    killed_count = 0
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'].lower().startswith('python'):
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                
                if 'jarvis' in cmdline.lower() or 'd:\\code\\jarvis' in cmdline.lower():
                    proc.kill()
                    killed_count += 1
                    print(f"[EMERGENCY KILL] PID {proc.info['pid']}")
        
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    print(f"Emergency killed {killed_count} processes")
    return killed_count > 0

if __name__ == "__main__":
    try:
        # Normal shutdown
        success = shutdown_jarvis()
        
        if not success:
            print("\nNormal shutdown failed. Trying emergency shutdown...")
            emergency_shutdown()
        
        print("\nJARVIS SHUTDOWN COMPLETE")
        
    except KeyboardInterrupt:
        print("\nShutdown interrupted by user")
        emergency_shutdown()
    
    except Exception as e:
        print(f"\nShutdown error: {e}")
        emergency_shutdown()