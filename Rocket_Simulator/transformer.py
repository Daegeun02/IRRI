import numpy as np

from math import cos, sin, sqrt



class Transformer:

    basic_orientation = np.array([[0],
                                  [1],
                                  [0],
                                  [0]])
    
    body_to_ground = np.array([[0,1,0],
                               [0,0,1],
                               [1,0,0]])

    ground_to_body = np.array([[0,0,1],
                               [1,0,0],
                               [0,1,0]])

############################################################
############################################################
############################################################

    @classmethod
    def unpack_attitude(cls, rocket_attitude):

        body_coord = Transformer.ground_to_body.dot(rocket_attitude)

        roll  = body_coord[0]
        pitch = body_coord[1]
        yaw   = body_coord[2]

        cos_roll  = cos(roll/2)
        sin_roll  = sin(roll/2)

        cos_pitch = cos(pitch/2)
        sin_pitch = sin(pitch/2)       

        cos_yaw   = cos(yaw/2)
        sin_yaw   = sin(yaw/2)

        return cos_roll, sin_roll, cos_pitch, sin_pitch, cos_yaw, sin_yaw

############################################################

    @classmethod
    def rotation_matrix(cls, q0, q1, q2, q3):

        R = np.zeros((3,3))
        R[0,0] = q0*q0 + q1*q1 - 0.5
        R[1,1] = q0*q0 + q2*q2 - 0.5
        R[2,2] = q0*q0 + q3*q3 - 0.5

        R[0,1] = q1*q2 - q0*q3
        R[1,0] = q0*q3 + q1*q2

        R[0,2] = q0*q2 + q1*q3
        R[2,0] = q1*q3 - q0*q2

        R[1,2] = q2*q3 - q0*q1
        R[2,1] = q0*q1 + q2*q3

        return R

############################################################

    @staticmethod
    def euler_to_orientation(rocket_attitude):
        cr, sr, cp, sp, cy, sy = Transformer.unpack_attitude(rocket_attitude)

        ## eular to quaternion
        q0 = cy*cp*cr + sy*sp*sr
        q1 = cy*cp*sr - sy*sp*cr
        q2 = cy*sp*cr - sy*cp*sr
        q3 = sy*cp*cr + cy*sp*sr

        ## quaternion to rotation matrix
        R = Transformer.rotation_matrix(q0, q1, q2, q3) * 2

        ## rotation matrix to orientation
        orientation = R.dot(Transformer.basic_orientation[1:])

        ## to ground coordinate
        orientation = Transformer.body_to_ground.dot(orientation)

        return orientation

############################################################
############################################################
############################################################

    @staticmethod
    def euler_to_quaternion(rocket_attitude):
        q0, q1, q2, q3 = Transformer.euler2quaternion(rocket_attitude)
        
        ## quaternion to rotation matrix
        R = Transformer.rotation_matrix(q0, q1, q2, q3) * 2

        ## rotation matrix to orientation
        orientation = R.dot(Transformer.basic_orientation[1:])

        ## to ground coordinate
        orientation = Transformer.body_to_ground.dot(orientation)

        return orientation, q0, q1, q2, q3

############################################################

    @classmethod
    def euler2quaternion(cls, rocket_attitude):

        roll  = rocket_attitude[0]
        pitch = rocket_attitude[1]
        yaw   = rocket_attitude[2]

        R11 = cos(yaw)*cos(pitch)
        R22 = sin(yaw)*sin(pitch)*sin(roll) + cos(yaw)*cos(roll)
        R33 = cos(pitch)*cos(roll)

        TraceR = R11 + R22 + R33

        q0 = sqrt((TraceR+1)/4)
        q1 = sqrt(R11/2 + (1-TraceR)/4)
        q2 = sqrt(R22/2 + (1-TraceR)/4)
        q3 = sqrt(R33/2 + (1-TraceR)/4)

        return q0, q1, q2, q3

############################################################
############################################################
############################################################

    @staticmethod
    def spherical_coordiante(rocket_attitude):
        
        body_coord = Transformer.ground_to_body.dot(rocket_attitude)

        pitch = body_coord[1]
        yaw   = body_coord[2]

        orientation = np.zeros((3,1))

        orientation[0] = sin(yaw)*cos(pitch)
        orientation[1] = sin(yaw)*sin(pitch)
        orientation[2] = cos(yaw)

        return orientation

############################################################
############################################################
############################################################

    @staticmethod
    def euler_rotation(rocket_attitude):

        roll  = rocket_attitude[0]
        pitch = rocket_attitude[1]
        yaw   = rocket_attitude[2]

        R = np.zeros((3,3))

        R_roll = np.array([[1,         0,          0],
                           [0, cos(roll), -sin(roll)],
                           [0, sin(roll),  cos(roll)]])

        R_pitch = np.array([[ cos(pitch), 0, sin(pitch)],
                            [          0, 1,          0],
                            [-sin(pitch), 0, cos(pitch)]])

        R_yaw = np.array([[cos(yaw), -sin(yaw), 0],
                          [sin(yaw),  cos(yaw), 0],
                          [       0,         0, 1]])

        R = R_yaw @ R_pitch @ R_roll

        orientation = R.dot(Transformer.basic_orientation[1:])

        return orientation