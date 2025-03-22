import keyboard

class KeyboardMonitor:
    
    keyboard_dict = {
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    }
    
    def __init__(self):
        keyboard.hook(self.block_input)
        
    def block_input(event):
        if event.event_type == 'down': 
            return False
    
    def is_pressed(self, key_name):
        
        if key_name:
            
            return keyboard.is_pressed(key_name)
        
    def wait_for(self, keys):
        if keys == {}: keys = self.keyboard_dict
        
        pressed = ""
        
        for key in keys:
            pressed = keyboard.wait(key)
            if pressed != "": break
        
        return pressed