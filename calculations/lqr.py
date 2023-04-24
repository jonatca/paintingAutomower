import numpy as np
import control as ct
class LQR:
    def __init__(self, initial_state, initial_input):
        self.state = initial_state   #state tre v
        self.input= initial_input  # 
        self.theta_in = initial_state[2] 

    def get_B(theta, dt):
        B = np.array([[np.cos(theta)*dt, 0],
                      [np.sin(theta)*dt, 0],
                       [0, dt]])
        return B
    def state_model(self, dt):
        A = np.array([[1,0,0],
                      [0,1,0],
                      [0,0,1]])
        B = self.get_B(self.theta_in, dt)

        self.state = np.dot(A, self.state) + np.dot(B, self.input)

    def lqr_position(self, x, y, theta, x_d, y_d, theta_d, dt):
        A = np.array([[1,0,0],
                      [0,1,0],
                      [0,0,1]])
        #B = self.get_B(self.theta, dt)
        B= np.array([[np.cos2(theta), 0],
                      [np.sin2(theta), 0],
                       [0, 1]])
        Q = np.array([[1,0,0],
                      [0,1,0],
                      [0,0,1]])
        R = np.array([[0.1, 0],    #parametr
                      [0, 0.1]])
        state_a = np.array([x,y,theta])
        state_d = np.array([x_d, y_d, theta_d])
        state_error = state_a - state_d

        #### chatgpt 

        # Compute LQR gain matrix
        K_lqr, _, _ = ct.lqr(A, B, Q, R)

        u_lqr = -np.dot(K_lqr, state_error) 

 


        N = 50  # man kan testa olika
        P = [None]*(N+1)
        Qf = Q
        P[N] = Qf

        for i in range(N, 0, -1):
            P[i-1] = Q + np.dot(A.T, np.dot(P[i], A)) - np.dot(np.dot(np.dot(A.T, np.dot(P[i],B)), np.linalg.inv(R+np.dot(B.T, np.dot(P[i], B)))), (np.dot(B.T, np.dot(P[i], A)))) 

        K = [None]* N
        u = [None]* N

        for i in range(N):
            # K[i] = -(R + B^T P[i+1]B)^-1 B^T P[i+1]A
            K[i]= -np.dot(np.linalg.inv(R + np.dot(B.T, np.dot(P[i+1], B))), np.dot(B.T, np.dot(P[i+1], A))) ## Calculate the optimal feedback gain K
            u[i] = np.dot(K[i], state_error)
        u_star=u[N-1]  ## Optimal control input is u_star
        v_linj =u_lqr[0]
        v_ang =u_lqr[1]
        return v_linj, v_ang  ## bara returna u om lqr fr
