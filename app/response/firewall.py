import subprocess


class WindowsFirewall:
    RULE_PREFIX = "AutonomousSOC_Block_"

    def block_ip(self, ip_address: str) -> dict:
        rule_name = f"{self.RULE_PREFIX}{ip_address}"

        command = [
            "netsh",
            "advfirewall",
            "firewall",
            "add",
            "rule",
            f"name={rule_name}",
            "dir=in",
            "action=block",
            f"remoteip={ip_address}"
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return {
                "status": "FAILED",
                "action": "BLOCK_IP",
                "ip": ip_address,
                "rule_name": rule_name,
                "error": result.stderr.strip()
            }

        return {
            "status": "BLOCKED",
            "action": "BLOCK_IP",
            "ip": ip_address,
            "rule_name": rule_name
        }

    def verify_block(self, ip_address: str) -> dict:
        rule_name = f"{self.RULE_PREFIX}{ip_address}"

        command = [
            "netsh",
            "advfirewall",
            "firewall",
            "show",
            "rule",
            f"name={rule_name}"
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        verified = (
            result.returncode == 0
            and "Rule Name" in result.stdout
        )

        return {
            "ip": ip_address,
            "rule_name": rule_name,
            "verified": verified,
            "status": "VERIFIED" if verified else "NOT_VERIFIED"
        }


firewall = WindowsFirewall()