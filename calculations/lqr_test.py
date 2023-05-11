import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import control as ct

def state_model_forward(state, input, dt):
    
    theta=state[2]
    
    A = np.array([[1,0,0],
                      [0,1,0],
                      [0,0,1]])
    B=np.array([[np.cos(theta)*dt,0,],
                      [np.sin(theta)*dt,0],
                      [0,0]])
    state=np.dot(A, state) + np.dot(B, input)
    return state
def state_model_turninplace(state, input, dt):

    theta=state[2]
    A = np.array([[1,0,0],
                      [0,1,0],
                  [0,0,1]])
    B=np.array([[0,0,],
                      [0,0],
                      [0,dt]]) #2*v*dt/l
    state = np.dot(A, state) + np.dot(B, input)
    return state

def drive_rakt( state, input, dt):
        hej=state
def lqr_position(x, y, theta, x_d, y_d, theta_d, A, B):
        A = A
        
        B= B
        
        Q = np.array([[2, 0, 0],  # Penalize X position error 
                     [0, 2, 0],  # Penalize Y position error 
                    [0, 0, 2]])
        R = np.array([[1,   0],  # Penalty for linear velocity effort
                        [ 0, 0.5]])
        state_a = np.array([x,y,theta])
        state_d = np.array([x_d, y_d, theta_d])
        state_error = state_a - state_d

        #### chatgpt 

        # Compute LQR gain matrix
        #K_lqr, _, _ = ct.lqr(A, B, Q, R)

        #u_lqr = -np.dot(K_lqr, state_error) 
        #print(u_lqr)
 


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
        #v_linj =np.clip(u_lqr[0], -self.max_linj_vel, self.max_linj_vel)    #vi bestammer en hastiget?
        #v_ang =np.clip(u_lqr[1], -self.max_ang_vel, self.max_ang_vel)
        return u_star#v_linj, v_ang  ## bara returna u om lqr fr      
def main():
     
    # Let the time interval be 1.0 seconds
    dt =0.1
    
    d_state_ray = np.array([(100,0,0),(100, 50, np.pi/2), (0, 50, np.pi), (0, 0, np.pi*3/2), (0,0,0)])
    ini_state = np.array([0,0,0])
    a_state=ini_state
    ini_input=np.array([0,0,0])
    x_varden=[]
    y_varden=[]
    for i in range(4):
        d_state=d_state_ray[i]
        for r in range(1000):
            print(f'iteration = {r*dt} seconds')
            print(f'Current State = {a_state}')
            print(f'Desired State = {d_state}')
         
            state_error = a_state - d_state
            state_error_magnitude = np.linalg.norm(state_error)     
            print(f'State Error Magnitude = {state_error_magnitude}')
            theta=a_state[2]
            A = np.array([[1,0,0],
                      [0,1,0],
                      [0,0,1]])
            B= np.array([[np.cos(theta)*dt,0,],
                      [np.sin(theta)*dt,0],
                      [0,0]])
            # LQR returns the optimal control input                 lqr_position(self, x, y, theta, x_d, y_d, theta_d):
            control_input = lqr_position(a_state[0], a_state[1], a_state[2], d_state[0], d_state[1], d_state[2], A, B)
         
            print(f'Control Input = {control_input}')
                                     
         
            # We apply the optimal control to the robot
            # so we can get a new actual (estimated) state.
            a_state = state_model_forward(a_state, control_input, dt)

            x_varden.append(a_state[0])
            y_varden.append(a_state[1])
            # Stop as soon as we reach the goal
            # Feel free to change this threshold value.
            if state_error_magnitude < 0.01:
                print("\nGoal Has Been Reached Successfully!")
                break
             
            print()
        
        j=i+1
        d_n_state=d_state_ray[j]
        d_vinkel=d_n_state[2]
        for i in range(500):
            print(f'iteration = {i*dt} seconds')
            print(f'Current ang = {a_state[2]}')
            print(f'Desired vinkel = {d_vinkel}')
         
            state_error = a_state[2] - d_vinkel
            state_error_magnitude = np.linalg.norm(state_error)     
            print(f'State Error Magnitude = {state_error_magnitude}')
            theta=a_state[2]
            A = np.array([[1,0,0],
                      [0,1,0],
                      [0,0,1]])
            B=np.array([[0,0,],
                      [0,0],
                      [0,dt]])
            # LQR returns the optimal control input                 lqr_position(self, x, y, theta, x_d, y_d, theta_d):
            control_input = lqr_position(a_state[0], a_state[1], a_state[2], d_state[0], d_state[1], d_vinkel, A, B)
         
            print(f'Control Input = {control_input}')
                                     
         
            # We apply the optimal control to the robot
            # so we can get a new actual (estimated) state.
            a_state = state_model_turninplace(a_state, control_input, dt)

            x_varden.append(a_state[0])
            y_varden.append(a_state[1])
            # Stop as soon as we reach the goal
            # Feel free to change this threshold value.
            if state_error_magnitude < 0.001:
                print("\nGoal Has Been Reached Successfully!")
                break
             
            print()
    plt.scatter(x_varden, y_varden)
    plt.show()
# Entry point for the program
main()