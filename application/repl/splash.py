import values, logging

splash = f"""
                                                        ▄▄▄▄▄▄▄▄▄▄▄             
                                                        ███████████      
     ██████████████████████████████████████████████████████████████████████    
     ██▌                                                                ▐██    
     ██▌      ██████████████                                            ▐██    
     ██▌      ███        ███                                            ▐██    
     ██▌      ██████████████                                            ▐██    
     ██▌                                                                ▐██    
     ██▌                                                                ▐██    
     ██▌                     ▄█▄▄                                       ▐██    
     ██▌                      ▀████▄                                    ▐██    
     ██▌                         ▀▀████▄                                ▐██    
     ██▌                            ▄████▌                              ▐██    
     ██▌                         ▄████▀▀                                ▐██    
     ██▌                      ▄███▀▀     ▄▄▄▄▄▄▄▄▄▄                     ▐██    
     ██▌                      ▀▀         ▀▀▀▀▀▀▀▀▀▀                     ▐██    
     ██▌                                                                ▐██    
     ██▌                                                                ▐██    
     ██▌                                                                ▐██    
     ██████████████████████████████████████████████████████████████████████   

Welcome to the Sorter Shell v{values.VERSION}@{values.HASH}.

Try the following commands:
- detect [got part:True|False]
- gather
- sort [partnr]
- sdc [Direct Communication Command]
"""

def print_splash():
    for line in splash.splitlines():
        logging.info("\u001b[36m " + line)