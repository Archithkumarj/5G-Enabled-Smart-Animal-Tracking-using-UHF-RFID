import csv
import socket

CSV_FILE = r''#file location

# Map EPCs to their corresponding Student data
epc_map = {
    "E2 00 00 1A 99 02 01 13 25 60 53 70": "Sheep",
    "E2 00 00 1A 99 02 01 33 25 60 6D 6E": "Dog",
    "E2 00 00 1A 99 02 41 26 25 60 5D 23": "Cow",
    "E2 00 00 1A 99 02 01 26 25 60 5D 23": "Hen"
}

UDP_IP = ""#MEC IP
UDP_PORT = 5005

try:
    student_attandance = []

    with open(CSV_FILE, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            if len(row) >= 4:
                epc = row[2].strip()
                
                
                student = epc_map.get(epc, "Unknown")

                identification = f"{student}: EPC={epc}"
                
                student_attandance.append(identification)

    if not student_attandance:
        print("No EPC tags found.")
    else:
        message = "student attandence:\n" + "\n".join(student_attandance)

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.sendto(message.encode('utf-8'), (UDP_IP, UDP_PORT))
            print(f"Data successfully sent to MEC server {UDP_IP}:{UDP_PORT}")

except Exception as e:
    print(f"Error: {e}")
