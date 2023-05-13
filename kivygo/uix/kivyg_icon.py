
from kivy.graphics import (
    Line as KivyLine,
    Color, Mesh,
)

from kivy.graphics.tesselator import (
    Tesselator, WINDING_ODD,
    TYPE_POLYGONS,
)

from svg.path.path import (
    Line, CubicBezier,
    Close, Move,
)

from kivygo.utils import (
    line_points, bezier_points,
    get_all_points, parse_svg,
    find_center,
)

from kivygo.animation import Animation
from svg.path import parse_path
from collections import OrderedDict


class Kivg():
    def __init__(self, widget, *args):
        """
        widget: widget to draw svg upon
        """
        self.b = widget
        self._fill = True  # Fill path with color after drawing
        self._LINE_WIDTH = 2
        self._LINE_COLOR = [0, 0, 0, 1]
        self._DUR = 0.02
        self.psf = ""  # Previous svg file - Don't re-find path for same file in a row

    def get_tess(self, shapes):
        tess = Tesselator()
        for shape in shapes:
            if len(shape) >= 3:
                tess.add_contour(shape)
        return tess

    def get_mesh(self, shapes):
        tess = self.get_tess(shapes)
        ret = tess.tesselate(WINDING_ODD, TYPE_POLYGONS)
        return tess.meshes

    def fill_up(self, shapes, color):
        meshes = self.get_mesh(shapes)
        with self.b.canvas:
            Color(*color[:3], getattr(self.b, "mesh_opacity"))
            for vertices, indices in meshes:
                Mesh(vertices=vertices, indices=indices, mode="triangle_fan")

    def fill_up_shapes(self, *args):
        for id_, closed_paths in self.closed_shapes.items():
            c = self.closed_shapes[id_]["color"]
            self.fill_up(closed_paths[id_ + "shapes"], c)

    def fill_up_shapes_anim(self, shapes, *args):
        for shape in shapes:
            c = shape[0]
            self.fill_up([shape[1]], c)

    def anim_on_comp(self, *args):
        self.curr_count += 1
        self.prev_shapes.append(self.curr_shape)
        if self.curr_count < len(self.all_anim):
            id_, a = self.all_anim[self.curr_count]
            setattr(self, "curr_id", id_)
            setattr(self, "curr_clr", self.closed_shapes[id_]["color"])
            a.bind(on_progress=self.track_progress)
            a.start(self.b)

    def shape_animate(self, svg_file, anim_config_list=[], on_complete=None):
        """
        svg_file: svg file name

        anim_config_list: a list of dicts with keys id_ to animate and from_, the direction of animation

        on_complete: optional function to call after total completion
        """
        self.draw(svg_file, from_shape_anim=True)
        setattr(self.b, "mesh_opacity", 1)

        self.all_anim = []
        self.curr_count = 0
        for i, config in enumerate(anim_config_list):
            anim_list = self._shape_animate(
                config["id_"],
                config.get("from_", None),
                config.get("t", "out_sine"),
                config.get("d", .3),
            )

            if anim_list:
                anim = anim_list[0]
                for a in anim_list[1:]:
                    anim &= a

                anim.bind(on_complete=self.anim_on_comp)
                self.all_anim.append((config["id_"], anim))
            else:
                setattr(self, "curr_id", config["id_"])
                setattr(self, "curr_clr",
                        self.closed_shapes[config["id_"]]["color"])
                self.track_progress()

        id_, a = self.all_anim[0]
        setattr(self, "curr_id", id_)
        setattr(self, "curr_clr", self.closed_shapes[id_]["color"])

        a.cancel_all(self.b)
        a.bind(on_progress=self.track_progress)

        if on_complete:
            self.all_anim[-1][1].bind(on_complete=on_complete)

        a.start(self.b)

    def _shape_animate(self, id_, from_, t, d):
        line_count = 0
        bezier_count = 0
        anim_list = []
        self.prev_shapes = []
        self.curr_shape = []
        if self.closed_shapes.get(id_, None):
            tmp = []
            for s in self.closed_shapes[id_][id_ + "paths"]:
                tmp2 = []
                for e in s:
                    if isinstance(e, Line):
                        lp = line_points(
                            e, *self.b.size, *self.b.pos,
                            *self.sw_size, self.sf
                        )

                        tmp2.append([
                            (lp[0], lp[1]),
                            (lp[2], lp[3])
                        ])

                    if isinstance(e, CubicBezier):
                        bp = bezier_points(
                            e, *self.b.size, *self.b.pos,
                            *self.sw_size, self.sf
                        )

                        tmp2.append([
                            (bp[0], bp[1]),
                            (bp[2], bp[3]),
                            (bp[4], bp[5]),
                            (bp[6], bp[7])
                        ])

                tmp.append(tmp2)

            l = []
            for each in tmp:
                for e in each:
                    for i in e:
                        if from_ in ("left", "right", "center_x"):
                            l.append(i[0])
                        else:
                            l.append(i[1])

            base_point = 0
            if from_ in ("top", "right"):
                # rightmost/topmost point to start animation from
                base_point = max(l)
            elif from_ in ("left", "bottom"):
                # leftmost/bottommost point to start animation from
                base_point = min(l)
            elif from_ in ("center_x", "center_y"):
                base_point = find_center(sorted(l))

            for each in tmp:
                for e in each:
                    # Line
                    if len(e) == 2:
                        nm_mesh = f"{id_}_mesh_line{line_count}"
                        value_sx = value_sy = base_point
                        value_ex = value_ey = base_point

                        if from_ in ("left", "right", "center_x"):
                            value_sx = e[0][0]
                            value_ex = e[1][0]

                            anim_list.append(
                                Animation(
                                    d=d, t=t,
                                    **{
                                        f"{nm_mesh}_start_x": e[0][0],
                                        f"{nm_mesh}_end_x": e[1][0]
                                    }
                                )
                            )

                        if from_ in ("top", "bottom", "center_y"):
                            value_sy = e[0][1]
                            value_ey = e[1][1]

                            anim_list.append(
                                Animation(
                                    d=d, t=t,
                                    **{
                                        f"{nm_mesh}_start_y": e[0][1],
                                        f"{nm_mesh}_end_y": e[1][1]
                                    }
                                )
                            )

                        setattr(self.b, f"{nm_mesh}_start_x", value_sx)
                        setattr(self.b, f"{nm_mesh}_start_y", value_sy)
                        setattr(self.b, f"{nm_mesh}_end_x", value_ex)
                        setattr(self.b, f"{nm_mesh}_end_y", value_ey)
                        line_count += 1

                    # Bezier
                    if len(e) == 4:
                        nm_mesh = f"{id_}_mesh_bezier{bezier_count}"

                        value_sx = value_sy = base_point
                        value_ex = value_ey = base_point
                        value_ctrl_1x = value_ctrl_1y = base_point
                        value_ctrl_2x = value_ctrl_2y = base_point

                        if from_ in ("left", "right", "center_x"):
                            value_sx = e[0][0]
                            value_ctrl_1x = e[1][0]
                            value_ctrl_2x = e[2][0]
                            value_ex = e[3][0]

                            anim_list.append(
                                Animation(
                                    d=d, t=t,
                                    **{
                                        f"{nm_mesh}_start_x": e[0][0],
                                        f"{nm_mesh}_control1_x": e[1][0],
                                        f"{nm_mesh}_control2_x": e[2][0],
                                        f"{nm_mesh}_end_x": e[3][0]
                                    }
                                )
                            )

                        if from_ in ("top", "bottom", "center_y"):
                            value_sy = e[0][1]
                            value_ctrl_1y = e[1][1]
                            value_ctrl_2y = e[2][1]
                            value_ey = e[3][1]

                            anim_list.append(
                                Animation(
                                    d=d, t=t,
                                    **{
                                        f"{nm_mesh}_start_y": e[0][1],
                                        f"{nm_mesh}_control1_y": e[1][1],
                                        f"{nm_mesh}_control2_y": e[2][1],
                                        f"{nm_mesh}_end_y": e[3][1]
                                    }
                                )
                            )

                        setattr(self.b, f"{nm_mesh}_start_x", value_sx)
                        setattr(self.b, f"{nm_mesh}_start_y", value_sy)
                        setattr(self.b, f"{nm_mesh}_control1_x", value_ctrl_1x)
                        setattr(self.b, f"{nm_mesh}_control1_y", value_ctrl_1y)
                        setattr(self.b, f"{nm_mesh}_control2_x", value_ctrl_2x)
                        setattr(self.b, f"{nm_mesh}_control2_y", value_ctrl_2y)
                        setattr(self.b, f"{nm_mesh}_end_x", value_ex)
                        setattr(self.b, f"{nm_mesh}_end_y", value_ey)
                        bezier_count += 1

            setattr(self, f"{id_}_tmp", tmp)
            return anim_list

    def track_progress(self, *args):

        id_ = getattr(self, "curr_id")
        shape_list = []
        line_count = 0
        bezier_count = 0

        for each in getattr(self, "{}_tmp".format(id_)):
            for e in each:
                # Line
                if len(e) == 2:
                    nm_mesh = f"{id_}_mesh_line{line_count}"

                    shape_list.extend([
                        getattr(self.b, f"{nm_mesh}_start_x"),
                        getattr(self.b, f"{nm_mesh}_start_y"),
                        getattr(self.b, f"{nm_mesh}_end_x"),
                        getattr(self.b, f"{nm_mesh}_end_y")
                    ])
                    line_count += 1

                # Bezier
                if len(e) == 4:
                    nm_mesh = f"{id_}_mesh_bezier{bezier_count}"
                    shape_list.extend(
                        get_all_points(
                            (getattr(self.b, f"{nm_mesh}_start_x"), getattr(
                                self.b, f"{nm_mesh}_start_y")),
                            (getattr(self.b, f"{nm_mesh}_control1_x"), getattr(
                                self.b, f"{nm_mesh}_control1_y")),
                            (getattr(self.b, f"{nm_mesh}_control2_x"), getattr(
                                self.b, f"{nm_mesh}_control2_y")),
                            (getattr(self.b, f"{nm_mesh}_end_x"), getattr(
                                self.b, f"{nm_mesh}_end_y"))
                        )
                    )
                    bezier_count += 1

        self.b.canvas.clear()
        self.curr_shape = (getattr(self, "curr_clr"), shape_list)
        s = [*self.prev_shapes, self.curr_shape]
        self.fill_up_shapes_anim(s)

    def draw(self, svg_file, animate=False, anim_type="seq", *args, **kwargs):
        """
        Function to animate

        Call this function with an svg file name to animate that svg

        ------------
        Extra arguments:

        fill: Whether to fill the drawing at the end using same png, defaults true,
         unexpected result if png with same name is not available

        outline_width: Line width for drawing, default 2

        line_color: Line Color for drawing, default [0,0,0,1]

        dur: Duration of each small path drawing animation, default .02

        anim_type: "seq"/"par" for sequence/parallel
        """
        self.fill = kwargs.get("fill", self._fill)
        self.outline_width = kwargs.get("outline_width", self._LINE_WIDTH)
        self.LINE_COLOR = kwargs.get("line_color", self._LINE_COLOR)
        self.DUR = kwargs.get("dur", self._DUR)
        from_shape_anim = kwargs.get("from_shape_anim", False)
        anim_type = (anim_type) if anim_type in {"seq", "par"} else ("seq")

        self.sf = svg_file
        if self.sf != self.psf:
            self.sw_size, path_strings = parse_svg(svg_file)

            self.path = []
            self.closed_shapes = OrderedDict()

            for path_string, id_, clr in path_strings:

                move_found = False
                tmp = []
                self.closed_shapes[id_] = dict()
                self.closed_shapes[id_][f"{id_}paths"] = []

                # for drawing meshes
                self.closed_shapes[id_][f"{id_}shapes"] = []
                self.closed_shapes[id_]["color"] = clr
                _path = parse_path(path_string)

                for e in _path:
                    self.path.append(e)

                    if isinstance(e, Close) or (isinstance(e, Move) and move_found):
                        self.closed_shapes[id_][f"{id_}paths"].append(tmp)
                        move_found = False

                    # shape started
                    if isinstance(e, Move):
                        tmp = []
                        move_found = True

                    if not isinstance(e, Move) and move_found:
                        tmp.append(e)

            self.psf = self.sf

        anim_list = self._calc_paths(animate)
        if not from_shape_anim:
            if animate:
                anim = anim_list[0]
                for a in anim_list[1:]:
                    if anim_type == "seq":
                        anim += a
                    else:
                        anim &= a

            if self.fill:
                setattr(self.b, "mesh_opacity", not bool(animate))

                if animate:
                    fill_anim = Animation(d=0.4, mesh_opacity=1)
                    fill_anim.bind(on_progress=self.fill_up_shapes)
                    anim += fill_anim

            if animate:
                anim.cancel_all(self.b)
                anim.bind(on_progress=self.update_canvas)
                anim.start(self.b)
            elif not self.fill:
                self.update_canvas()
            else:
                self.b.canvas.clear()
                self.fill_up_shapes()

    def _calc_paths(self, animate):

        line_count = 0
        bezier_count = 0
        anim_list = []
        for id_, closed_paths in self.closed_shapes.items():
            # TODO: Support for other svg shapes like Arc, Circle, Text etc.

            for s in closed_paths[id_ + "paths"]:
                tmp = []

                for e in s:
                    if isinstance(e, Line):

                        nm_mesh = f"line{line_count}"

                        lp = line_points(
                            e, *self.b.size, *self.b.pos,
                            *self.sw_size, self.sf
                        )

                        setattr(self.b, f"{nm_mesh}_start_x", lp[0])
                        setattr(self.b, f"{nm_mesh}_start_y", lp[1])
                        setattr(self.b, f"{nm_mesh}_end_x",
                                lp[0] if animate else lp[2])
                        setattr(self.b, f"{nm_mesh}_end_y",
                                lp[1] if animate else lp[3])
                        setattr(self.b, f"{nm_mesh}_width",
                                1 if animate else self.outline_width)

                        if animate:
                            anim_list.append(
                                Animation(
                                    d=self.DUR,
                                    **{
                                        f"{nm_mesh}_end_x": lp[2],
                                        f"{nm_mesh}_end_y": lp[3],
                                        f"{nm_mesh}_width": self.outline_width
                                    }
                                )
                            )
                        line_count += 1
                        tmp.extend(lp)

                    if isinstance(e, CubicBezier):

                        nm_mesh = f"bezier{bezier_count}"

                        bp = bezier_points(
                            e, *self.b.size, *self.b.pos,
                            *self.sw_size, self.sf
                        )

                        setattr(self.b, f"{nm_mesh}_start_x", bp[0])
                        setattr(self.b, f"{nm_mesh}_start_y", bp[1])
                        setattr(self.b, f"{nm_mesh}_control1_x",
                                bp[0] if animate else bp[2])
                        setattr(self.b, f"{nm_mesh}_control1_y",
                                bp[1] if animate else bp[3])
                        setattr(self.b, f"{nm_mesh}_control2_x",
                                bp[0] if animate else bp[4])
                        setattr(self.b, f"{nm_mesh}_control2_y",
                                bp[1] if animate else bp[5])
                        setattr(self.b, f"{nm_mesh}_end_x",
                                bp[0] if animate else bp[6])
                        setattr(self.b, f"{nm_mesh}_end_y",
                                bp[1] if animate else bp[7])
                        setattr(self.b, f"{nm_mesh}_width",
                                1 if animate else self.outline_width)

                        if animate:
                            anim_list.append(
                                Animation(
                                    d=self.DUR,
                                    **{
                                        f"{nm_mesh}_control1_x": bp[2],
                                        f"{nm_mesh}_control1_y": bp[3],
                                        f"{nm_mesh}_control2_x": bp[4],
                                        f"{nm_mesh}_control2_y": bp[5],
                                        f"{nm_mesh}_end_x": bp[6],
                                        f"{nm_mesh}_end_y": bp[7],
                                        f"{nm_mesh}_width": self.outline_width
                                    }
                                )
                            )
                        bezier_count += 1
                        tmp.extend(
                            get_all_points(
                                (bp[0], bp[1]),
                                (bp[2], bp[3]),
                                (bp[4], bp[5]),
                                (bp[6], bp[7]),
                            )
                        )

                if tmp not in closed_paths[f"{id_}shapes"]:
                    closed_paths[f"{id_}shapes"].append(tmp)

        return anim_list

    def update_canvas(self, *args, **kwargs):
        self.b.canvas.clear()

        with self.b.canvas:
            Color(*self.LINE_COLOR)

            line_count = 0
            bezier_count = 0

            # Draw svg
            for e in self.path:

                if isinstance(e, Line):

                    nm_mesh = f"line{line_count}"

                    KivyLine(
                        points=[
                            getattr(self.b, f"{nm_mesh}_start_x"),
                            getattr(self.b, f"{nm_mesh}_start_y"),
                            getattr(self.b, f"{nm_mesh}_end_x"),
                            getattr(self.b, f"{nm_mesh}_end_y"),
                        ],
                        width=getattr(self.b, f"{nm_mesh}_width")
                    )

                    line_count += 1

                if isinstance(e, CubicBezier):

                    nm_mesh = f"bezier{bezier_count}"

                    KivyLine(
                        bezier=[
                            getattr(self.b, f"{nm_mesh}_start_x"),
                            getattr(self.b, f"{nm_mesh}_start_y"),
                            getattr(self.b, f"{nm_mesh}_control1_x"),
                            getattr(self.b, f"{nm_mesh}_control1_y"),
                            getattr(self.b, f"{nm_mesh}_control2_x"),
                            getattr(self.b, f"{nm_mesh}_control2_y"),
                            getattr(self.b, f"{nm_mesh}_end_x"),
                            getattr(self.b, f"{nm_mesh}_end_y"),
                        ],
                        width=getattr(self.b, f"{nm_mesh}_width"),
                    )

                    bezier_count += 1
