import pygame
from asteroid import Asteroid

def create_asteroid_ellipse(size , x0, y0, x1, y1,color,fill = True):
    """
    This function creates the asteroid pice sprites for one asteroid.
    :param size: integer representing the size of an asteroid pice by pixel
    :type size: integer
    :param x0: integer representing the x startpoint for the asteroid rectangle space
    :type x0: integer
    :param y0: integer representing the y startpoint for the asteroid rectangle space
    :type y0: integer
    :param x1: integer representing the x endpoint for the asteroid rectangle space
    :type x1: integer
    :param y1: integer representing the y endpoint for the asteroid rectangle space
    :type y1: integer
    :param color: tupel representing the rgb color value
    :type color: tupel
    :param fill: boolean to fill out the asteroid or only draw the edge
    :type fill: boolean
    :return param: list of asteroidpice strites
    :return type: list
    """
    asteroid_pices =[]
    color = color
        
    # Calculate height
    yb = yc = (y0 + y1) / 2
    if(y0 < y1):
        qb = y1 - y0 
    else:
        qb = y0 - y1
    qy = qb
    dy = qb / 2
    if (qb % 2 != 0):
        # Bounding box has even pixel height
        yc+=1
    # Calculate width
    xb = xc = (x0 + x1) / 2
    if(x0 < x1):
        qa = x1 - x0
    else:
        qa = x0 - x1
    qx = qa % 2 
    dx = 0
    qt = qa*qa + qb*qb -2*qa*qa*qb
    if qx != 0:
        # Bounding box has even pixel width
        xc+=1
        qt += 3*qb*qb
    # Start at (dx, dy) = (0, b) and iterate until (a, 0) is reached
    while qy >= 0 and qx <= qa:
        # Draw the new points
        if not fill:
            asteroid_pices.append(Asteroid(size,xb-dx,yb-dy,color))
            if (dx != 0 or xb != xc):
                asteroid_pices.append(Asteroid(size,xc+dx,yb-dy,color))
            if (dy != 0 or yb != yc):
                asteroid_pices.append(Asteroid(size,xc+dx,yc+dy,color))
            if (dy != 0 or yb != yc):
                asteroid_pices.append(Asteroid(size,xb-dx,yc+dy,color))

        # If a (+1, 0) step stays inside the ellipse, do it
        if (qt + 2*qb*qb*qx + 3*qb*qb <= 0 or qt + 2*qa*qa*qy - qa*qa <= 0):
            qt += 8*qb*qb + 4*qb*qb*qx
            dx+=size
            qx += size*2
        # If a (0, -1) step stays outside the ellipse, do it
        if (qt - 2*qa*qa*qy + 3*qa*qa > 0):
            if (fill):
                for i in range(int(xb-dx),int(xc+dx),size):
                    asteroid_pices.append(Asteroid(size,i,yc+dy,color))
                if (dy != 0 or yb != yc):
                    for i in range(int(xb-dx),int(xc+dx),size):
                        asteroid_pices.append(Asteroid(size,i,yb-dy,color))
            
            qt += 8*qa*qa - 4*qa*qa*qy
            dy -=size
            qy -= size*2
        # Else step (+1, -1)
        else:
            if (fill):
                for i in range(int(xb-dx),int(xc+dx),size):
                    asteroid_pices.append(Asteroid(size,i,yc+dy,color))
                if (dy != 0 or yb != yc):
                    for i in range(int(xb-dx),int(xc+dx),size):
                        asteroid_pices.append(Asteroid(size,i,yb-dy,color))#
            qt += 8*qb*qb + 4*qb*qb*qx + 8*qa*qa - 4*qa*qa*qy
            dx +=size
            qx += size+2
            dy -=size 
            qy -= size*2
        
       # End of while loop
    return asteroid_pices
