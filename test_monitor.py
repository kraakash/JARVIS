"""
Test Desktop Monitor System
"""

from modules.monitoring.desktop_monitor import desktop_monitor
import time

def test_monitor():
    print("Testing Desktop Monitor System")
    print("=" * 40)
    
    # Test 1: Check if monitoring is available
    print("1. Checking monitoring availability...")
    try:
        from modules.monitoring.desktop_monitor import MONITORING_AVAILABLE
        if MONITORING_AVAILABLE:
            print("   [OK] Monitoring libraries available")
        else:
            print("   [ERROR] Monitoring libraries missing")
            return False
    except Exception as e:
        print(f"   [ERROR] Import error: {e}")
        return False
    
    # Test 2: Start monitoring
    print("\n2. Starting desktop monitoring...")
    success = desktop_monitor.start_monitoring()
    if success:
        print("   [OK] Monitoring started successfully")
    else:
        print("   [ERROR] Failed to start monitoring")
        return False
    
    # Test 3: Monitor for 10 seconds
    print("\n3. Monitoring for 10 seconds...")
    print("   Switch between different apps to test tracking...")
    
    for i in range(10):
        time.sleep(1)
        current = desktop_monitor.get_current_activity()
        if current:
            print(f"   [{i+1}s] {current['app']}: {current['duration']}s")
        else:
            print(f"   [{i+1}s] No activity detected")
    
    # Test 4: Get activity summary
    print("\n4. Getting activity summary...")
    summary = desktop_monitor.get_activity_summary()
    print(f"   {summary}")
    
    # Test 5: Check suggestions
    print("\n5. Checking suggestions...")
    suggestions = desktop_monitor.get_recent_suggestions()
    if suggestions:
        for suggestion in suggestions:
            print(f"   [SUGGESTION] {suggestion['message']}")
    else:
        print("   No suggestions yet")
    
    # Test 6: Stop monitoring
    print("\n6. Stopping monitoring...")
    desktop_monitor.stop_monitoring()
    print("   [OK] Monitoring stopped")
    
    print("\nDesktop Monitor Test Complete!")
    return True

if __name__ == "__main__":
    test_monitor()