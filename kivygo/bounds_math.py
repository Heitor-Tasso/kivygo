
from math import sin, cos
from array import array
peers = {}


def scale(points, length, width, height):
	for h in range(0, length, 2):
		points[h] = points[h] * width
		points[h+1] = points[h+1] * height


def move(points, length, pos0, pos1):
	for i in range(0, length, 2):
		points[i] = points[i] + pos0
		points[i+1] = points[i+1] + pos1


def rotate(points, length, angle, orig0, orig1):
	c = cos(angle)
	s = sin(angle)

	for j in range(0, length, 2):
		points[j] = points[j] - orig0
		points[j+1] = points[j+1] - orig1
		pj = points[j]
		points[j] = pj * c - points[j+1] * s
		points[j+1] = pj * s + points[j+1] * c
		points[j] = points[j] + orig0
		points[j+1] = points[j+1] + orig1


def calc_segboxes(points, polids, ptids, plens, length, bbox, blefts, bbotts, brghts, btops):
	for k in range(0, length, 2):
		k1 = k + 1
		off = plens[polids[k]] * 2 - 2
		if ptids[k] < plens[polids[k]] - 1:
			k2 = k1 + 1
			k3 = k2 + 1
		else:
			k2 = k - off
			k3 = k2 + 1

		blefts[k] = points[k] if points[k] <= points[k2] else points[k2]
		bbotts[k] = points[k1] if points[k1] <= points[k3] else points[k3]
		brghts[k] = points[k] if points[k] >= points[k2] else points[k2]
		btops[k] = points[k1] if points[k1] >= points[k3] else points[k3]

		if blefts[k] < bbox[0]:
			bbox[0] = blefts[k]

		if brghts[k] > bbox[2]:
			bbox[2] = brghts[k]

		if bbotts[k] < bbox[1]:
			bbox[1] = bbotts[k]

		if btops[k] > bbox[3]:
			bbox[3] = btops[k]


def calc_polboxes(points, plens, bbox, blefts, bbotts, brghts, btops):
	strt = 0
	for p in range(len(plens)):
		left = float("inf")
		bottom = float("inf")
		right = 0.
		top = 0.
		for l in range(strt, strt + plens[p] * 2, 2):
			l1 = l + 1

			if points[l] < left:
				left = points[l]

			if points[l] > right:
				right = points[l]

			if points[l1] < bottom:
				bottom = points[l1]

			if points[l1] > top:
				top = points[l1]

		if left < bbox[0]:
			bbox[0] = left

		if right > bbox[2]:
			bbox[2] = right

		if bottom < bbox[1]:
			bbox[1] = bottom

		if top > bbox[3]:
			bbox[3] = top

		blefts[p] = left
		bbotts[p] = bottom
		brghts[p] = right
		btops[p] = top

		strt = strt + plens[p] * 2


def intersection_w(pts, ptids, plens, opens, t_box):
	t_pts = [
		t_box[0], t_box[1], t_box[2], t_box[1],
		t_box[2], t_box[3], t_box[0], t_box[3]
	]
	o = 0
	strt = 0

	for p in range(len(plens)):
		if p in opens:
			o = 2

		for i in range(strt, strt + plens[p] * 2 - o, 2):
			i1 = i + 1
			off = plens[p] * 2 - 2
			if ptids[i] < plens[p] - 1:
				i2 = i1 + 1
				i3 = i2 + 1
			else:
				i2 = i - off
				i3 = i2 + 1

			v10 = pts[i]
			v11 = pts[i1]
			v20 = pts[i2]
			v21 = pts[i3]

			for j in range(0, 8, 2):
				j1 = j + 1
				t_off = 6
				if j < 6:
					j2 = j1 + 1
					j3 = j2 + 1
				else:
					j2 = j - t_off
					j3 = j2 + 1

				v30 = t_pts[j]
				v31 = t_pts[j1]
				v40 = t_pts[j2]
				v41 = t_pts[j3]

				# Segment intersection detection method:
				# If the vertices v1 and v2 are not on opposite sides of the
				# segment v3, v4, or the vertices v3 and v4 are not on
				# opposite sides of the segment v1, v2, there's no
				# intersection.
				if ((v40 - v30) * (v11 - v31) - (v10 - v30) * (v41 - v31) > 0) == \
						((v40 - v30) * (v21 - v31) - (v20 - v30) * (v41 - v31) > 0):
					continue

				elif ((v20 - v10) * (v31 - v11) - (v30 - v10) * (v21 - v11) > 0) == \
						((v20 - v10) * (v41 - v11) - (v40 - v10) * (v21 - v11) > 0):
					continue

				return [p, ptids[i], 0, j/2]

		strt = strt + plens[p] * 2
	return False


def intersection_f(pts, ptids, plens, opens, t_pts, t_polis, t_ptis, t_plens):
	o = 0
	strt = 0
	for p in range(len(plens)):
		if p in opens:
			o = 2

		for i in range(strt, strt + plens[p] * 2 - o, 2):
			i1 = i + 1
			off = plens[p] * 2 - 2
			if ptids[i] < plens[p] - 1:
				i2 = i1 + 1
				i3 = i2 + 1
			else:
				i2 = i - off
				i3 = i2 + 1

			v10 = pts[i]
			v11 = pts[i1]
			v20 = pts[i2]
			v21 = pts[i3]

			t_strt = 0
			for t_p in range(len(t_plens)):
				for j in range(t_strt, t_strt + t_plens[t_p] * 2, 2):
					j1 = j + 1
					t_off = t_plens[t_polis[j]] * 2 - 2
					if t_ptis[j] < t_plens[t_polis[j]] - 1:
						j2 = j1 + 1
						j3 = j2 + 1
					else:
						j2 = j - t_off
						j3 = j2 + 1
					v30 = t_pts[j]
					v31 = t_pts[j1]
					v40 = t_pts[j2]
					v41 = t_pts[j3]

					# Segment intersection detection method:
					# If the vertices v1 and v2 are not on opposite sides of
					# the segment v3, v4, or the vertices v3 and v4 are not
					# on opposite sides of the segment v1, v2, there's no
					# intersection.
					if ((v40 - v30) * (v11 - v31) - (v10 - v30) * (v41 - v31) > 0) == \
							((v40 - v30) * (v21 - v31) - (v20 - v30) * (v41 - v31) > 0):
						continue

					elif ((v20 - v10) * (v31 - v11) - (v30 - v10) * (v21 - v11) > 0) == \
							((v20 - v10) * (v41 - v11) - (v40 - v10) * (v21 - v11) > 0):
						continue

					return [p, ptids[i], t_p, t_ptis[j]]

				t_strt = t_strt + t_plens[t_p] * 2

		strt = strt + plens[p] * 2
	return False


def intersection(pts, ptids, le, plens, opens, lefts, botts, rghts, tops,
				 t_box, t_pts, t_ptis, t_le, t_plens, t_opens, t_lefts,
				 t_botts, t_rghts, t_tops):
	o = 0
	t_o = 0
	strt = 0
	for p in range(len(plens)):
		if p in opens:
			o = 2

		for i in range(strt, strt + plens[p] * 2 - o, 2):
			if rghts[i] < t_box[0]:
				continue

			if lefts[i] > t_box[2]:
				continue

			if tops[i] < t_box[1]:
				continue

			if botts[i] > t_box[3]:
				continue

			i1 = i + 1
			off = plens[p] * 2 - 2
			if ptids[i] < plens[p] - 1:
				i2 = (i1 + 1) % le
				i3 = i2 + 1
			else:
				i2 = i - off
				i3 = i2 + 1

			v10 = pts[i]
			v11 = pts[i1]
			v20 = pts[i2]
			v21 = pts[i3]

			t_strt = 0
			for t_p in range(len(t_plens)):
				if t_p in t_opens:
					t_o = 2
				for j in range(t_strt, t_strt + t_plens[t_p] * 2 - t_o, 2):
					if rghts[i] < t_lefts[j]:
						continue

					if lefts[i] > t_rghts[j]:
						continue

					if tops[i] < t_botts[j]:
						continue

					if botts[i] > t_tops[j]:
						continue

					j1 = j + 1
					t_off = t_plens[t_p] * 2 - 2
					if t_ptis[j] < t_plens[t_p] - 1:
						j2 = (j1+1) % t_le
						j3 = j2 + 1
					else:
						j2 = j - t_off
						j3 = j2 + 1

					v30 = t_pts[j]
					v31 = t_pts[j1]
					v40 = t_pts[j2]
					v41 = t_pts[j3]

					# Segment intersection detection method:
					# If the vertices v1 and v2 are not on opposite sides of
					# the segment v3, v4, or the vertices v3 and v4 are not
					# on opposite sides of the segment v1, v2, there's no
					# intersection.
					if ((v40 - v30) * (v11 - v31) - (v10 - v30) * (v41 - v31) > 0) == \
							((v40 - v30) * (v21 - v31) - (v20 - v30) * (v41 - v31) > 0):
						continue

					elif ((v20 - v10) * (v31 - v11) - (v30 - v10) * (v21 - v11) > 0) == \
							((v20 - v10) * (v41 - v11) - (v40 - v10) * (v21 - v11) > 0):
						continue

					return [p, ptids[i], t_p, t_ptis[j]]

				t_strt = t_strt + t_plens[t_p] * 2

		strt = strt + plens[p] * 2
	return False


def membership(pts, plens, lefts, botts, rghts, tops,
			   t_box, t_pts, t_polis, t_le):
	strt = 0
	for p, pl in enumerate(plens):
		# Preliminary 1: pol's bbox vs widget's bbox.
		if rghts[p] < t_box[0]:
			strt = strt + pl * 2
			continue

		if lefts[p] > t_box[2]:
			strt = strt + pl * 2
			continue

		if tops[p] < t_box[1]:
			strt = strt + pl * 2
			continue

		if botts[p] > t_box[3]:
			strt = strt + pl * 2
			continue

		for k in range(0, t_le, 2):
			x = t_pts[k]
			y = t_pts[k + 1]
			# Preliminary 2: pol's bbox vs widget's points to filter out.
			if rghts[p] < x:
				continue

			if lefts[p] > x:
				continue

			if tops[p] < y:
				continue

			if botts[p] > y:
				continue

			# Point-in-polygon (oddeven) collision detection method:
			# Checking the membership of each poby assuming a ray at 0 angle
			# from that poto infinity (through window right) and counting
			# the number of times that this ray crosses the polygon line.
			# If this number is odd, the pois inside; if it's even, the pois
			# outside.
			c = 0
			j = strt + pl * 2 - 2
			for i in range(strt, strt + pl * 2, 2):
				x1 = pts[j]
				y1 = pts[j+1]
				x2 = pts[i]
				y2 = pts[i+1]
				if (((y2 > y) != (y1 > y))
						and x < (x1 - x2) * (y - y2) / (y1 - y2) + x2):
					c = not c
				j = i

			if c:
				return [p, t_polis[k]]

		strt = strt + pl * 2
	return False


def collide_bounds(rid, wid, frame='bounds', tframe='bounds'):

	try:
		this_box = peers[rid]['bbox']
	except KeyError:
		return False

	try:
		that_box = peers[wid]['bbox']
	except TypeError:
		that_box = wid

	try:
		if this_box[2] < that_box[0]:
			return False
	except IndexError:
		return False

	if this_box[0] > that_box[2]:
		return False

	if this_box[3] < that_box[1]:
		return False

	if this_box[1] > that_box[3]:
		return False

	bounds = peers[rid][frame]
	try:
		tbounds = peers[wid][tframe]
	except TypeError:
		return intersection_w(bounds['points'], bounds['pt_ids'],
							  bounds['pol_lens'], bounds['opens'], that_box)

	if not peers[rid]['seg']:
		return membership(bounds['points'], bounds['pol_lens'],
						  bounds['lefts'], bounds['botts'], bounds['rights'],
						  bounds['tops'], that_box, tbounds['points'],
						  tbounds['pol_ids'],
						  tbounds['length'])

	if peers[wid]['seg']:
		return intersection(bounds['points'], bounds['pt_ids'],
							bounds['length'], bounds['pol_lens'],
							bounds['opens'], bounds['lefts'],
							bounds['botts'], bounds['rights'],
							bounds['tops'], that_box,
							tbounds['points'], tbounds['pt_ids'],
							tbounds['length'], tbounds['pol_lens'],
							tbounds['opens'], tbounds['lefts'],
							tbounds['botts'], tbounds['rights'],
							tbounds['tops'])

	return intersection_f(bounds['points'], bounds['pt_ids'],
						  bounds['pol_lens'], bounds['opens'],
						  tbounds['points'], tbounds['pol_ids'],
						  tbounds['pt_ids'], tbounds['pol_lens'])


def point_in_bounds(x, y, rid, frame='bounds'):
	'''"Oddeven" point-in-polygon method:
	Checking the membership of touch poby assuming a ray at 0 angle
	from that poto infinity (through window right) and counting the
	number of polygon sides that this ray crosses. If this number is
	odd, the pois inside; if it's even, the pois outside.
	'''
	bounds = peers[rid][frame]
	strt = 0
	for r, rang in enumerate(bounds['pol_lens']):
		c = 0
		j = strt + rang * 2 - 2
		for i in range(strt, strt + rang * 2, 2):
			x1, y1 = bounds['points'][j], bounds['points'][j+1]
			x2, y2 = bounds['points'][i], bounds['points'][i+1]
			if (((y2 > y) != (y1 > y)) and
					x < (x1 - x2) * (y - y2) / (y1 - y2) + x2):
				c = not c
			j = i

		if c:
			return c
		strt = strt + rang * 2

	return False


def update_bounds(motion, angle, origin, rid, frame='bounds'):
	'''Updating the elements of the collision detection checks.
	'''
	try:
		bounds = peers[rid][frame]
	except TypeError:
		return None

	if motion:
		move(bounds['points'], bounds['length'], motion[0], motion[1])

	if angle:
		rotate(bounds['points'], bounds['length'], angle, origin[0],
			   origin[1])

	bbox = array('d', [float("inf"), float("inf"), 0., 0.])

	if peers[rid]['seg']:
		calc_segboxes(bounds['points'], bounds['pol_ids'], bounds['pt_ids'],
					  bounds['pol_lens'], bounds['length'], bbox,
					  bounds['lefts'], bounds['botts'], bounds['rights'],
					  bounds['tops'])
	else:
		calc_polboxes(bounds['points'], bounds['pol_lens'], bbox,
					  bounds['lefts'], bounds['botts'], bounds['rights'],
					  bounds['tops'])

	peers[rid]['bbox'] = bbox


def aniupdate_bounds(motion, pos, angle, origin, rid, frame='bounds'):
	'''Updating the elements of the collision detection checks,
	in case of an animation.
	'''
	try:
		bounds = peers[rid][frame]
	except TypeError:
		return None

	if motion:
		bounds['mov_pts'][:] = bounds['sca_pts']
		move(bounds['mov_pts'], bounds['length'], pos[0], pos[1])
		bounds['points'][:] = bounds['mov_pts']

	if angle:
		bounds['points'][:] = bounds['mov_pts']
		rotate(bounds['points'], bounds['length'], angle, origin[0], origin[1])

	bbox = array('d', [float("inf"), float("inf"), 0.0, 0.0])

	if peers[rid]['seg']:
		calc_segboxes(bounds['points'], bounds['pol_ids'], bounds['pt_ids'],
					  bounds['pol_lens'], bounds['length'], bbox,
					  bounds['lefts'], bounds['botts'], bounds['rights'],
					  bounds['tops'])
	else:
		calc_polboxes(bounds['points'], bounds['pol_lens'], bbox,
					  bounds['lefts'], bounds['botts'], bounds['rights'],
					  bounds['tops'])

	peers[rid]['bbox'] = bbox


def resize(width, height, rid):
	for k, frame in peers[rid].items():
		if k == 'bounds':
			bounds = peers[rid]['bounds']
			bounds['points'][:] = bounds['hints']
			scale(bounds['points'], bounds['length'], width, height)
			break
	else:
		for k, frame in peers[rid].items():
			if k != 'bbox' and k != 'vbbox' and k != 'hhits' and k != 'seg' \
					and k != 'friendly':
				frame['points'][:] = frame['hints']
				scale(frame['points'], frame['length'], width, height)


def aniresize(width, height, rid):
	for k, frame in peers[rid].items():
		if k == 'bounds':
			bounds = peers[rid]['bounds']
			bounds['sca_pts'][:] = bounds['hints']
			scale(bounds['sca_pts'], bounds['length'], width, height)
			break
	else:
		for k, frame in peers[rid].items():
			if k != 'bbox' and k != 'seg' and k != '':
				frame['sca_pts'][:] = frame['hints']
				scale(frame['sca_pts'], frame['length'], width, height)


def define_frame(frame, opens, seg_mode, bounds, ani=False):
	for p in range(len(frame)):
		pol = frame[p]
		plen = len(pol)
		array.extend(bounds['pol_lens'], array('i', [plen]))
		for i in range(plen):
			array.extend(bounds['hints'], array('d', [pol[i][0], pol[i][1]]))
			array.extend(bounds['pol_ids'], array('i', [p, p]))
			array.extend(bounds['pt_ids'], array('i', [i, i]))
			bounds['length'] += 2

	if seg_mode:
		length = bounds['length']
	else:
		length = len(bounds['pol_lens'])
	bounds['lefts'] = array('d', [float("inf")] * length)
	bounds['botts'] = array('d', [float("inf")] * length)
	bounds['rights'] = array('d', [0.] * length)
	bounds['tops'] = array('d', [0.] * length)

	if seg_mode:
		bounds['opens'] = array('i', opens)

	if ani:
		bounds['mov_pts'][:] = bounds['sca_pts'][:] = bounds['hints']
	bounds['points'][:] = bounds['hints']


def define_bounds(custom_bounds, open_bounds, segment_mode, rid, pc):
	'''Organising the data from the user's [self.custom_bounds] hints.
	The [pc] parameter is not used. It's here for compatibility with the
	equivalent function in the cython module.
	'''
	frames = {}

	if isinstance(custom_bounds, dict):   # Animation case
		for key, frame in custom_bounds.items():
			bounds = {'hints': array('d'), 'sca_pts': array('d'),
					  'mov_pts': array('d'), 'points': array('d'),
					  'pol_ids': array('i'), 'pt_ids': array('i'),
					  'pol_lens': array('i'), 'length': 0}
			if isinstance(open_bounds, dict):
				opens = array('i', open_bounds[key])
			else:
				opens = array('i', open_bounds)

			define_frame(frame, opens, segment_mode, bounds, ani=True)

			frames[key] = bounds

	elif isinstance(custom_bounds, list):  # Single image case
		bounds = {'hints': array('d'), 'points': array('d'),
				  'pol_ids': array('i'), 'pt_ids': array('i'),
				  'pol_lens': array('i'), 'length': 0}
		define_frame(custom_bounds, open_bounds, segment_mode, bounds)

		frames['bounds'] = bounds

	frames['bbox'] = array('d', [])
	frames['seg'] = segment_mode

	peers[rid] = frames
