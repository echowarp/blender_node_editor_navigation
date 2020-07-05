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
        # print("DRAW")
        self.draw_preset_box( self.matrix_basis )

    def draw_select(self, context, select_id):
        print("SELECT")
        self.draw_preset_box( self.matrix_basis)

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

        # print("Test Select")
        return self.test_inside(x,y)

    def invoke(self, context, event):
        # print("INVOKE mouse: {}, {}".format(event.mouse_region_x, event.mouse_y) )
        # print(dir(event))

        # print( bpy.context.area.type )
        # bpy.context.area.type = "NODE_EDITOR"
#        print( bpy.context.area.type )
#        print( bpy.context.area.spaces.active.type)
#        bpy.ops.view2d.scroller_activate()

        x = event.mouse_region_x
        y = event.mouse_region_y

        # print("Event type: {}   Value: {}".format(event.type, event.value) )

        inside = self.test_inside(x, y)

        if inside and event.type == "LEFTMOUSE" and event.value == "PRESS":
            return {'RUNNING_MODAL'}
        else:
            return {'PASS_THROUGH'}

    def setup(self):
        print("gizmo setup")

        self.use_grab_cursor = True
        self.use_event_handle_all = True


    def exit(self, context, cancel):
        context.area.header_text_set(None)
        # if cancel:

    def refresh(self, context):
        pass

    def modal(self, context, event, tweak):
        # Tweak = 'PRECISE' or 'SNAP'

        # print("MODAL")
        # print( dir(event) )
        # print("Type: {} | Value: {}".format( event.type, event.value ) )

        # if event.value == 'PRESS':
            # print("Finished")
            # return {'FINISHED'}


        dx = event.mouse_x - event.mouse_prev_x
        dy = event.mouse_y - event.mouse_prev_y

        bpy.ops.view2d.pan(deltax=dx, deltay=dy)

        self.group.adjust_minimap_view(context)

        # scrolls with mouse
        # bpy.ops.view2d.smoothview(xmin=0, xmax=0, ymin=0, ymax=0, wait_for_input=True)

        region = context.region

        # find the center of the region in view coords
        x, y = context.region.view2d.region_to_view( region.width/2 , region.height/2)

        # x, y = context.region.view2d.region_to_view(event.mouse_region_x, event.mouse_region_y)
        context.area.header_text_set( "Panning to: {:.0f}, {:.0f}".format(x,y) )

        return {'RUNNING_MODAL'}




#class nodeMiniMapRelay():
#    def __init__(self, gizmoGroup, node):
#        self.group = gizmoGroup
#
#        self.group.nodes[ n.name ] = self
#
#        self.gizmo = self.group.gizmos.new( gizmoMousePad.bl_idname )
#
#        self.gizmo.matrix_basis[0][0] = 0
#        self.gizmo.matrix_basis[1][1] = 0
#        self.gizmo.draw_style = 'BOX'
#        self.gizmo.color = .7, .7, .7
#        self.gizmo.alpha = 0.5
#        self.gizmo.color_highlight = 1.0, 0.5, 1.0
#        self.gizmo.alpha_highlight = 0.5
#        self.gizmo.scale_basis = 1
#
#
#        self.refresh(node)
#
#    def refresh(self, node):
#
#        self.group.width
#        self.group.height
#
#        # position
#        self.gizmo.matrix_basis[0][3] = region.width - 100
#        self.gizmo.matrix_basis[1][3] = region.height - 100
#
#        # scale
#        self.gizmo.matrix_basis[0][1] = width / 2
#        self.gizmo.matrix_basis[1][0] = height / 2









class NODE_EDITOR_GGT_navigator(GizmoGroup):
    bl_idname = "NODE_EDITOR_GGT_navigator"
    bl_label = "Node Navigation Widget"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'WINDOW'
    bl_options = {'PERSISTENT', "SELECT", "SHOW_MODAL_ALL"}

    @staticmethod
    def printOb( ob ):

        print("Object:")
        try:
            print(ob.name)
        except:
            print("object does not have a name")

        print( dir ( ob ) )

    @classmethod
    def poll(cls, context):
        #print("Poll")
        #print(context.object)

        # print("poll")

        # ob = context.object
        # return (ob and ob.type == 'LIGHT')

        return len(context.space_data.node_tree.nodes)


    def adjust_minimap_map(self, context):
        self.minimap_width  = 200
        self.minimap_height = 200 / self.full_view_aspect_ratio

        print("Minimap size: {}, {}   Full View Size {}, {}  - {}".format( self.minimap_width, self.minimap_height, self.full_view_width, self.full_view_height, self.full_view_aspect_ratio) )

        region = context.region

        # position
        self.minimap.matrix_basis[0][3] = region.width  - self.minimap_width /2 - 40
        self.minimap.matrix_basis[1][3] = region.height - self.minimap_height/2 - 40

        # scale
        self.minimap.matrix_basis[0][1] = self.minimap_width  / 2
        self.minimap.matrix_basis[1][0] = self.minimap_height / 2

        self.minimap_minx = self.minimap.matrix_basis[0][3] - self.minimap_width /2
        self.minimap_miny = self.minimap.matrix_basis[1][3] - self.minimap_height/2
        self.minimap_maxx = self.minimap.matrix_basis[0][3] + self.minimap_width /2
        self.minimap_maxy = self.minimap.matrix_basis[1][3] + self.minimap_height/2





    def convert_view_to_minimap_coords(self, cx, cy, w, h):
        dx = (cx - self.full_view_minx) / self.full_view_width  * self.minimap_width
        dy = (cy - self.full_view_miny) / self.full_view_height * self.minimap_height

        x = self.minimap_minx + dx
        y = self.minimap_miny + dy

        # print("w {}   fvw   {}    mmw  {}".format(w, self.full_view_width, self.minimap_width))

        reduction_raito = self.minimap_width / self.full_view_width
        nw = w * reduction_raito
        nh = h * reduction_raito  # / self.full_view_height  * self.minimap_height

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

        print("Minimap region position: {}, {}    Size: {}, {}".format(cx,cy,w,h))

        # weird scaling for width and height for minimap, probably a bug somewhere
        x, y, w, h = self.convert_view_to_minimap_coords(cx, cy, w/2, h/2)

        print("Minimap mini position: {}, {}    Size: {}, {}".format(x,y,w,h))


        # clamp size of view
        w = min(self.minimap_width,  w)
        h = min(self.minimap_height, h)

        original_w = w
        original_h = h

        from_minx = (x-w/2) - self.minimap_minx
        from_miny = (y-h/2) - self.minimap_miny
        from_maxx = self.minimap_maxx - (x+w/2)
        from_maxy = self.minimap_maxy - (y+h/2)

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
        self.minimap_view.matrix_basis[0][3] = x # - original_w/2 # weird offset from scaling, probably a bug somewhere
        self.minimap_view.matrix_basis[1][3] = y # - original_h/4

        # scale
        self.minimap_view.matrix_basis[0][1] = w / 2
        self.minimap_view.matrix_basis[1][0] = h / 2


    def refresh_nodes(self, context):
        for n_gizmo, n_context in zip(self.nodes, context.space_data.node_tree.nodes):
            cx = n_context.location[0]
            cy = n_context.location[1]

            # cw = n_context.width
            # ch = n_context.height * 3
            cw = n_context.dimensions[0] / 2 # don't understand why these need to be scaled down twice?
            ch = n_context.dimensions[1] / 2

            # print(dir(n_context))
            # print("Node size: {}, {}".format(cw, ch) )
            x, y, w, h = self.convert_view_to_minimap_coords(cx, cy, cw, ch)

            # position
            n_gizmo.matrix_basis[0][3] = x
            n_gizmo.matrix_basis[1][3] = y

            # scale
            n_gizmo.matrix_basis[0][1] = w / 2
            n_gizmo.matrix_basis[1][0] = h / 2

            if n_context.select:
                n_gizmo.color = .8, .8, .8
            else:
                n_gizmo.color = .6, .6, .6


    def scan_nodes(self, context):

        if len(context.space_data.node_tree.nodes) != len(self.nodes):
            print("Node added or removed, setup again to enforce z-index")
            self.setup(context)

        if not len(context.space_data.node_tree.nodes):
            return

        minx =  math.inf;
        miny =  math.inf;
        maxx = -math.inf;
        maxy = -math.inf;

        for n in context.space_data.node_tree.nodes:
            # print( dir(n) )
            # print( "Node location: {}, {}".format(n.location[0], n.location[1]) )

            #print("Node dimensions: {}, {}".format(n.dimensions[0], n.dimensions[1]) )

            # w = n.width     # weird scaling. node height is in different units than width
            # h = n.height*5  # weird scaling. node height is in different units than width
            w = n.dimensions[0]
            h = n.dimensions[1]

            minx = min( minx, n.location[0] - w )
            maxx = max( maxx, n.location[0] + w )
            miny = min( miny, n.location[1] - h )
            maxy = max( maxy, n.location[1] + h )

        self.full_view_minx = minx
        self.full_view_miny = miny
        self.full_view_maxx = maxx
        self.full_view_maxy = maxy
        self.full_view_width = maxx - minx
        self.full_view_height = maxy - miny


        print("Found bounds: minx: {}  miny: {}  maxx: {}  maxy: {}".format( minx, miny, maxx, maxy ))

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



        print("Setup")
        print("Context")
        print( dir(context) )

        print("Nodes:")
        print( dir(context.selected_nodes) )
        print( dir(context.active_node) )
        nx = context.active_node.location[0]
        ny = context.active_node.location[1]
        print( "Node Pos: {}, {}".format(nx, ny))

        print("Workspace")
        print( dir(context.workspace) )

        window = context.window
        print("Window: X: {}, Y:{} | W: {}, H:{}".format(window.x, window.y, window.width, window.height) )
        print( dir(context.window) )

        area = context.area
        print("Area  X: {}, Y: {} | W: {} H: {}".format(area.x, area.y, area.width, area.height))
        print( dir(context.area) )
        print( dir(context.area.regions) )
        print("Area Spaces")
        print( dir(context.area.spaces) )
        print( dir(context.area.spaces.active) )
        print( dir(context.area.spaces.active.node_tree) )




        print("Screen")
        print( dir( context.screen) )

        print("Space data")
        print( dir( context.space_data) )
        print( dir( context.space_data.show_region_ui) )

        print("\n Node Tree")
        print( dir( context.space_data.node_tree ) )
        print( dir( context.space_data.node_tree.nodes ) )



        print("World")
        print( dir( context.world) )

        region = context.region
        print("Region: X: {}, Y:{} | W: {}, H:{}".format(region.x, region.y, region.width, region.height))
        print( dir( context.region) )
        print( dir( context.region.view2d ) )


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

        self.minimap_view = self.gizmos.new( gizmoSimpleBox.bl_idname )

        # mpr = self.gizmos.new("GIZMO_GT_cage_2d")
        mpr = self.gizmos.new( gizmoMousePad.bl_idname )
        self.minimap = mpr

        self.minimap_view.matrix_basis[2][3] = 1
        self.minimap.matrix_basis[2][3] = 0



        # print("\n MPR")
        # print( dir(mpr) )
        # print( mpr.matrix_basis )

        # skew
        mpr.matrix_basis[0][0] = 0
        mpr.matrix_basis[1][1] = 0
        mpr.matrix_basis[2][2] = 0
        mpr.matrix_basis[2][2] = 1

        self.minimap_view.matrix_basis[0][0] = 0
        self.minimap_view.matrix_basis[1][1] = 0
        self.minimap_view.matrix_basis[2][2] = 0
        self.minimap_view.matrix_basis[3][3] = 1



        # mpr.draw_style = 'BOX'
        mpr.color = .3, .3, .3
        mpr.alpha = 0.5

        self.minimap_view.color = .7, .4, .3
        self.minimap_view.alpha = 0.8

        mpr.hide_select = False
        mpr.color_highlight = .4, .4, .4
        mpr.alpha_highlight = 0.5
        mpr.scale_basis = 1

        self.refresh(context)





    def refresh(self, context):

        # nx = context.active_node.location[0]
        # ny = context.active_node.location[1]
        # print( "Active Node Pos: {}, {}".format(nx, ny))

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
