

🔍 Subdomain Scanner Tool – Features, Commands & Descriptions
✅ Features
Feature	Description
🌐 Subdomain Brute Forcing	Uses a wordlist to find possible subdomains
🧠 DNS Resolution	Resolves each subdomain to check if it's live
⚡ Multithreading Support	Scans multiple subdomains in parallel for faster results
🎨 Colored Output	Easy-to-read success/fail status using colored terminal output (with colorama)
📝 Output Summary	Shows a list of all live subdomains at the end
🧩 Custom Wordlist Support	You can use your own custom subdomain wordlist
🎯 Easy Command-Line Interface	Simple CLI arguments with help flags

💻 Command Usage
   python subdomain.py -d example.com -w subdomains.txt

Or with custom threads:

python subdomain.py -d example.com -w subdomains.txt -t 50

📄 Command-Line Arguments & Descriptions
Argument	Description	Example
-d, --domain	Target domain name to scan subdomains for	-d example.com
-w, --wordlist	Path to subdomain wordlist file	-w wordlists/subdomains.txt
-t, --threads	Number of concurrent threads (optional, default = 20)	-t 50
-h, --help	Show help message and exit	-h
🧪 Example Wordlist (subdomains.txt)
www
ftp
admin
mail
api
test
dev
portal
shop
beta

🖥️ Sample Output
[*] Scanning 100 subdomains on example.com with 20 threads...

[LIVE] www.example.com -> 93.184.216.34
[LIVE] mail.example.com -> 93.184.216.22
[DEAD] test.example.com
[DEAD] ftp.example.com
...

[+] Scan complete. 2 live subdomains found:
 - www.example.com
 - mail.example.com

⚙️ Requirements

Python 3.x

colorama (optional for colored output)

Install required module:
pip install colorama

📦 requirements.txt

For easy installation:

colorama

