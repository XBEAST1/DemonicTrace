import subprocess
import os

print ('''
                                                                                                   
                                                                                                   
________   __________ ___       ___   ____    ___      ___      __________ ____     ___ __________ 
`MMMMMMMb. `MMMMMMMMM `MMb     dMM'  6MMMMb   `MM\     `M'      `MMMMMMMMM `MM(     )M' `MMMMMMMMM 
 MM    `Mb  MM      \  MMM.   ,PMM  8P    Y8   MMM\     M        MM      \  `MM.    d'   MM      \ 
 MM     MM  MM         M`Mb   d'MM 6M      Mb  M\MM\    M        MM          `MM.  d'    MM        
 MM     MM  MM    ,    M YM. ,P MM MM      MM  M \MM\   M        MM    ,      `MM d'     MM    ,   
 MM     MM  MMMMMMM    M `Mb d' MM MM      MM  M  \MM\  M        MMMMMMM       `MM'      MMMMMMM   
 MM     MM  MM    `    M  YM.P  MM MM      MM  M   \MM\ M        MM    `        MM       MM    `   
 MM     MM  MM         M  `Mb'  MM MM      MM  M    \MM\M        MM             MM       MM        
 MM     MM  MM         M   YP   MM YM      M9  M     \MMM        MM             MM       MM        
 MM    .M9  MM      /  M   `'   MM  8b    d8   M      \MM        MM      /      MM       MM      / 
_MMMMMMM9' _MMMMMMMMM _M_      _MM_  YMMMM9   _M_      \M       _MMMMMMMMM     _MM_     _MMMMMMMMM 
                                                                                                   
                                                                                                   
                                                                                                   
''')
def loop():
    global iface
    def get_wifi_adapters():
        try:
            output = subprocess.check_output(['iw', 'dev'], stderr=subprocess.STDOUT, universal_newlines=True)
            lines = output.split('\n')
            adapters = []

            for line in lines:
                if 'Interface' in line:
                    adapter = line.split(' ')[-1]
                    adapters.append(adapter)

            return adapters
        except subprocess.CalledProcessError as e:
            print(f"Command execution failed with error: {e.output}")

    wifi_adapters = get_wifi_adapters()

    if len(wifi_adapters) > 0:
        print("Available Wi-Fi adapters:\n")
        for index, adapter in enumerate(wifi_adapters, start=1):
            print(f"{index}. {adapter}\n")

        while True:
            selection = input("Enter the number corresponding to the Wi-Fi adapter you want to select: \n\n")
            
            try:
                selection = int(selection)
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

loop()

os.system ('airmon-ng check kill')
os.system (f'airmon-ng start {iface}')
print ('\nProbe Capturing Started. \nPress Ctrl+C To Stop\n')
os.system (f'tcpdump -l -i {iface} -e -s 256 type mgt subtype probe-req | awk -f tcpdump.awk | tee -a "captured_probes.txt" ')
os.system (f'airmon-ng stop {iface}')
os.system ('service NetworkManager restart')