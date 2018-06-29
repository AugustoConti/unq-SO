from termcolor import colored


def logo():
    img = '''
    
  ,ad8888ba,                                     88  88  88  88               88       ,ad8888ba,     ad88888ba  
 d8"     `"8b                             ,d     ""  88  88  ""               ""      d8"     `"8b   d8"     "8b 
d8,                                       88         88  88                          d8,        `8b  Y8,         
88              ,adPPYba,   8b,dPPYba,  MM88MMM  88  88  88  88  8b,dPPYba,   88     88          88  `Y8aaaaa,   
88             a8"     "8a  88P    `"8a   88     88  88  88  88  88P    `"8a  88     88          88    `"""""8b, 
Y8,            8b       d8  88       88   88     88  88  88  88  88       88  88     Y8,        ,8P          `8b 
 Y8a.    .a8P  "8a,   ,a8"  88       88   88,    88  88  88  88  88       88  88      Y8a.    .a8P   Y8a     a8P 
  `"Y8888Y"     `"YbbdP"    88       88   "Y888  88  88  88  88  88       88  88       `"Y8888Y"      "Y88888P"  

'''
    print(colored(img, 'cyan', attrs=['bold', 'reverse']))


def blue_screen():
    img = '''
    
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
    raise Exception('\n' + colored(img, 'cyan', attrs=['bold', 'reverse']))
