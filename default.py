# -*- coding: utf-8 -*-
from libmediathek4 import lm4
import resources.lib.jsonparser as jsonParser


class artekino(lm4):
	def __init__(self):
		self.defaultMode = 'main'

		self.modes = {
			'main':self.main,
			}	

		self.playbackModes = {
			'playVideo':self.playVideo,
			}

	def main(self):
		return jsonParser.getMovies()

	def playVideo(self):
		return jsonParser.getVideo(self.params['id'])

a = artekino()
a.action()