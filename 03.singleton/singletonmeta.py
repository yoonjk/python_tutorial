
class SingletonMeta(type):
  """_summary_

  Args:
      type (_type_): _description_
  """
  _instances = {}
  
  def __call__(cls):
    """
       Possible changes to the value of the `__init__` argument do not effect
    """
    
    print('<call meta> calling...')
    
    if cls not in cls._instances: 
        instance = super().__call__()
        cls._instances[cls]= instance
    
    return cls._instances[cls]
  
class Singleton(metaclass=SingletonMeta):
  """_summary_

  Args:
      metaclass (_type_, optional): _description_. Defaults to SingletonMeta.
  """
  
  def some_business_logic(self):
      """ 
         The nice thing about this approach is that this Singleton can define any business logic seprately
         from the actual singleton definition/implementation (which is in the SingletonMeta class)
      """

s1 = Singleton()
s2 = Singleton()
s3 = Singleton()
print(s1 is s2)      
print(s1 is s3)    
  