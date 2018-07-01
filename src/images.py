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
 .o8       oooo                                                                                                
"888       `888                                                                                                
 888oooo.   888  oooo  oooo   .ooooo.        .oooo.o  .ooooo.  oooo d8b  .ooooo.   .ooooo.  ooo. .oo.     
 d88' `88b  888  `888  `888  d88' `88b      d88(  "8 d88' `"Y8 `888""8P d88' `88b d88' `88b `888P"Y88b   
 888   888  888   888   888  888ooo888      `"Y88b.  888        888     888ooo888 888ooo888  888   888   
 888   888  888   888   888  888    .o      o.  )88b 888   .o8  888     888    .o 888    .o  888   888   
 `Y8bod8P' o888o  `V88V"V8P' `Y8bod8P'      8""888P' `Y8bod8P' d888b    `Y8bod8P' `Y8bod8P' o888o o888o 
                                                                                                                                                                                  
                         .o88o.            .o8                          .   oooo        
                         888 `"           "888                        .o8   `888        
               .ooooo.  o888oo        .oooo888   .ooooo.   .oooo.   .o888oo  888 .oo.   
              d88' `88b  888         d88' `888  d88' `88b `P  )88b    888    888P"Y88b  
              888   888  888         888   888  888ooo888  .oP"888    888    888   888  
              888   888  888         888   888  888    .o d8(  888    888 .  888   888  
              `Y8bod8P' o888o        `Y8bod88P" `Y8bod8P' `Y888""8o   "888" o888o o888o                                                                                                                                                                                       
                                  
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
    raise Exception('\n' + colored(img_blue_screen, 'cyan', attrs=['bold']))
