class Piece(object):
    rows = 20       # y
    columns = 10    # x
    
    def __init__(self,column,row,shape,shape_colors,shapes):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0    #number from 0 - 3