# MINIMAP / NAVIGATOR for NODE EDITOR
#
# A rectangular overview of all of the nodes is shown in the top right
#
# Installation:
#   1: Go to the scripting workspace
#   2: Add a "new text" at the top
#   3: Paste in this file, or select this file in the browser if it was downloaded
#   4: Hit "Run Script" at the top
#
# Since this is not an addon, the navigator will only be shown until this .blend is closed.
# To use it again when reloading a save, just hit the run button
#
# Usage: Click and drag on the navigator to move the viewport
#

__author__ = "Evan Boldt"
__license__ = "GPL"
__email__ = "evan.d.boldt@gmail.com"

import bpy
import math

bl_info = {
    "name": "Minimap for Node Editor",
    "description": "Adds a minimap to node editor that shows all nodes at once.",
    "location": "Top right of shader editor or compsitor node edit views.",
    "tracker_url": "https://github.com/echowarp/blender_node_editor_navigation",
    "blender": (2, 80, 0),
    "category": "Node",
    "version": (1,0),
    "author": "Evan Boldt",
    "support": "TESTING"
}


from bpy.types import (
    GizmoGroup,
    Gizmo
)


class gizmoSimpleBox(Gizmo):
    bl_idname = "NODE_EDITOR_GT_simplebox"

    def draw(self, context):
        self.draw_preset_box( self.matrix_basis )

    def setup(self):
        self.use_draw_modal = True
        self.use_grab_cursor = False
        self.use_event_handle_all = False




class gizmoMousePad(Gizmo):
    bl_idname = "NODE_EDITOR_GT_mousepad"

    def draw(self, context):
        self.draw_preset_box( self.matrix_basis )

    def draw_select(self, context, select_id):
        self.draw_preset_box( self.matrix_basis )

    def test_inside(self, x, y, debug=False):
        cx = self.matrix_basis[0][3]
        cy = self.matrix_basis[1][3]

        w2 = self.matrix_basis[0][1]
        h2 = self.matrix_basis[1][0]

        lx = cx - w2
        rx = cx + w2
        ty = cy - h2
        by = cy + h2

        inside = (lx <= x <= rx) and (ty <= y <= by)

        if debug:
            print("Test Select: {} < {} < {}   and   {} < {} < {} || {}".format(lx, x, rx, ty, y, by, inside))
        return inside


    def test_select(self, context, location):
        x = location[0]
        y = location[1]

        return self.test_inside(x,y)

    def invoke(self, context, event):
        x = event.mouse_region_x
        y = event.mouse_region_y

        inside = self.test_inside(x, y)

        if inside and event.type == "LEFTMOUSE" and event.value == "PRESS":
            return {'RUNNING_MODAL'}
        else:
            return {'PASS_THROUGH'}

    def setup(self):
        self.use_grab_cursor = True
        self.use_event_handle_all = False


    def exit(self, context, cancel):
        context.area.header_text_set(None)
        # TODO:
        # if cancel:

    def refresh(self, context):
        pass

    def modal(self, context, event, tweak):
        dx = event.mouse_x - event.mouse_prev_x
        dy = event.mouse_y - event.mouse_prev_y

        # Tweak = {'PRECISE'} or {'SNAP'}
        if tweak == {"PRECISE"}:
            dx = dx / 10
            dy = dy / 10

        bpy.ops.view2d.pan(deltax=dx, deltay=dy)

        # update the minimap graphics
        self.group.adjust_minimap_view(context)

        # Show node coordinates in the title area
        # find the center of the region in view coords
        region = context.region
        x, y = context.region.view2d.region_to_view( region.width/2 , region.height/2)
        context.area.header_text_set( "Panning to: {:.0f}, {:.0f}".format(x,y) )

        return {'RUNNING_MODAL'}







class NODE_EDITOR_GGT_navigator(GizmoGroup):
    bl_idname = "NODE_EDITOR_GGT_navigator"
    bl_label = "Node Navigation Widget"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'WINDOW'
    bl_options = {'PERSISTENT', "SELECT", "SHOW_MODAL_ALL"}

    @classmethod
    def poll(cls, context):
        node_tree = context.space_data.node_tree
        return node_tree and len(node_tree.nodes)


    def adjust_minimap_map(self, context):
        # minimap is fixed width, but changes height based on canvas size
        self.minimap_width  = 200
        self.minimap_height = 200 / self.full_view_aspect_ratio

        region = context.region

        # position
        self.minimap.matrix_basis[0][3] = region.width  - self.minimap_width /2 - 40
        self.minimap.matrix_basis[1][3] = region.height - self.minimap_height/2 - 40

        # scale
        self.minimap.matrix_basis[0][1] = self.minimap_width  / 2
        self.minimap.matrix_basis[1][0] = self.minimap_height / 2

        # precalculate boundaries for use by minimap_view
        self.minimap_minx = self.minimap.matrix_basis[0][3] - self.minimap_width /2
        self.minimap_miny = self.minimap.matrix_basis[1][3] - self.minimap_height/2
        self.minimap_maxx = self.minimap.matrix_basis[0][3] + self.minimap_width /2
        self.minimap_maxy = self.minimap.matrix_basis[1][3] + self.minimap_height/2


    def convert_view_to_minimap_coords(self, cx, cy, w, h):
        dx = (cx - self.full_view_minx) / self.full_view_width  * self.minimap_width
        dy = (cy - self.full_view_miny) / self.full_view_height * self.minimap_height

        x = self.minimap_minx + dx
        y = self.minimap_miny + dy

        reduction_raito = self.minimap_width / self.full_view_width
        nw = w * reduction_raito
        nh = h * reduction_raito

        return x, y, nw, nh

    def adjust_minimap_view(self,context):
        region = context.region

        # find the center of the region in view coords
        cx, cy = context.region.view2d.region_to_view(region.width/2, region.height/2)

        # find the bottom left of the region in view coords
        ox, oy = context.region.view2d.region_to_view(0, 0)

        # convert to minimap coordinates
        w = (cx-ox)*2
        h = (cy-oy)*2

        # BUG?
        # No idea why this weird scaling is necessary
        cx = cx / 2
        cy = cy / 2

        # weird scaling for width and height for minimap, probably a bug somewhere
        x, y, w, h = self.convert_view_to_minimap_coords(cx, cy, w/2, h/2)

        # clamp size of view
        # w = min(self.minimap_width,  w)
        # h = min(self.minimap_height, h)

        original_w = w
        original_h = h

        #find distance of view from each edge of the minimap
        from_minx = (x-w/2) - self.minimap_minx
        from_miny = (y-h/2) - self.minimap_miny
        from_maxx = self.minimap_maxx - (x+w/2)
        from_maxy = self.minimap_maxy - (y+h/2)

        # clamp the view to stay inside the minimap
        if from_minx < 0:
            w += from_minx
            x += from_minx

        if from_miny < 0:
            h += from_miny
            y += from_miny

        if from_maxx < 0:
            w += from_maxx
            x -= from_maxx

        if from_maxy < 0:
            h += from_maxy
            y -= from_maxy

        w = max(w, 2)
        h = max(h, 2)
        x = max(x, self.minimap_minx + w / 2)
        x = min(x, self.minimap_maxx - w / 2)
        y = max(y, self.minimap_miny + h / 2)
        y = min(y, self.minimap_maxy - h / 2)

        # position
        self.minimap_view.matrix_basis[0][3] = x
        self.minimap_view.matrix_basis[1][3] = y

        # scale
        self.minimap_view.matrix_basis[0][1] = w / 2
        self.minimap_view.matrix_basis[1][0] = h / 2


    def refresh_nodes(self, context):
        for n_gizmo, n_context in zip(self.nodes, context.space_data.node_tree.nodes):
            cx = n_context.location[0]
            cy = n_context.location[1]

            # BUG? Again, no idea why this weird scaling is necessary
            # don't understand why these need to be scaled down twice?
            cw = n_context.dimensions[0] / 2
            ch = n_context.dimensions[1] / 2

            # Convert coordinate systems
            x, y, w, h = self.convert_view_to_minimap_coords(cx, cy, cw, ch)

            # position
            n_gizmo.matrix_basis[0][3] = x + w /2
            n_gizmo.matrix_basis[1][3] = y - h /2

            # scale
            n_gizmo.matrix_basis[0][1] = w / 2
            n_gizmo.matrix_basis[1][0] = h / 2

            # highlight if node is selected
            if n_context.select:
                n_gizmo.color = .8, .8, .8
            else:
                n_gizmo.color = .6, .6, .6


    def scan_nodes(self, context):
        # if a node is added or removed, clear self.gizmos
        # z-index is only determined by order added into gizmos list
        # no way to re-order the list, so just start over
        #
        # This is the only way to ensure that nodes stay on top
        if len(context.space_data.node_tree.nodes) != len(self.nodes):
            self.setup(context)

        # can't show nodes on screen if there are none...
        if not len(context.space_data.node_tree.nodes):
            return

        # search for the furthest nodes in each direction
        minx =  math.inf;
        miny =  math.inf;
        maxx = -math.inf;
        maxy = -math.inf;

        for n in context.space_data.node_tree.nodes:
            w = n.dimensions[0] / 2
            h = n.dimensions[1] / 2

            minx = min( minx, n.location[0] )
            maxx = max( maxx, n.location[0] + w)
            miny = min( miny, n.location[1] - h)
            maxy = max( maxy, n.location[1] )

        self.full_view_minx = minx - 0
        self.full_view_miny = miny - 0
        self.full_view_maxx = maxx + 0
        self.full_view_maxy = maxy + 0
        self.full_view_width = maxx - minx
        self.full_view_height = maxy - miny

        try:
            self.full_view_aspect_ratio = self.full_view_width / self.full_view_height
        except:
            print("Invalid node range coordinates {} {}".format(self.full_view_height, self.full_view_width))
            self.full_view_minx = -1000
            self.full_view_miny = -1000
            self.full_view_maxx = 1000
            self.full_view_maxy = 1000
            self.full_view_width = maxx - minx
            self.full_view_height = maxy - miny
            self.full_view_aspect_ratio = 1
        finally:
            self.adjust_minimap_map(context)



    def setup(self, context):
        # this function also re-initializes to clear out existing gizmos
        self.gizmos.clear()
        self.nodes = []
        for n in context.space_data.node_tree.nodes:
            g = self.gizmos.new( gizmoSimpleBox.bl_idname )
            self.nodes.append( g )

            g.matrix_basis[0][0] = 0
            g.matrix_basis[1][1] = 0
            g.matrix_basis[2][2] = 0
            g.matrix_basis[3][3] = 1

            g.alpha = 0.7
            g.scale_basis = 1

        view = self.gizmos.new( gizmoSimpleBox.bl_idname )
        self.minimap_view = view

        # mpr = self.gizmos.new("GIZMO_GT_cage_2d")
        mmap = self.gizmos.new( gizmoMousePad.bl_idname )
        self.minimap = mmap

        # skew/rotation: 0
        mmap.matrix_basis[0][0] = 0
        mmap.matrix_basis[1][1] = 0
        view.matrix_basis[0][0] = 0
        view.matrix_basis[1][1] = 0

        # set some colors
        # BUG? Some of these parameters, like alpha seem to do nothing
        mmap.color = .3, .3, .3
        mmap.alpha = 0.5

        view.color = .7, .4, .3
        view.alpha = 0.8

        mmap.hide_select = False
        mmap.color_highlight = .4, .4, .4
        mmap.alpha_highlight = 0.5
        mmap.scale_basis = 1

        self.refresh(context)

    def refresh(self, context):
        self.scan_nodes(context)
        self.adjust_minimap_view(context)
        self.refresh_nodes(context)


def register():
    bpy.utils.register_class(gizmoSimpleBox)
    bpy.utils.register_class(gizmoMousePad)
    bpy.utils.register_class(NODE_EDITOR_GGT_navigator)


def unregister():
    bpy.utils.unregister_class(NODE_EDITOR_GGT_navigator)
    bpy.utils.unregister_class(gizmoMousePad)
    bpy.utils.unregister_class(gizmoSimpleBox)


if __name__ == "__main__":

    try:
        unregister()
    except Exception as e:
        print( "Could not unregister" )
        print( e )

    register()

    print("Reregistered gizmo")
