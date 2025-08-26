

import yaml
from netmiko import ConnectHandler
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def load_devices():
    """Loads device credentials from devices.yaml."""
    try:
        with open("devices.yaml", "r") as file:
            data = yaml.safe_load(file)
            if "devices" not in data:
                raise KeyError("Missing 'devices' key in YAML file")
            return data["devices"]
    except yaml.YAMLError as e:
        print(Fore.RED + f"❌ YAML Parsing Error: {e}")
        exit(1)
    except FileNotFoundError:
        print(Fore.RED + "❌ Error: devices.yaml file not found.")
        exit(1)

def ssh_connect(device):
    """
    Attempts SSH connection to a device.

    Args:
        device (dict): Device connection details.

    Returns:
        bool: True if SSH is successful, False otherwise.
    """
    try:
        connection = ConnectHandler(
            device_type="cisco_ios" if device["os_type"] == "ios-xe" else "cisco_xr",
            host=device["host"],
            username=device["username"],
            password=device["password"],
            port=device["port"]
        )
        connection.disconnect()
        print(Fore.GREEN + f"✅ SUCCESS: SSH to {device['name']} ({device['host']})")
        return True
    except Exception as e:
        print(Fore.RED + f"❌ FAILED: SSH to {device['name']} ({device['host']}) - {e}")
        return False

if __name__ == "__main__":
    devices = load_devices()
    print(Fore.CYAN + "\n🔹 Attempting SSH connections...\n" + Style.RESET_ALL)
    for device in devices:
        ssh_connect(device)
    print(Fore.YELLOW + "\n🔹 SSH Checks Completed.\n")
