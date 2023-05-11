import numpy as np
import control as ct
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
#from calc_velocities import CalcVelocities
class LQR:
    def __init__(self, max_linj_vel, max_ang_vel): #initial_state, initial_input, 
        #self.state = initial_state   #state tre v
       # self.input= initial_input  # 
       # self.theta_in = initial_state[2] 
        self.max_linj_vel=max_linj_vel
        self.max_ang_vel=max_ang_vel
        self.dir=1
    def get_B(self, theta, dt):
        B = np.array([[np.cos(theta)*dt, 0],
                      [np.sin(theta)*dt, 0],
                       [0, dt]])
        return B
    def state_model(self, state, input, dt):   # the real statemodel
        A = np.array([[1,0,0],
                      [0,1,0],
                      [0,0,1]])
        self.state=state
        self.input=input
        self.theta_in=state[2]
        B =  np.array([[np.cos(self.theta_in)*dt, 0],
                      [np.sin(self.theta_in)*dt, 0],
                       [0, dt]])
        self.input[0]=np.clip(self.input[0], -self.max_linj_vel, self.max_linj_vel)
        self.input[1]=np.clip(self.input[1], -self.max_ang_vel, self.max_ang_vel)
        self.state = np.dot(A, self.state) + np.dot(B, self.input)
        
        return self.state
    def state_model_forward(self, state, input, dt):   # go foward, same as statemodel
        self.state=state
        theta=self.state[2]
        self.input=input
        A = np.array([[1,0,0],
                      [0,1,0],
                      [0,0,1]])
        B=np.array([[np.cos(theta)*dt,0,],
                      [np.sin(theta)*dt,0],
                      [0,0]])
        self.state=self.state = np.dot(A, self.state) + np.dot(B, self.input)
        return self.state
    def state_model_turninplace(self, state, input, dt):  #turns when standing on same position
        self.state=state
        theta=self.state[2]
        self.input=input
        A = np.array([[1,0,0],
                      [0,1,0],
                      [0,0,1]])
        B=np.array([[0,0,],
                      [0,0],
                      [0,dt]]) #2*v*dt/l
        self.state=self.state = np.dot(A, self.state) + np.dot(B, self.input)
        return self.state
    def drive_rakt(self, state, input, dt):
        hej=state
        
    def linje(x1,y1,x2,y2,points):
    
    # define two points as numpy arrays
        point1 = np.array([x1, y1])
        point2 = np.array([x2, y2])

    # generate 10 points evenly spaced along the line
        num_points = points
        x_values = np.linspace(point1[0], point2[0], num_points)
        y_values = np.linspace(point1[1], point2[1], num_points)
        coordinates = np.stack((x_values, y_values), axis=-1)
        #plt.scatter(x_values, y_values)
        #plt.show()
        return coordinates
    
    def pathfollowing(self, state, input, linje):
        linjen=[]
        linjen = linje
        x_linje=[] #TODO
        y_linje=[] #TODO
        closest=[]
        self.state=self.state_model(state, input)
        a=np.sqrt((self.state[0]-x_linje[0])**2+(self.state[1]-y_linje[0]))
        for i in len(linjen):
            d=np.sqrt((self.state[0]-x_linje[i])**2+(self.state[1]-y_linje[i]))
            if d<a:
                closest.remove()
                closest.append(x_linje[i], y_linje[i]) 
                 #ersätta inte append
                a=d
        self.state=self.state_model(state, input)
        
        r=0.01 # en centimeter ifran
        if d<r:
            None#gor inget?     #TODO
        else:
            None#find projektionpoint + seek   #TODO
    def circle():
        # Set the number of points
        num_points = 100

        # Calculate the angle between points
        angle = 2 * np.pi / num_points

        # Create an array of angles
        angles = np.arange(num_points) * angle

        # Calculate the x and y coordinates of the points
        x = 10 * np.cos(angles)
        y = 10 * np.sin(angles)

        # Stack the x and y arrays horizontally to create a (num_points, 2) array
        points = np.column_stack((x, y))
        return points
    def _goal_angle_circle(self, x_mid, y_mid, x, y):
    # Calculate the vector from the center of the circle to the robot's position
        V_x = x - x_mid
        V_y = y - y_mid
        # Normalize the vector
        V_mag = np.sqrt(V_x**2 + V_y**2)
        V_x_norm = V_x / V_mag
        V_y_norm = V_y / V_mag
        # Calculate the tangent vector
        T_x = -V_y_norm
        T_y = V_x_norm
        return self._normalize_angle(self.dir + np.arctan2(T_y, T_x))
    def _goal_angle_circle2(self, x, y):
    # Calculate the vector from (0, 0) to the robot's position
        V_x = x
        V_y = y
    # Normalize the vector
        V_mag = np.sqrt(V_x**2 + V_y**2)
        V_x_norm = V_x / V_mag
        V_y_norm = V_y / V_mag
    # Calculate the tangent vector
        T_x = -V_y_norm
        T_y = V_x_norm
        return np.arctan2(T_y, T_x)#self._normalize_angle(self.dir + np.arctan2(T_y, T_x))

    def _normalize_angle(self, angle):
        while angle > np.pi:
            angle -= 2 * np.pi
        while angle < -np.pi:
            angle += 2 * np.pi
        return angle

    def state_model_2(self, state, input, dt, A, B):
        self.A=A
        self.B=B
        self.state=state
        self.input=input
        self.theta_in=state[2]
        self.input[0]=np.clip(self.input[0], -self.max_linj_vel, self.max_linj_vel)
        self.input[1]=np.clip(self.input[1], -self.max_ang_vel, self.max_ang_vel)
        self.state = np.dot(A, self.state) + np.dot(B, self.input)
        
        return self.state
    def reglering_circ(self, state, ref_punkt, input, dt): # not done
        self.state=state
        self.ICC_ref=ref_punkt  #x o y position. punketn som ska roteras runt
        self.input=input
        omega=self.input[1]
        X=np.array([self.state[0]-self.ICC_ref[0], self.state[1]-self.ICC_ref[1], self.state[2]])
        B=np.array([self.ICC_ref[0], self.ICC_ref[1], omega*dt])
        A=np.array([np.cos(omega*dt), -np.sin(omega*dt), 0], 
                   [np.sin(omega*dt), np.cos(omega*dt), 0], 
                   [0,0,1])
        R=np.sqrt((self.state[0]-self.ICC_ref[0])**2+(self.state[1]-self.ICC_ref[1]))
        next_state= np.dot(A, X)+ B
    def lqr_position(self, x, y, theta, x_d, y_d, theta_d):
        #A = np.array([[0, 0,np.sin(theta)],
         #            [0, 0, np.cos(theta)],
          #           [0, 0, 1]])   # A for different state model
        dt=0.1
        B =  np.array([[np.cos(theta)*dt, 0],
                      [np.sin(theta)*dt, 0],
                       [0, dt]])
        A=np.array([[1, 0, 0],
                     [0, 1, 0],
                     [0, 0, 1]])
        #B= np.array([[np.sin(theta), 0],
        #              [np.cos(theta), 0],
         #              [0, 1]])        #B for different state model
    # Q matrix
    # The state cost matrix.
    # Experiment with different Q matrices.
    # Q helps us weigh the relative importance of each state in the 
    # state vector (X, Y, YAW ANGLE). 
    # Q is a square matrix that has the same number of rows as 
    # there are states.
    # Q penalizes bad performance.
    # Q has positive values along the diagonal and zeros elsewhere.
    # Q enables us to target states where we want low error by making the 
    # corresponding value of Q large.
        Q = np.array([[1,0,0],        #funkar för punkt 2,2
                    [0,1,0],
                    [0,0,0.8]])  #works for real state model
    # R matrix
    # The control input cost matrix
    # Experiment with different R matrices
    # This matrix penalizes actuator effort (i.e. rotation of the 
    # motors on the wheels that drive the linear velocity and angular velocity).
    # The R matrix has the same number of rows as the number of control
    # inputs and same number of columns as the number of 
    # control inputs.
    # This matrix has positive values along the diagonal and 0s elsewhere.
    # We can target control inputs where we want low actuator effort 
    # by making the corresponding value of R large. 
        R = np.array([[0.4, 0],    #parametr
                     [0, 0.35]])  #works for real statemodel
        #Q = np.array([[2, 0, 0],  # Penalize X position error 
         #            [0, 2.0, 0],  # Penalize Y position error 
         #           [0, 0, 0.1]])  #works for a different statemodel
        #R = np.array([[3,   0],  # Penalty for linear velocity effort
          #              [ 0, 2.4]]) # fworks for different state model
        state_a = np.array([x,y,theta])
        state_d = np.array([x_d, y_d, theta_d])
        state_error = state_a - state_d

        #### chatgpt # does not work

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
     
    
    # Launch the robot, and have it move to the desired goal destination
    lqr_go=LQR(0.3,0.3)#LQR(ini_state, ini_input, 0.1, 0.2 )
    #d_state_ray = lqr_go.circle()

    ####circle###
    # Set the number of points
    num_points = 10

        # Calculate the angle between points
    angle = 2 * np.pi / num_points

        # Create an array of angles
    angles = np.arange(num_points) * angle

        # Calculate the x and y coordinates of the points
    x = 1 * np.cos(angles)
    y = 1 * np.sin(angles)

        # Stack the x and y arrays horizontally to create a (num_points, 2) array
    points = np.column_stack((x, y))
    ####circle done######

    #d_state_ray1 = lqr_go.circle
    #print(d_state_ray1)
    #np.array([(0.3,.75,np.pi*5/16),(.6, 1.5, np.pi*6/16), (0.9, 2.25, np.pi*7/16), (1.2, 3, np.pi*8/16), (1.5, 3.75, np.pi*9/16)])
    

    ini_state1 = points[0]#d_state_ray1[0]
    angle1=lqr_go._goal_angle_circle2(ini_state1[0], ini_state1[1])
    print(angle)
    # delete the first row from the array
    ini_state=np.array([ini_state1[0], ini_state1[1], angle1])
    points = np.delete(points, 0, axis=0) # första elementet från listan ovan#np.array([0,0,np.pi*4/16])
    a_state=ini_state
    ini_input=np.array([0,0,0])
    
    x_varden=[]
    y_varden=[]
    for i in range(5):
        d_state1=points[i]
        angle=lqr_go._goal_angle_circle2(d_state1[0], d_state1[1])
        d_state=np.array([d_state1[0], d_state1[1], angle]) 
        for i in range(600):
            print(f'iteration = {i*dt} seconds')
            print(f'Current State = {a_state}')
            print(f'Desired State = {d_state}')
            print('angle', angle1, angle)
            state_error = a_state - d_state
            state_error_magnitude = np.linalg.norm(state_error)     
            print(f'State Error Magnitude = {state_error_magnitude}')
         
         
            # LQR returns the optimal control input                 lqr_position(self, x, y, theta, x_d, y_d, theta_d):
            control_input = lqr_go.lqr_position(a_state[0], a_state[1], a_state[2], d_state[0], d_state[1], d_state[2])
         
            print(f'Control Input = {control_input}')
                                     
         
            # We apply the optimal control to the robot
            # so we can get a new actual (estimated) state.
            a_state = lqr_go.state_model(a_state, control_input, dt)

            x_varden.append(a_state[0])
            y_varden.append(a_state[1])
            # Stop as soon as we reach the goal
            # Feel free to change this threshold value.
            if state_error_magnitude < 0.01:
                print("\nGoal Has Been Reached Successfully!")
                break
             
            print()
    plt.scatter(x_varden, y_varden, label='LQR')
    x_mid, y_mid, radius = 0,0,1
    circle = Circle((x_mid, y_mid), radius, edgecolor = "red", facecolor = "none")
    plt.gca().add_patch(circle)
    plt.axis("equal")
    plt.show()
# Entry point for the program
main()