import subprocess
import sys

VM_NAME = "vm-gateway"
VM_USER = "ubuntu"
VM_PASSWORD = "Ubuntu1234!"

def stress_vm():
    print(f"Starting CPU stress test on {VM_NAME}...")
    print("This will push VM CPU to 90%+ to trigger auto-scaling")
    
    # SSH command to stress the VM
    ssh_cmd = f'VBoxManage guestcontrol {VM_NAME} run --exe "/usr/bin/stress-ng" --username {VM_USER} --password {VM_PASSWORD} -- stress-ng --cpu 2 --timeout 180s'
    
    try:
        print("Running stress-ng inside VM...")
        subprocess.run(ssh_cmd, shell=True)
        print("Stress test complete")
    except Exception as e:
        print(f"Error: {e}")
        print("\nAlternative: Manually SSH into VM and run:")
        print("  sudo apt install stress-ng -y")
        print("  stress-ng --cpu 2 --timeout 180s")

if __name__ == "__main__":
    stress_vm()