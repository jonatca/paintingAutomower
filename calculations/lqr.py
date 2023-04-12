import numpy as np
import control as ct
class LQR:
    def __init__(self, initial_state, initial_input):
        self.state = initial_state   #state tre värden: x y theta
        self.input= initial_input  # två värden v  omega
        self.theta = initial_state[2] 

    def get_B(theta, dt):
        B = np.array([[np.cos(theta)*dt, 0],
                      [np.sin(theta)*dt, 0
                       [0, dt]]])
        return B
    def state_model(self, dt):
        A = np.array([[1,0,0],
                      [0,1,0],
                      [0,0,1]])
        B = self.get_B(self.theta, dt)

        self.state = np.dot(A, self.state) + np.dot(B, self.input)

    def lqr(self, desired_state, dt):
        A = np.array([[1,0,0],
                      [0,1,0],
                      [0,0,1]])
        B = self.get_B(self.theta, dt)

        Q = np.array([[1,0,0],
                      [0,1,0],
                      [0,0,1]])
        R = np.array([[0.1, 0],    #parametrarna kan ändras, börjar med 0.1 på både v o w
                      [0, 0.1]])
        
        state_error = self.state - desired_state

        #### chatgpt säger detta ####

        # Compute LQR gain matrix
        K, _, _ = ct.lqr(A, B, Q, R)

        u = -np.dot(K, state_error) 

        #### istället för att skriva ut ekvationerna nedan ####   


        N = 50  # man kan testa olika här
        P = [None]*(N+1)
        Qf = Q
        P[N] = Qf

        for i in range(N, 0, -1):
            #P[i-1] = Q + A^T P[i]A – (A^T P[i]B)(R + BTP[i]B)^-1(B^T P[i]A)  
            P[i-1] = Q + np.dot(A.T, np.dot(P[i], A)) - np.dot(np.dot(np.dot(A.T, np.dot(P[i],B)), np.linalg.inv(R+np.dot(B.T, np.dot(P[i], B)))), (np.dot(B.T, np.dot(P[i], A)))) 

        K = [None]* N
        u = [None]* N

        for i in range(N):
            # K[i] = -(R + B^T P[i+1]B)^-1 B^T P[i+1]A
            K[i]= -np.dot(np.linalg.inv(R + np.dot(B.T, np.dot(P[i+1], B))), np.dot(B.T, np.dot(P[i+1], A))) ## Calculate the optimal feedback gain K
            u[i] = np.dot(K[i], state_error)
        u_star=u[N-1]  ## Optimal control input is u_star

        return u_star  ## bara returna u om lqr från gpt funkar    