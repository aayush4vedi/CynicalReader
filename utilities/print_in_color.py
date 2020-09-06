

""" 
    Contains texts to print in color, all work same as print()
    * printWarn() => Cyan
    * printErr()  => Red
    * printSucc() => Green
    * printLog()  => Grey
    * printMsg()  => Yellow
"""

def printWarn(txt): 
    print("\033[96m {}\033[00m" .format(txt)) 

def printErr(txt): 
    print("\033[91m {}\033[00m" .format(txt)) 

def printSucc(txt): 
    print("\033[92m {}\033[00m" .format(txt)) 

def printLog(txt): 
    print("\033[95m {}\033[00m" .format(txt)) 

def printMsg(txt): 
    print("\033[93m {}\033[00m" .format(txt)) 

"""
    Other colors, not used currently
"""

def prRed(txt): print("\033[91m {}\033[00m" .format(txt)) 
def prGreen(txt): print("\033[92m {}\033[00m" .format(txt)) 
def prYellow(txt): print("\033[93m {}\033[00m" .format(txt)) 
def prLightPurple(txt): print("\033[94m {}\033[00m" .format(txt)) 
def prPurple(txt): print("\033[95m {}\033[00m" .format(txt)) 
def prCyan(txt): print("\033[96m {}\033[00m" .format(txt)) 
def prLightGray(txt): print("\033[97m {}\033[00m" .format(txt)) 
def prBlack(txt): print("\033[98m {}\033[00m" .format(txt)) 
