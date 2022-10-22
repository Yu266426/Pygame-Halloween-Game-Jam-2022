from data.modules.constants import TILE_SIZE


def get_tiled_pos(pos):
	return int(pos[0] // TILE_SIZE), int(pos[1] // TILE_SIZE)
