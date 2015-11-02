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

