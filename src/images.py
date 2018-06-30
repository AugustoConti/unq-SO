from time import sleep

from termcolor import colored

img_logo = '''  ,ad8888ba,                                     88  88  88  88               88       ,ad8888ba,     ad88888ba  
 d8"     `"8b                             ,d     ""  88  88  ""               ""      d8"     `"8b   d8"     "8b 
d8,                                       88         88  88                          d8,        `8b  Y8,         
88              ,adPPYba,   8b,dPPYba,  MM88MMM  88  88  88  88  8b,dPPYba,   88     88          88  `Y8aaaaa,   
88             a8"     "8a  88P    `"8a   88     88  88  88  88  88P    `"8a  88     88          88    `"""""8b, 
Y8,            8b       d8  88       88   88     88  88  88  88  88       88  88     Y8,        ,8P          `8b 
 Y8a.    .a8P  "8a,   ,a8"  88       88   88,    88  88  88  88  88       88  88      Y8a.    .a8P   Y8a     a8P 
  `"Y8888Y"     `"YbbdP"    88       88   "Y888  88  88  88  88  88       88  88       `"Y8888Y"      "Y88888P"  
'''

img_blue_screen = '''

                          BLUE SCREEN OF DEATH

                                uuuuuuu                   
                            uu$$$$$$$$$$$uu               
                         uu$$$$$$$$$$$$$$$$$uu            
                        u$$$$$$$$$$$$$$$$$$$$$u           
                       u$$$$$$$$$$$$$$$$$$$$$$$u          
                      u$$$$$$$$$$$$$$$$$$$$$$$$$u         
                      u$$$$$$$$$$$$$$$$$$$$$$$$$u         
                      u$$$$$$"   "$$$"   "$$$$$$u         
                      "$$$$"      u$u       $$$$"         
                       $$$u       u$u       u$$$          
                       $$$u      u$$$u      u$$$          
                        "$$$$uu$$$   $$$uu$$$$"           
                         "$$$$$$$"   "$$$$$$$"            
                           u$$$$$$$u$$$$$$$u              
                            u$"$"$"$"$"$"$u               
                 uuu        $$u$ $ $ $ $u$$       uuu     
                u$$$$        $$$$$u$u$u$$$       u$$$$    
                 $$$$$uu      "$$$$$$$$$"     uu$$$$$$    
               u$$$$$$$$$$$uu    """""    uuuu$$$$$$$$$$  
               $$$$"""$$$$$$$$$$uuu   uu$$$$$$$$$"""$$$"  
                """      ""$$$$$$$$$$$uu ""$"""           
                          uuuu ""$$$$$$$$$$uuu            
                 u$$$uuu$$$$$$$$$uu ""$$$$$$$$$$$uuu$$$   
                 $$$$$$$$$$""""           ""$$$$$$$$$$$"  
                  "$$$$$"                      ""$$$$""   
                    $$$"                         $$$$"


'''


def logo():
    print("Loading...")
    for line in img_logo.splitlines():
        sleep(0.5)
        print(colored(line, 'cyan', attrs=['bold', 'reverse']))
    print()


def blue_screen():
    raise Exception('\n' + colored(img_blue_screen, 'cyan', attrs=['bold', 'reverse']))
