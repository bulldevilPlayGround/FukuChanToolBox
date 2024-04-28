import subprocess
import sys
import signal

def run_nc_command(port, ip):
    # Connect to the specified IP address and port using nc command
    nc_command = f"nc {ip} {port}"
    process = subprocess.Popen(nc_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Read the initial prompt from nc command
    prompt = process.stdout.readline().decode().strip()
    print(prompt, end=" ")

    # Keep reading user input and sending commands until user exits
    try:
        while True:
            # Read user input
            user_input = input()

            # Send user input as command to nc command
            process.stdin.write(user_input.encode() + b"\n")
            process.stdin.flush()

            # Read the output from nc command
            output = process.stdout.readline().decode().strip()

            # Print the prompt and output
            print(prompt, output, end=" ")

            # Break the loop if user exits
            if user_input == "exit":
                break
    except KeyboardInterrupt:
        # Close the nc command process if script is canceled
        process.send_signal(signal.SIGINT)

    # Close the nc command process
    process.stdin.close()
    process.stdout.close()
    process.stderr.close()
    process.wait()

if __name__ == "__main__":
    #add input argv check, and print help info if input args are not enough
    if len(sys.argv) < 3:
        print("Usage: python3 runCommand.py [IPaddress] [port]")
        sys.exit(1)
    # take port and ip from input args
    ip = sys.argv[1]
    port = sys.argv[2]
    run_nc_command(port, ip)