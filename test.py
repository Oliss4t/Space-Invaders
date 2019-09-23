
# https://stackoverflow.com/questions/2914807/plot-ellipse-from-rectangle
##########################################################################

def create_asteroid_ellipse2(size , x0, y0, x1, y1,color,fill = True):
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
            #print(asteroid_pices)
            if (dx != 0 or xb != xc):
                asteroid_pices.append(Asteroid(size,xc+dx,yb-dy,color))
            # print(asteroid_pices)
                #drawPoint(xc+dx, yb-dy)
                if (dy != 0 or yb != yc):
                    asteroid_pices.append(Asteroid(size,xc+dx,yc+dy,color))
            # print(asteroid_pices)
                #drawPoint(xc+dx, yc+dy)
            if (dy != 0 or yb != yc):
                asteroid_pices.append(Asteroid(size,xb-dx,yc+dy,color))
                #print(asteroid_pices)
                #drawPoint(xb-dx, yc+dy)

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
                    #print(asteroid_pices)
                #drawRow(xb-dx, xc+dx, yc+dy)
                if (dy != 0 or yb != yc):
                    for i in range(int(xb-dx),int(xc+dx),size):
                        asteroid_pices.append(Asteroid(size,i,yb-dy,color))
                        #print(asteroid_pices)
                    #drawRow(xb-dx, xc+dx, yb-dy)
            
            qt += 8*qa*qa - 4*qa*qa*qy
            dy -=size
            qy -= size*2
        # Else step (+1, -1)
        else:
            if (fill):
                for i in range(int(xb-dx),int(xc+dx),size):
                    asteroid_pices.append(Asteroid(size,i,yc+dy,color))
                   # print(asteroid_pices)
                #drawRow(xb-dx, xc+dx, yc+dy)
                if (dy != 0 or yb != yc):
                    for i in range(int(xb-dx),int(xc+dx),size):
                        asteroid_pices.append(Asteroid(size,i,yb-dy,color))#
                        #print(asteroid_pices)
                    #drawRow(xb-dx, xc+dx, yb-dy)
            qt += 8*qb*qb + 4*qb*qb*qx + 8*qa*qa - 4*qa*qa*qy
            dx +=size
            qx += size*2
            dy -=size #oder -2
            qy -= size*2
        
       # End of while loop
    #print(asteroid_pices)
    #print(len(asteroid_pices))
    return asteroid_pices

def create_asteroid_ellipse3(size , x0, y0, x1, y1,color,fill = True):
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
    qt = qa*qa + qb*qb -2*qa*qa*qb
    if (qx != 0):
        xc+=1
        qt += 3*qb*qb

    # Start at (dx, dy) = (0, b) and iterate until (a, 0) is reached
    while (qy >= 0 and qx <= qa*size):
        if (not fill):
            asteroid_pices.append(Asteroid(size,xb-dx,yb-dy,color))
        if (dx != 0 or xb != xc):
            asteroid_pices.append(Asteroid(size,xc+dx,yb-dy,color))
            if (dy != 0 or yb != yc):
                asteroid_pices.append(Asteroid(size,xc+dx, yc+dy,color))
        
        if (dy != 0 or yb != yc):
            asteroid_pices.append(Asteroid(size,xb-dx, yc+dy,color))

        
        #// If a (+1, 0) step stays inside the ellipse, do it
        if (qt + 2*qb*qb*qx + 3*qb*qb <= 0 or qt + 2*qa*qa*qy - qa*qa <= 0):
            qt += 8*qb*qb + 4*qb*qb*(qx)
            dx += size
            qx += size*2
        #// If a (0, -1) step stays outside the ellipse, do it
        elif (qt - 2*qa*qa*qy + 3*qa*qa > 0):
            if (fill):
                for i in range(int(xb-dx), int(xc+dx),size):
                    asteroid_pices.append(Asteroid(size,i, yc+dy,( 0, 0, 0)))
                if (dy != 0 or yb != yc):
                    for i in range(int(xb-dx), int(xc+dx),size):
                        asteroid_pices.append(Asteroid(size,i, yb-dy,( 0, 0, 0)))

            qt += 8*qa*qa - 4*qa*qa*(qy)
            dy -= size
            qy -= size*2
        #// Else step (+1, -1)
        else:
            if (fill):
                for i in range(int(xb-dx), int(xc+dx),size):
                    asteroid_pices.append(Asteroid(size,i, yc+dy,( 0, 0, 0)))
                if (dy != 0 or yb != yc):
                    for i in range(int(xb-dx), int(xc+dx),size):
                        asteroid_pices.append(Asteroid(size,i, yb-dy,( 0, 0, 0)))
            qt += 8*qb*qb + 4*qb*qb*(qx) + 8*qa*qa - 4*qa*qa*(qy)
            dx += size
            qx += size*2
            dy -= size
            qy -= size*2
        
       #// End of while loop
    return asteroid_pices

###

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
