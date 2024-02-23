from termcolor import cprint
import subprocess
import re, sys
import argparse
import random

def printAscii():
    cprint("""
███╗░░░███╗░█████╗░░█████╗░  ░█████╗░██╗░░██╗░█████╗░███╗░░██╗░██████╗░███████╗██████╗░
████╗░████║██╔══██╗██╔══██╗  ██╔══██╗██║░░██║██╔══██╗████╗░██║██╔════╝░██╔════╝██╔══██╗
██╔████╔██║███████║██║░░╚═╝  ██║░░╚═╝███████║███████║██╔██╗██║██║░░██╗░█████╗░░██████╔╝
██║╚██╔╝██║██╔══██║██║░░██╗  ██║░░██╗██╔══██║██╔══██║██║╚████║██║░░╚██╗██╔══╝░░██╔══██╗
██║░╚═╝░██║██║░░██║╚█████╔╝  ╚█████╔╝██║░░██║██║░░██║██║░╚███║╚██████╔╝███████╗██║░░██║
╚═╝░░░░░╚═╝╚═╝░░╚═╝░╚════╝░  ░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝░╚═════╝░╚══════╝╚═╝░░╚═╝""",'yellow','on_black')
    
class MacChanger:

    def __init__(self):
        self.interface = ""
        self.new_mac = ""
        
    
    def getArguments(self):
        self.parse_object = argparse.ArgumentParser()
        self.parse_object.add_argument("-i", "--interface", type=str, metavar='', help="Enter the Interface for which you want to change the MAC Address", required=True)
        self.parse_object.add_argument("-m", "--mac", type=str, metavar='', help="Enter the new Mac Address")
        
        
    def change_mac_address(self):
        subprocess.call(["sudo","ifconfig",self.interface,"down"])
        subprocess.call(["sudo","ifconfig",self.interface,"hw","ether",self.new_mac])
        subprocess.call(["sudo","ifconfig",self.interface,"up"])

    def check_output_control(self):
        output = str(subprocess.check_output(["ifconfig",self.interface]))
        changed_mac = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w',output)
        if changed_mac:
            return changed_mac.group(0)
        else:
            return None
        
    def operationCompleted(self):
        mac = self.check_output_control()
        if mac == self.new_mac:
            cprint("[+] Successfully changed Mac Address",'green','on_black')
        else:
            cprint("[-] Could not change the Mac Address",'red','on_black')
    
    def generate_mac(self):
        cprint("[+] Generating Random Mac Address...\n",'yellow')
        mac = ""
        possible_value = ['1', '2', '3', '4', '5', '6', '7', '8', '9',
                      'a','b','c', 'd', 'e']
        value_second_place = ['2', '4', '6', '8', 'a', 'c', 'e']

        for i in range(1,13):
            if i ==2 :
                value = random.choice(value_second_place)
            else:
                value = random.choice(possible_value)
            mac += value
            if i%2 ==0 and i!=12:
                mac+=":"
        cprint("[+] Random Mac address generated successfully.\n",'yellow')
        return mac

    def check_interface(self):
        try:
            subprocess.check_call(["sudo","ifconfig",self.interface],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            cprint("\n[-] Error! Interface (" + self.interface+") not found\n", 'red')
            sys.exit(0)

    def run(self):
        try:
            self.getArguments()
            self.interface = self.parse_object.parse_args().interface
            self.check_interface()
            if self.parse_object.parse_args().mac == None:
                self.new_mac = self.generate_mac()
            else:
                self.new_mac = self.parse_object.parse_args().mac
            self.change_mac_address()
            self.operationCompleted()
        except Exception as e:
            cprint("[-] Error Occured",'red','on_black')
            sys.exit(0)



printAscii()
mac_ch = MacChanger()  
mac_ch.run()  
