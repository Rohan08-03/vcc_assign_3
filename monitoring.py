import time
import subprocess
import re

THRESHOLD = 20
VM_NAME = "vm-gateway"
VBOX_PATH = r"Z:\VirtualBox\VBoxManage.exe"
GCP_PROJECT_ID = "virtual-cloud-computing"  
GCP_ZONE = "asia-south1-a"  
GCP_INSTANCE_NAME = "auto-scaled-vm"

def get_vm_cpu():
    """Get CPU usage of VirtualBox VM"""
    try:
        cmd = f'"{VBOX_PATH}" metrics query {VM_NAME} CPU/Load/User:avg'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
        
        # Try to parse percentage
        lines = result.stdout.split('\n')
        for line in lines:
            if 'CPU/Load/User' in line or '%' in line:
                match = re.search(r'(\d+\.?\d*)\s*%', line)
                if match:
                    return float(match.group(1))
        
        # Fallback: return a simulated value for testing
        return 0
    except Exception as e:
        print(f"Warning: {e}")
        return 0

def create_gcp_vm():
    print("\nTHRESHOLD EXCEEDED! Creating GCP VM...")
    
    cmd = f'gcloud compute instances create {GCP_INSTANCE_NAME} --project={GCP_PROJECT_ID} --zone={GCP_ZONE} --machine-type=e2-micro --image-family=ubuntu-2204-lts --image-project=ubuntu-os-cloud --boot-disk-size=10GB --tags=http-server'
    
    try:
        subprocess.run(cmd, shell=True, check=True)
        print("GCP VM created successfully!")
        
        with open('scale_log.txt', 'a') as f:
            f.write(f"{time.ctime()}: Auto-scaled to GCP\n")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    print(f"Monitoring VirtualBox VM: {VM_NAME}")
    print(f"CPU Threshold: {THRESHOLD}%")
    print(f"VBoxManage: {VBOX_PATH}")
    print("-" * 60)
    
    # Enable metrics collection
    try:
        subprocess.run(f'"{VBOX_PATH}" metrics setup', shell=True, capture_output=True)
    except:
        pass
    
    count = 0
    while True:
        cpu = get_vm_cpu()
        count += 1
        
        print(f"[{time.strftime('%H:%M:%S')}] Check #{count} - VM CPU: {cpu:.1f}%", end="")
        
        if cpu > THRESHOLD:
            print(" THRESHOLD EXCEEDED!")
            create_gcp_vm()
            break
        else:
            print("OK")
        
        time.sleep(10)

if __name__ == "__main__":
    main()