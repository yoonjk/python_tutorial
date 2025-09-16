import threading 
  
class NumberGenerator:
    _instance = None
    _lock = threading.Lock()
    _current_number = 0
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance
      
    def get_next_number(self):
        with self._lock:
            number = self._current_number
            self._current_number += 1
        
        return number
      
def test_singleton_thread_safe():
    generator = NumberGenerator()
    print(f"Generated Number: {generator.get_next_number()}")
    
    
if __name__ == "__main__":
    threads = []
    
    for i in range(10):
        thread = threading.Thread(target = test_singleton_thread_safe)
        threads.append(thread)
        thread.start()
        
    