import numpy as np

class four_points_method():

    mat_pix = None
    mat_mm = None
    transform_pix_mm = None

    def __init__(self) -> None:
        p1_pix = np.array( [508, 128, 1] )
        p2_pix = np.array( [321, 316, 1] )
        p3_pix = np.array( [229, 207, 1] )
        p4_pix = np.array( [157, 204, 1] )

        self.mat_pix = np.mat( [ p1_pix, p2_pix, p3_pix, p4_pix ] ).transpose()

        #print(mat_pix)

        p4_mm = np.array( [-484.75, -196.35, 694.72, 1 ] )
        p3_mm = np.array( [-492.72 , -98.03, 692.74, 1 ] )
        p2_mm = np.array( [-478.25, 143.48, 669.28, 1 ] )
        p1_mm = np.array( [-489.26, 288.89, 812.4, 1 ] )

        self.mat_mm = np.mat( [ p1_mm, p2_mm, p3_mm, p4_mm ] ).transpose()

        self.transform_pix_mm = self.mat_mm * np.linalg.pinv(self.mat_pix)

    def print_transform(self):
        print("K-Transform from pix to mm\n",  self.transform_pix_mm )

    def get_transform_from_pix_mm(self):
        return self.transform_pix_mm

#print(mat_mm)

