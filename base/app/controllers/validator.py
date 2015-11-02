from base.app.controllers import get_parameters_by_method

class Validator(object):
	def __init__(self):
		self.errors = []

	def accept(args):
		return args

class ArgumentValidator(Validator):
	def __init__(self, required_args=None):
		super(ArgumentValidator, self).__init__()
		self.required_args = required_args
		
	def accept(self, request):
		request_args = get_parameters_by_method().keys()
		if not request_args:
			return
		if self.required_args:
			self.validate_required_args(request_args)


	def validate_required_args(self, request_args):
		for arg in self.required_args:
			if arg not in request_args:
				error_msg = "Required pamameter %s is missing." % arg
				self.errors.append(error_msg)

class FileValidator(Validator):
	def __init__(self, file_name=None):
		super(FileValidator, self).__init__()
		self.file_name = file_name
		
	def accept(self, request):
		try:
			request_file = request.files[self.file_name]
		except KeyError:
			error_msg = "No file %s in request." % self.file_name
			self.errors.append(error_msg)
			return 
		if getsizeof(request_file) > 40000:
			error_msg = "File exceeds maximun size."
			self.errors.append(error_msg)