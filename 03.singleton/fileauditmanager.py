import threading
import datetime   

class FileAuditManager: 
  """
    This is a thread-safe Singleton class that writes log entries to a common file
    each log entry includes a timestamp and a message.
    the file name i s configurable.
  """
  
  _instance = None 
  _lock = threading.Lock()
  
  def __new__(cls, file_name = 'audit.log'):
    """_summary_

    Args:
        file_name (str, optional): _description_. Defaults to 'audit.log'.
    """
    with cls._lock:
      if cls._instance is None:
        cls._instance = super(FileAuditManager, cls).__new__(cls)
        cls._instance._file_name = file_name
        with open(cls._instance._file_name, 'a') as file:
          file.write(f"Log started: {datetime.datetime.now()}\n")
  
    return cls._instance
  
  def log_message(self, message):
    """ 
      This method writes a log entry to the file.
      each entry includes a timestamp and the message, followed by a newline character.
      It is thread-safe, ensuring that log entries remain consistent across threads.
    """
    with self._lock:
      timestamp = datetime.datetime.now().strftime('%Y%m-%d %H:%M:%S')
      with open(self._file_name, 'a') as file:
        file.write(f"{timestamp}: {message}\n")
        
def test_file_audit_manager():
  logger = FileAuditManager("test_audit.log")
  logger.log_message("Test message from thread.")
  
if __name__ == "__main__":
  threads = []
  for i in range(10):
    thread = threading.Thread(target = test_file_audit_manager)
    threads.append(thread)
    thread.start()
    
    