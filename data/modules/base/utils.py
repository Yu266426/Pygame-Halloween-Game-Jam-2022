from data.modules.base.constants import TILE_SIZE


def get_tiled_pos(pos):
	return int(pos[0] // TILE_SIZE), int(pos[1] // TILE_SIZE)


def man_dist(pos1, pos2):
	return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
