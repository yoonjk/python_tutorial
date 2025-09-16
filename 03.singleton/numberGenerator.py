class NumberGenerator:
    _instance = None
    _current_number = 0
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
      
    def get_next_number(self):
        number = self._current_number
        self._current_number += 1
        
        return number
      
if __name__ == "__main__":
    generator1 = NumberGenerator()
    generator2 = NumberGenerator()
    
    print(f"Generator 1: {generator1.get_next_number()}")
    print(f"Generator 1: {generator1.get_next_number()}")
    print(f"Generator 2: {generator2.get_next_number()}")
    print(f"Generator 2: {generator2.get_next_number()}") 

    print(f"Generator 1: {generator1.get_next_number()}")
    print(f"Generator 2: {generator2.get_next_number()}")
    print(f"Generator 1: {generator1.get_next_number()}")
    print(f"Generator 2: {generator2.get_next_number()}") 