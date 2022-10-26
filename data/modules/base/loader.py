import os

import pygame.image

from data.modules.base.constants import SCALE
from data.modules.base.file import ASSET_DIR


class Loader:
	images: dict[str, pygame.Surface] = {}
	sounds: dict[str, pygame.mixer.Sound] = {}

	@classmethod
	def load(cls):
		for _, _, files in os.walk(ASSET_DIR):
			for file in files:
				if file.endswith(".png"):
					file_name = file[:-4]
					image = pygame.image.load(os.path.join(ASSET_DIR, file)).convert_alpha()
					cls.images[file_name] = pygame.transform.scale(image, (image.get_width() * SCALE, image.get_height() * SCALE))
				elif file.endswith(".wav"):
					file_name = file[:-4]
					cls.sounds[file_name] = pygame.mixer.Sound(os.path.join(ASSET_DIR, file))
