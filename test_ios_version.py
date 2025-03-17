import yaml
import sys
from netmiko import ConnectHandler
from colorama import Fore, Style, init

# Initialize colorama for color support
init()

def load_devices():
    """Loads device credentials from devices.yaml."""
    try:
        with open("devices.yaml", "r") as file:
            data = yaml.safe_load(file)
            if "devices" not in data:
                raise KeyError("Missing 'devices' key in YAML file")
            return data["devices"]
    except yaml.YAMLError as e:
        print(f"{Fore.RED}❌ YAML Parsing Error: {e}{Style.RESET_ALL}")
        sys.exit(1)

def get_device_version(device):
    """
    Connects to a Cisco device (IOS-XE or IOS-XR) and retrieves the version.

    Args:
        device (dict): Device connection details.

    Returns:
        str: OS version if successful, "ERROR" if unreachable.
    """
    try:
        if "os_type" not in device:
            raise KeyError("Missing 'os_type' in device configuration")

        os_type = device["os_type"]
        if os_type == "ios-xe":
            device_type = "cisco_ios"
            command = "show version | include Cisco IOS XE Software"
        elif os_type == "ios-xr":
            device_type = "cisco_xr"
            command = "show version | include Cisco IOS XR Software"
        else:
            raise ValueError(f"Unsupported OS type: {os_type}")

        connection = ConnectHandler(
            device_type=device_type,
            host=device["host"],
            username=device["username"],
            password=device["password"],
            port=device["port"]
        )
        output = connection.send_command(command)
        connection.disconnect()

        return output.strip()

    except KeyError as e:
        print(f"{Fore.RED}❌ Missing key in device config: {e}{Style.RESET_ALL}")
        return "ERROR"
    except ValueError as e:
        print(f"{Fore.RED}❌ Configuration Error: {e}{Style.RESET_ALL}")
        return "ERROR"
    except Exception as e:
        print(f"{Fore.RED}❌ {device['name']} ({device['host']}) - Unreachable: {e}{Style.RESET_ALL}")
        return "ERROR"

if __name__ == "__main__":
    devices = load_devices()
    print(f"\n{Fore.CYAN}🔍 Checking Cisco Device Versions...{Style.RESET_ALL}\n")

    for device in devices:
        version_output = get_device_version(device)
        if version_output != "ERROR":
            print(f"{Fore.GREEN}✅ {device['name']} ({device['host']}) - {device['os_type'].upper()} Version: {version_output}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ {device['name']} ({device['host']}) - Unreachable or Error{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}✔️ Completed Version Checks.{Style.RESET_ALL}\n")
