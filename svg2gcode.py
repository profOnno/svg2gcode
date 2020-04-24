#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET
import shapes as shapes_pkg
from shapes import point_generator
from config import *

def generate_gcode():
    svg_shapes = set(['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path'])
    
    tree = ET.parse(sys.stdin)
    root = tree.getroot()
    viewbox = root.get('viewBox')
    if viewbox:
      _, _, width, height = viewbox.split()                

    if width == None or height == None:
        print "Unable to get width and height for the svg"
        sys.exit(1)

    width = float(width)
    height = float(height)

    scale_x = bed_max_x / max(width, height)
    scale_y = bed_max_y / max(width, height)

    print preamble 
    
    for elem in root.iter():
        
        try:
            _, tag_suffix = elem.tag.split('}')
        except ValueError:
            continue

        if tag_suffix in svg_shapes:
            shape_class = getattr(shapes_pkg, tag_suffix)
            shape_obj = shape_class(elem)
            d = shape_obj.d_path()
            m = shape_obj.transformation_matrix()

            if d:
                p = point_generator(d, m, smoothness)
                # first move to pos
                #print "\n\n$$$$$$$$$$ start d path"
                (t,x,y) = next(p)
                print "G0 X%0.1f Y%0.1f" % (scale_x*x, scale_y*y) 
                # then post preamble
                print shape_preamble 
                
                needs_preamble=False

                sm = "G1"
                fm = "G0"
                mt = sm

                for t,x,y in p:
                    if t == "p":
                      # TODO clean up.. moving with g1 doesn't need G1_speed

                      if needs_preamble:
                        mt = fm
                      else:
                        mt = sm

                      if x > 0 and x < bed_max_x and y > 0 and y < bed_max_y:  
                        print "%s X%0.1f Y%0.1f %s" % (mt, scale_x*x, scale_y*y, G1_speed) 
                      if needs_preamble:
                        print shape_preamble
                        needs_preamble=False

                    elif t == "m":
                        print shape_postamble
                        needs_preamble=True
                #print shape_postamble

    print postamble 

if __name__ == "__main__":
    generate_gcode()



