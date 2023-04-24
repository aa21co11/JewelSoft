from math import radians

from ..lib import gemlib


def init_presets(self):
	
	# Defaults
	# ---------------------------
	
	self.number = 4
	self.diameter = 0.4 * self.gem_dim.y
	self.z1 = 0.3 * self.gem_dim.y
	self.z2 = 0.5 * self.gem_dim.y
	self.position = radians(45.0)
	self.intersection = 30.0
	self.alignment = 0.0
	self.use_symmetry = False
	self.symmetry_pivot = 0.0
	self.bump_scale = 0.5
	self.taper = 0.0
	self.detalization = 32
	
	# Sizes
	# ----------------------------
	
	if self.gem_dim.y >= 2.5:
		self.diameter = 0.8
		self.z1 = 0.8
		self.z2 = 1.2
		
	elif self.gem_dim.y >= 1.7:
		self.diameter = 0.7
		self.z1 = 0.6
		self.z2 = 0.9
		
	elif self.gem_dim.y >= 1.5:
		self.diameter = 0.6
		self.z1 = 0.5
		self.z2 = 0.7
		
	elif self.gem_dim.y >= 1.2:
		self.diameter = 0.5
		self.z1 = 0.4
		self.z2 = 0.6
		
	elif self.gem_dim.y >= 1.0:
		self.diameter = 0.4
		self.z1 = 0.3
		self.z2 = 0.5
		
	# Shapes
	# ---------------------------
	
	if self.shape is gemlib.SHAPE_ROUND:
		self.number = 2
		self.position = radians(-30.0)
		self.intersection = 30.0
		
	elif self.shape is gemlib.SHAPE_TRIANGLE:
		self.number = 3
		self.position = radians(60.0)
		self.intersection = 0.0
		self.alignment = radians(10.0)
		
	elif self.shape is gemlib.SHAPE_SQUARE:
		self.intersection = -20.0
		
		if self.cut == "OCTAGON":
			self.intersection = 0.0
			
	elif self.shape is gemlib.SHAPE_RECTANGLE:
		self.number = 2
		self.position = radians(36.0)
		self.intersection = -20.0
		self.use_symmetry = True
		
		if self.cut == "BAGUETTE":
			self.position = radians(29.0)
			self.intersection = -10.0
			
	elif self.shape is gemlib.SHAPE_FANTASY:
		self.number = 2
		self.position = radians(0.0)
		self.intersection = 0.0
		self.alignment = radians(10.0)
		
		if self.cut == "OVAL":
			self.position = radians(30.0)
			self.intersection = 40.0 
			self.use_symmetry = True
			
		elif self.cut == "HEART":
			self.number = 3
			self.position = radians(60.0)
			self.intersection = -10.0
			
		elif self.cut == "PEAR":
			self.number = 1
			self.position = radians(50.0)
			self.intersection = 40.0
			self.use_symmetry = True
			self.symmetry_pivot = radians(-90.0) 
