
# Import Blender's python API.  This only works when the script is being
# run from the context of Blender.  Blender contains it's own version of Python
# with this library pre-installed.
import bpy

# Load a font
def load_font(font_path):
	""" Load a new TTF font into Blender, and return the font object """
	# get the original list of fonts (before we add a new one)
	original_fonts = bpy.data.fonts.keys()
	
	# load new font
	bpy.ops.font.open(filepath=font_path)
	
	# get the new list of fonts (after we added a new one)
	for font_name in bpy.data.fonts.keys():
		if font_name not in original_fonts:
			return bpy.data.fonts[font_name]
		
	# no new font was added
	return None

# Debug Info:
# ./blender -b test.blend -P demo.py
# -b = background mode
# -P = run a Python script within the context of the project file

# Init all of the variables needed by this script.  Because Blender executes
# this script, OpenShot will inject a dictionary of the required parameters
# before this script is executed.
params = {		
			'title' : 'Oh Yeah! OpenShot!',
			'extrude' : 0.1,
			'bevel_depth' : 0.02,
			'spacemode' : 'CENTER',
			'text_size' : 1.5,
			'width' : 1.0,
			'fontname' : 'Bfont',
			
			'color' : [0.8,0.8,0.8],
			'alpha' : 1.0,
			
			'output_path' : '/tmp/',
			'fps' : 24,
			'quality' : 90,
			'file_format' : 'PNG',
			'color_mode' : 'RGBA',
			'horizon_color' : [0.57, 0.57, 0.57],
			'resolution_x' : 1920,
			'resolution_y' : 1080,
			'resolution_percentage' : 100,
			'start_frame' : 20,
			'end_frame' : 25,
			'animation' : True,
		}

#INJECT_PARAMS_HERE

# The remainder of this script will modify the current Blender .blend project
# file, and adjust the settings.  The .blend file is specified in the XML file
# that defines this template in OpenShot.
#----------------------------------------------------------------------------

# Modify Text / Curve settings
#print (bpy.data.curves.keys())
text_object = bpy.data.curves["Text.001"]
text_object.extrude = params["extrude"]
text_object.bevel_depth = params["bevel_depth"]
text_object.body = params["title"]
text_object.align_x = params["spacemode"]
text_object.size = params["text_size"]
text_object.space_character = params["width"]

# Get font object
font = None
if params["fontname"] != "Bfont":
	# Add font so it's available to Blender
	font = load_font(params["fontname"])
else:
	# Get default font
	font = bpy.data.fonts["Bfont"]
	
text_object.font = font

# Change the material settings (color, alpha, etc...)
material_object = bpy.data.materials["Material.001"]
material_object.diffuse_color = params["diffuse_color"]
material_object.specular_color = params["specular_color"]
material_object.specular_intensity = params["specular_intensity"]
material_object.alpha = params["alpha"]

# Set the render options.  It is important that these are set
# to the same values as the current OpenShot project.  These
# params are automatically set by OpenShot
bpy.context.scene.render.filepath = params["output_path"]
bpy.context.scene.render.fps = params["fps"]
#bpy.context.scene.render.quality = params["quality"]
try:
	bpy.context.scene.render.file_format = params["file_format"]
	bpy.context.scene.render.color_mode = params["color_mode"]
except:
	bpy.context.scene.render.image_settings.file_format = params["file_format"]
	bpy.context.scene.render.image_settings.color_mode = params["color_mode"]
bpy.context.scene.render.alpha_mode = params["alpha_mode"]
bpy.data.worlds[0].horizon_color = params["horizon_color"]
bpy.context.scene.render.resolution_x = params["resolution_x"]
bpy.context.scene.render.resolution_y = params["resolution_y"]
bpy.context.scene.render.resolution_percentage = params["resolution_percentage"]
bpy.context.scene.frame_start = params["start_frame"]
bpy.context.scene.frame_end = params["end_frame"]

# Animation Speed (use Blender's time remapping to slow or speed up animation)
animation_speed = int(params["animation_speed"])	# time remapping multiplier
new_length = int(params["end_frame"]) * animation_speed	# new length (in frames)
bpy.context.scene.frame_end = new_length
bpy.context.scene.render.frame_map_old = 1
bpy.context.scene.render.frame_map_new = animation_speed
if params["start_frame"] == params["end_frame"]:
	bpy.context.scene.frame_start = params["end_frame"]
	bpy.context.scene.frame_end = params["end_frame"]

# Render the current animation to the params["output_path"] folder
bpy.ops.render.render(animation=params["animation"])

