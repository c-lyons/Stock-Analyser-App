# Python 3
#
# Code written by Conor Lyons, James O'Doherty and Robert Pauley
#
# UCD MIS41110 Business Analytics Assignment: Group Project
# Submitted 23/11/2018
#
#

# importing menus module

import menus  # importing other referenced modules

# defining welcome message (Courtesy of http://patorjk.com ASCII script generator)
print("""
  ______   _               __             _                    __                             
.' ____ \ / |_            [  |  _        / \                  [  |                            
| (___ \_`| |-'.--.  .---. | | / ]      / _ \    _ .--.  ,--.  | |  _   __ .--. .---. _ .--.  
 _.____`. | |/ .'`\ / /'`\]| '' <      / ___ \  [ `.-. |`'_\ : | | [ \ [  ( (`\/ /__\[ `/'`\] 
| \____) || || \__. | \__. | |`\ \   _/ /   \ \_ | | | |// | |,| |  \ '/ / `'.'| \__.,| |     
 \______.'\__/'.__.''.___.[__|  \_] |____| |____[___||__\'-;__[___[\_:  / [\__) '.__.[___]    
      _______                                                      \__.'                      
     |_   __ \                                                                                
       | |__) _ .--.  .--.                                                                    
       |  ___[ `/'`\/ .'`\ \                                                                  
      _| |_   | |   | \__. |                                                                  
     |_____| [___]   '.__.'                                                                   
               _____    ____   __   ______                                                    
              / ___ `..'    './  |.' ____ '.                                                  
             |_/___) |  .--.  `| || (____) |                                                  
              .'____.| |    | || |'_.____. |                                                  
             / /_____|  `--'  _| || \____| |                                                  
             |_______|'.____.|_____\______,'                                                  
                                                                                              
                    Welcome to the Stock Analyser Pro 2019 v1.0. 
                           
To begin, please select "Explore Stock" below, or else select "Quit" to exit the application. 
""")

menus.main_prompt()

