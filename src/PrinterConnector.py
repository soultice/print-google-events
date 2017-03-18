import subprocess
import os

class PrinterConnector():

    def list_printers(self):
        cmd = ['lpstat', '-s']
        self.printers = subprocess.check_output(cmd).split('\n')

    def print_file(self, printer, filein):
        cmd = ['lp', '-d', printer, filein]
        subprocess.call(cmd)



