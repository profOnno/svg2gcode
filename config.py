"""G-code emitted at the start of processing the SVG file"""
preamble = ";For pen drawing put your machine on the paper @x0y0z0\nG28\nG0 Z5.0"

"""G-code emitted at the end of processing the SVG file"""
postamble = "G0 X0 Y0 Z5\n;done"

"""G-code emitted before processing a SVG shape"""
#shape_preamble = "G4 P200"
shape_preamble = "G0 Z0"

"""G-code emitted after processing a SVG shape"""
#shape_postamble = "G4 P200"
shape_postamble = "G0 Z5"

# draw speed seems to be nice @ 1000
G1_speed = "F1000"

# A4 area:               210mm x 297mm 

"""Print bed width in mm"""
bed_max_x = 200

"""Print bed height in mm"""
bed_max_y = 280

""" 
Used to control the smoothness/sharpness of the curves.
Smaller the value greater the sharpness. Make sure the
value is greater than 0.1
"""
smoothness = 0.2


