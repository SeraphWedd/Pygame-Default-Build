'''
Game Methods
'''
def configuration():
    '''Loads game configurations from a file.'''
    try:
        temp = {}
        file = open('configuration.info', 'r')
        file.seek(0)
        all_lines = file.readlines()
        for line in all_lines:
            if line[0] not in ['#', ' ', '\n', '@']:
                conf, _, val = line.split()
                temp[conf] = int(val)
        file.close()
        return temp
    except FileNotFoundError:
        print('Error! Configuration file not found! Game cannot Run!')
        pg.quit()
        time.sleep(5)
        sys.exit()

def crop_image(image, image_rect, crop_rect):
    '''Receives a surface, it's rect, and the rect of image to be cropped.
Returns a surface.'''
    ix, iy, iw, ih = image_rect
    cx, cy, cw, ch = crop_rect
    #Trim from topleft of image to topleft of crop_rect
    temp = pg.transform.chop(image, (0, 0, cx, cy))
    #Trim from bottomright of crop_rect to bottomright of image (temp)
    return pg.transform.chop(temp, (cw, ch, iw-cx-cw, ih-cy-ch))

def make_text_object(text, font, color):
    '''Creates a surf and rect from a text.'''
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

def int_to_str(n):
    '''Converts long integer into a comma separated string.'''
    neg = (n < 0)
    num = str(abs(n))
    if len(num) < 4:
        return str(n)
    else:
        i = len(num)-3
        while i > 0:
            num = num[:i] + ',' + num[i:]
            i -= 3
        if neg:
            return '-' + num
        else:
            return num

def color_mixer(color1, colors):
    '''Mixes color1 with all color passed by colors.'''
    r1, g1, b1 = color1
    
    for color in colors:
        if hasattr(color, '__getitem__'):
            r2, g2, b2 = color
            r1 += r2
            g1 += g2
            b1 += b2
            r1, g1, b1 = [int(x) for x in [r1/2, g1/2, b1/2]]
        else:
            r2, g2, b2 = colors
            r1 += r2
            g1 += g2
            b1 += b2
            r1, g1, b1 = [int(x) for x in [r1/2, g1/2, b1/2]]
            return (r1, g1, b1)
    return (r1, g1, b1)

def get_angle(p1, p2):
    '''p1 is origin and p2 is the target dest.'''
    x1, y1 = p1
    x2, y2 = p2
    if x2 == x1: #Undefined slope
        if y2 > y1: return -90
        else: return 90
    elif y2 == y1: #0 slope
        if x2 > x1: return 0
        else: return 180
    slope = (y2-y1)/(x2-x1)
    angle = math.atan(slope) * 180/math.pi
    if (y2 - y1) > 0 and (x2 - x1) > 0:
        return angle
    elif (y2 - y1) > 0 and (x2 - x1) < 0:
        return 180 + angle
    elif (y2 - y1) < 0 and (x2 - x1) < 0:
        return angle - 180
    elif (y2 - y1) < 0 and (x2 - x1) > 0:
        return angle
