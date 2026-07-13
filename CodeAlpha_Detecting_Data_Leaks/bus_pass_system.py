import queue
import threading
import time
import random

# Global system variables simulating a highly scalable cluster architecture
available_passes = 5
pass_lock = threading.Lock()
traffic_queue = queue.Queue()

def cloud_provision_worker(server_id):
    """Simulates a dynamically provisioned virtual cloud machine instance."""
    global available_passes
    while not traffic_queue.empty():
        try:
            user_id = traffic_queue.get_nowait()
        except queue.Empty:
            break
        
        print(f"[SERVER-{server_id}] Processing reservation request for User_{user_id}...")
        # Simulate processing delay on cloud node
        time.sleep(random.uniform(0.1, 0.4))
        
        # High traffic thread safety zone
        with pass_lock:
            if available_passes > 0:
                available_passes -= 1
                print(f"🏆 [SUCCESS] Pass booked for User_{user_id}! (Passes left: {available_passes})")
            else:
                print(f"❌ [FAILED] Pass denied for User_{user_id}. All slots are sold out!")
        
        traffic_queue.task_done()

def simulate_high_traffic_booking():
    global available_passes
    available_passes = 5 # Reset passes counter
    
    print("\n--- Initializing Automated Elastic Cloud Cluster ---")
    total_concurrent_users = 12
    print(f"Flooding network with {total_concurrent_users} simultaneous booking hits...")
    
    # Load requests directly into global queue
    for i in range(1, total_concurrent_users + 1):
        traffic_queue.put(i)
        
    # Scale dynamically out to 3 virtual container servers to absorb the high traffic spike
    spawned_servers = []
    for server_node in range(1, 4):
        t = threading.Thread(target=cloud_provision_worker, args=(server_node,))
        spawned_servers.append(t)
        t.start()
        
    # Block operations until all instances sync up and clear out requests safely
    for t in spawned_servers:
        t.join()
        
    print("\n--- Cloud Execution Spike Completed Cleanly ---")

def main():
    while True:
        print("\n=============================================")
        print(" TASK 3: ELASTIC CLOUD BUS PASS MANAGER      ")
        print("=============================================")
        print("1. Launch High Traffic Concurrent Stress Test")
        print("2. Exit")
        
        choice = input("Select an option (1-2): ")
        if choice == '1':
            simulate_high_traffic_booking()
        elif choice == '2':
            print("Shutting down Bus Pass Cloud Nodes.")
            break
        else:
            print("Invalid entry.")

if __name__ == "__main__":
    main()