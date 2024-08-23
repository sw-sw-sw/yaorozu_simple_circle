import time

class Timer:
    def __init__(self, name: str, fps_update_interval = 0.01):
        self.name = name
        self.frame_count = 0
        self.start_time = time.time()
        self.fps_update_interval = fps_update_interval
        self.last_time = time.time()
        self.time_value = 0
        self.b_print = True
    
    def start(self):
        self.start_time = time.time()
    
    # def calculate(self):
        # self.frame_count += 1
        # self.current_time = time.time() 
        # if self.current_time - self.last_time >= self.fps_update_interval: 
            
        #     # calculate fps
        #     fps = self._calculate_fps()
        #     if self.b_print:
        #         print(self.name + f" FPS: {fps:.2f}")
            
        #     #   calculate time value
        #     self.last_time = self.current_time
        #     self.frame_count = 0
        #     self.time_value = time.time() - self.start_time
        #     self._set_time_interval(self.time_value)
            
        #     # TensorFlowの処理時間を記録
        # return self.time_value
        
    def _calculate_fps(self):
        return self.frame_count / (self.current_time - self.last_time) if (self.current_time - self.last_time) > 0 else 0

    def sleep_time(self, other_time_value):
        time_interval = max(other_time_value - self.time_value, 0)
        # print("time interval", time_interval)
        time.sleep(time_interval)
        
    def calculate_time(self):
        self.time_value = time.time() - self.start_time
        return self.time_value
    
    def print_fps(self,interval_time):
        self.frame_count += 1
        self.current_time = time.time() 
        if self.current_time - self.last_time >= interval_time:
            # calculate fps
            fps = self._calculate_fps()
            print(self.name + " FPS:", f"{fps:4.2f}")
            self.last_time = self.current_time
            self.frame_count = 0            
        return