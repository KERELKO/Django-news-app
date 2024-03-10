class IncorrectModelNameError(ValueError):
	"""Custom exception, raise if name of the model is incorrect"""
	def __init__(
		self, 
		model_name: str, 
		allowed_models: list[str] = None
	):
		self.model_name = model_name  
		self.allowed_models = allowed_models

	def message(self):
		if not self.allowed_models:
			return f'Incorrect name of the model: "{self.model_name.lower()}"' 
		return (
			f'Incorrect name of the model: "{self.model_name.lower()}"\n'
			f'Allowed models: {self.allowed_models}'
		)

	def __str__(self):
		return self.message()
