class AppLogger ():
  @staticmethod
  def log (fileObject, message):
    try:
      fileObject.write(message)
    except Exception as e:
      raise e
