class INPUT_DATA_ERROR(Exception):
    """Exception raised for errors in the input data.
 
    Args:
        Exception (_type_): Built-in class
    """
    def __init__(self, message):
        self.message = f"Input data error: {message}"
        super().__init__(self.message)
