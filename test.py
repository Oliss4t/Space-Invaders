def drawEllipse(self,x0, y0, x1, y1,fill = True):

    self.xb
    self.yb
    self.xc
    self.yc

    # Calculate height
    yb = yc = (y0 + y1) / 2
    qb = lambda qb: y1 - y0 if y0 < y1 else y0 - y1
    qb = y1 - y0
    gy = qb
    dy = qb / 2
    if (qb % 2 != 0):
        # Bounding box has even pixel height
        yc+=1

    # Calculate width
    xb = xc = (x0 + x1) / 2
    qa = lambda qa: x1 - x0 if x0 < x1 else x0 - x1
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
        if  not fill:
        drawPoint(xb-dx, yb-dy)
        if (dx != 0 or xb != xc):
            drawPoint(xc+dx, yb-dy)
            if (dy != 0 or yb != yc)
            drawPoint(xc+dx, yc+dy)
    
        if (dy != 0 or yb != yc):
            drawPoint(xb-dx, yc+dy)


        # If a (+1, 0) step stays inside the ellipse, do it
        if (qt + 2*qb*qb*qx + 3*qb*qb <= 0 or 
            qt + 2*qa*qa*qy - qa*qa <= 0):
            qt += 8*qb*qb + 4*qb*qb*qx
            dx+=1
            qx += 2
        # If a (0, -1) step stays outside the ellipse, do it
        if (qt - 2*qa*qa*qy + 3*qa*qa > 0):
            if (fill):
                drawRow(xb-dx, xc+dx, yc+dy)
                if (dy != 0 or yb != yc):
                    drawRow(xb-dx, xc+dx, yb-dy)
            
            qt += 8*qa*qa - 4*qa*qa*qy
            dy -=1
            qy -= 2
        # Else step (+1, -1)
        else:
            if (fill):
                drawRow(xb-dx, xc+dx, yc+dy)
                if (dy != 0 or yb != yc):
                    drawRow(xb-dx, xc+dx, yb-dy)
            qt += 8*qb*qb + 4*qb*qb*qx + 8*qa*qa - 4*qa*qa*qy
            dx +=1
            qx += 2
            dy -=1 #oder -2
            qy -= 2
        
       # End of while loop
    return