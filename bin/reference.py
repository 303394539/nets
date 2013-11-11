# -*- coding:utf-8 -*-

class Reference(object):
	def __init__(self,*arg,**kvargs):
		for k,v in kvargs.items():
			setattr(self,k,v)
