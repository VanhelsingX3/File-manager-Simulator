class Compare:
    def __init__(self):
        self.alphabet = "!-_/\{@}[]#=+$%^&*()0123456789abcdefghijklmnopqrstuvwxzABCDEFGHIJKLMNOPQRSTUVWXYZáéíóúÁÉÍÓÚ"
    
    def compare(self,obj1,obj2):
        if(obj1 == obj2):
            return 0

        if(len(obj1) == len(obj2)):
            for i in range(len(obj1)):
                if(self.alphabet.index(obj1[i]) < self.alphabet.index(obj2[i])):
                    return -1
                elif (self.alphabet.index(obj1[i]) > self.alphabet.index(obj2[i])):
                    return 1

        if(len(obj1) < len(obj2)):
            return -1

        if(len(obj1) > len(obj2)):        
            return 1
                
        