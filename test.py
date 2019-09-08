
def create_asteroid_ellipse3(x0, y0, x1, y1, fill= True):
    asteroid_pices =[]
    color = color
    size = size
    yb = yc = (y0 + y1) / 2
    if y0 < y1:
        qb=y1 - y0
    else:
        qb =y0 - y1
    qy = qb
    dy = qb / 2
    if (qb % 2 != 0):
        yc+=1
    xb = xc = (x0 + x1) / 2
    if x0 < x1:
        qa=x1 - x0
    else:
        qa =x0 - x1
    qx = qa % 2
    dx = 0
    qt = float(qa)*float(qa) + float(qb*qb -2*qa*qa*qb)
    if (qx != 0):
        xc+=1
        qt += 3*qb*qb

    # Start at (dx, dy) = (0, b) and iterate until (a, 0) is reached
    while (qy >= 0 and qx <= qa):
        if (not fill):
            asteroid_pices.append(Asteroid(size,xb-dx,yb-dy,color))
        if (dx != 0 or xb != xc):
            asteroid_pices.append(Asteroid(size,xc+dx,yb-dy,color))
            if (dy != 0 or yb != yc):
                asteroid_pices.append(Asteroid(size,xc+dx, yc+dy,color))
        
        if (dy != 0 or yb != yc):
            asteroid_pices.append(Asteroid(size,xb-dx, yc+dy,color))

        
        #// If a (+1, 0) step stays inside the ellipse, do it
        if (qt + 2*qb*qb*qx + 3*qb*qb <= 0 or qt + 2*qa*qa*qy - float(qa*qa) <= 0):
            qt += 8*qb*qb + 4*qb*qb*qx
            dx+=1
            qx += 2
        #// If a (0, -1) step stays outside the ellipse, do it
        elif (qt - 2L*qa*qa*qy + 3L*qa*qa > 0L):
            if (fill):
                for i in range(xb-dx, xc+dx):
                    asteroid_pices.append(Asteroid(size,i, yc+dy,color))
                if (dy != 0 or yb != yc):
                    for i in range(xb-dx, xc+dx):
                        asteroid_pices.append(Asteroid(size,i, yb-dy,color))

            qt += 8*qa*qa - 4*qa*qa*qy
            dy-=1
            qy -= 2
        #// Else step (+1, -1)
        else:
            if (fill):
                for i in range(xb-dx, xc+dx):
                    asteroid_pices.append(Asteroid(size,i, yc+dy,color))
                if (dy != 0 or yb != yc):
                    for i in range(xb-dx, xc+dx):
                        asteroid_pices.append(Asteroid(size,i, yb-dy,color))
            qt += 8*qb*qb + 4*qb*qb*qx + 8*qa*qa - 4*qa*qa*qy
            dx+=1
            qx += 2
            dy-=1
            qy -= 2
        
       #// End of while loop
    return
