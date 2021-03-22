allowedExtentions = ['csv']

def allowed_file(*, file: str) -> bool:
  extension = file.rsplit('.', 1)[1] 
  return extension in allowedExtentions