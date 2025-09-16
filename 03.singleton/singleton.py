class Singleton:
  _instance = None 
  
  def __new__(cls):
      print('<new> creating...')
      
      if not cls._instance:
        cls._instance = super().__new__(cls)
        
      return cls._instance
    
  def __init__(self):
       print('<init> called..') 
  
s1 = Singleton()
s2 = Singleton()
print(s1 is s2)
  