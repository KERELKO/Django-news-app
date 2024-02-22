class ModelException(Exception):
	pass  


class IncorrectModelNameError(ModelException):
	def __init__(self, model_name: str):
		self.model_name = model_name  

	def __str__(self):
		return f'Incorrect name of the model: "{self.model_name}"'
