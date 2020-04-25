#!/usr/bin/env python

from __future__ import print_function
import sys
import xml.etree.ElementTree as ET
import shapes as shapes_pkg
from shapes import point_generator
from config import *

sys.setrecursionlimit(5500)

def e_print(x):
  print(x, file=sys.stderr)

def generate_gcode():
    svg_shapes = set(['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path'])
    
    tree = ET.parse(sys.stdin)
    root = tree.getroot()
    viewbox = root.get('viewBox')
    if viewbox:
      _, _, width, height = viewbox.split()                

    e_print("width: %0.2f, height %0.2f" % (float(width),float(height)))

    if width == None or height == None:
        print ("Unable to get width and height for the svg")
        sys.exit(1)

    width = float(width)
    height = float(height)

#    scale_x = bed_max_x / max(width, height)
#    scale_y = bed_max_y / max(width, height)
    #scale_x = 1
    #scale_y = 1
    scale_x = bed_max_x / float(width)
    scale_y = bed_max_y / float(height)
    scale = min (scale_x, scale_y)


    print (preamble)
    
    for elem in root.iter():
        
        try:
            _, tag_suffix = elem.tag.split('}')
        except ValueError:
            e_print("value error")
            continue

        if tag_suffix in svg_shapes:
            shape_class = getattr(shapes_pkg, tag_suffix)
            shape_obj = shape_class(elem)
            d = shape_obj.d_path()
            m = shape_obj.transformation_matrix()

            if d:
                #e_print(d)
                p = point_generator(d, m, smoothness)
                # first move to pos
                #print "\n\n$$$$$$$$$$ start d path"
#                (t,x,y) = next(p)
#                print ("G0 X%0.1f Y%0.1f" % (scale_x*x, scale_y*y))
                # then post preamble
#                print (shape_preamble)
                
                needs_preamble=True

                for t,x,y in p:
                    #e_print("%0.2f, %0.2f, %s" % (x,y,t))

                    if t == "p":
                      
                      # TODO clean up.. moving with g1 doesn't need G1_speed

                      #if x > 0 and x < bed_max_x and y > 0 and y < bed_max_y:  
                      if True:
                        if needs_preamble:
                          print ("G0 X%0.1f Y%0.1f" % (scale*x, scale*y)) 
                          print (shape_preamble)
                          needs_preamble=False
                        else:
                          print ("G1 X%0.1f Y%0.1f %s" % (scale*x, scale*y, G1_speed)) 

                    elif t == "m":
                        print (shape_postamble)
                        needs_preamble=True
                print (shape_postamble)

    print (postamble)

if __name__ == "__main__":
    generate_gcode()



