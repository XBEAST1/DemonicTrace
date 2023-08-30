import subprocess
import os
import glob

print ('''
________  __________ ___       ___   ____   ___      _______   ____         __________ ________          _        ____   __________ 
`MMMMMMMb.`MMMMMMMMM `MMb     dMM'  6MMMMb  `MM\     `M'`MM'  6MMMMb/       MMMMMMMMMM `MMMMMMMb.       dM.      6MMMMb/ `MMMMMMMMM 
 MM    `Mb MM      \  MMM.   ,PMM  8P    Y8  MMM\     M  MM  8P    YM       /   MM   \  MM    `Mb      ,MMb     8P    YM  MM      \ 
 MM     MM MM         M`Mb   d'MM 6M      Mb M\MM\    M  MM 6M      Y           MM      MM     MM      d'YM.   6M      Y  MM        
 MM     MM MM    ,    M YM. ,P MM MM      MM M \MM\   M  MM MM                  MM      MM     MM     ,P `Mb   MM         MM    ,   
 MM     MM MMMMMMM    M `Mb d' MM MM      MM M  \MM\  M  MM MM                  MM      MM    .M9     d'  YM.  MM         MMMMMMM   
 MM     MM MM    `    M  YM.P  MM MM      MM M   \MM\ M  MM MM                  MM      MMMMMMM9'    ,P   `Mb  MM         MM    `   
 MM     MM MM         M  `Mb'  MM MM      MM M    \MM\M  MM MM                  MM      MM  \M\      d'    YM. MM         MM        
 MM     MM MM         M   YP   MM YM      M9 M     \MMM  MM YM      6           MM      MM   \M\    ,MMMMMMMMb YM      6  MM        
 MM    .M9 MM      /  M   `'   MM  8b    d8  M      \MM  MM  8b    d9           MM      MM    \M\   d'      YM. 8b    d9  MM      / 
_MMMMMMM9'_MMMMMMMMM _M_      _MM_  YMMMM9  _M_      \M _MM_  YMMMM9           _MM_    _MM_    \M\_dM_     _dMM_ YMMMM9  _MMMMMMMMM 
       
                                  by XBEAST ~  Hunt, haunt, and expose with Wi-Fi Enforcer.
                                                         v3.2
                                        Github Link: https://github.com/XBEAST1

''')
def loop():
    global iface
    # Function to retrieve the Wi-Fi adapters available
    def get_wifi_adapters():
        try:
            # Executes the 'iw dev' command and captures the output
            output = subprocess.check_output(['iw', 'dev'], stderr=subprocess.STDOUT, universal_newlines=True)
            # Split the output into lines
            lines = output.split('\n')
            adapters = []

            # Iterate over the lines and find the Wi-Fi adapters
            for line in lines:
                if 'Interface' in line:
                    # Extract the adapter name
                    adapter = line.split(' ')[-1]
                    adapters.append(adapter)

            return adapters
        except subprocess.CalledProcessError as e:
            # If the command execution fails, print the error
            print(f"Command execution failed with error: {e.output}")

    # Retrieve the available Wi-Fi adapters
    wifi_adapters = get_wifi_adapters()

    # If there are Wi-Fi adapters available
    if len(wifi_adapters) > 0:
        print("Available Wi-Fi adapters:\n")
        # Print the list of available adapters with their corresponding numbers
        for index, adapter in enumerate(wifi_adapters, start=1):
            print(f"{index}. {adapter}\n")

        while True:
            # Prompt the user to select a Wi-Fi adapter by entering the corresponding number
            selection = input("Enter the number corresponding to the Wi-Fi adapter you want to select: \n\nYour Choice: ")

            try:
                selection = int(selection)
                # If the selection is valid, assign the selected adapter to 'iface'
                if selection >= 1 and selection <= len(wifi_adapters):
                    iface = wifi_adapters[selection - 1]
                    print(f"Selected Wi-Fi adapter: {iface}")
                    break
                else:
                    print("\nInvalid selection.\n")
            except ValueError:
                print("\nInvalid input. Please enter a number.\n")
    else:
        print("No Wi-Fi adapters found.")

# Call the 'loop' function
loop()

# Kill any conflicting processes using 'airmon-ng'
os.system('airmon-ng check kill')

# Start monitor mode on the selected Wi-Fi adapter using 'airmon-ng'
os.system(f'airmon-ng start {iface}')

# Check if a specific interface exists, and if it does, assign it to 'iface'
check_iface = glob.glob('/sys/class/net/wlan*mon')

if check_iface:
    # Get the first matching interface
    iface = os.path.basename(check_iface[0])

# Clear the screen
os.system('clear')

# Capture probe requests using 'tcpdump' and save them to 'captured_probes.txt'
os.system(f'tcpdump -l -i {iface} -e -s 256 type mgt subtype probe-req | awk -f tcpdump.awk | tee -a "captured_probes.txt"')

# Stop monitor mode on the Wi-Fi adapter using 'airmon-ng'
os.system(f'airmon-ng stop {iface}')

# Restart the NetworkManager service
os.system('service NetworkManager restart')