import numpy as np

class four_points_method():

    mat_pix = None
    mat_mm = None
    transform_pix_mm = None

    def __init__(self) -> None:

        p1_pix = np.array( [74, 268, 1] )
        p2_pix = np.array( [145, 279, 1] )
        p3_pix = np.array( [324, 294, 1] )
        p4_pix = np.array( [447, 192, 1] )

        self.mat_pix = np.mat( [ p1_pix, p2_pix, p3_pix, p4_pix ] ).transpose()

        p1_mm = np.array( [112.06, 663.58, -27.28, 1 ] )       
        p2_mm = np.array( [210.75 , 647.66, -19.77, 1 ] )
        p3_mm = np.array( [456.48, 621.83, -38.8, 1 ] ) 
        p4_mm = np.array( [629.8, 765.42, -46.59, 1 ] )
        

        self.mat_mm = np.mat( [ p1_mm, p2_mm, p3_mm, p4_mm ] ).transpose()

        self.transform_pix_mm = self.mat_mm * np.linalg.pinv(self.mat_pix)

    def print_transform(self):
        print("K-Transform from pix to mm\n",  self.transform_pix_mm )

    def get_transform_from_pix_mm(self):
        return self.transform_pix_mm

#print(mat_mm)

