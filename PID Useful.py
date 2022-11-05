import time
Kp=0                                       # Proportional controller Gain (0 to 100)
Ki=0                                       # Integral controller Gain (0 to 100)
Kd=0      
previous_time =0.0
previous_error=0.0
Set_RPM =500                              # SET RPM value
feedback=0.0                              # actual motor rpm
Integral=0.0   
D_cycal=10

def PID_function():
    
    global previous_time
    global previous_error
    global Integral
    global D_cycal
    global Kp
    global Ki
    global Kd
    
    error = int(Set_RPM) -feedback                    # Differnce between expected RPM and run RPM
    
    if (previous_time== 0):
         previous_time =time.time()
         
    current_time = time.time()
    delta_time = current_time - previous_time
    delta_error = error - previous_error
    
    Pout = (Kp/10 * error)              
    
    Integral += (error * delta_time)
    
    
    if Integral>10:      
        Integral=10
        
    if Integral<-10:
        Integral=-10
    
    Iout=((Ki/10) * Integral)
    
    
    Derivative = (delta_error/delta_time)         #de/dt
    previous_time = current_time
    previous_error = error
    
    Dout=((Kd/1000 )* Derivative)
    
    output = Pout + Iout + Dout                  # PID controller output
    
    return ()