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
iface = input ('Enter Your Wifi Interface Name : ')
print ('\nProbe Capturing Started. \nPress Ctrl+C To Stop\n')
os.system (f'tcpdump -l -i {iface} -e -s 256 type mgt subtype probe-req | awk -f tcpdump.awk | tee -a "captured_probes.txt" ')
