import pyrealsense2 as rs
import numpy as np
depth_scale = 0
class DepthCamera:
    def __init__(self):
        global depth_scale
        # Configure depth and color streams & imu data
        self.pipeline = rs.pipeline()
        config = rs.config()
        
        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))
        
        
        config.enable_stream(rs.stream.accel, rs.format.motion_xyz32f, 200)
        # Gyroscope available FPS: {200,400}Hz
        config.enable_stream(rs.stream.gyro, rs.format.motion_xyz32f, 200)
        
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        
        
        #config.enable_stream(rs.stream.accel)
        #config.enable_stream(rs.stream.gyro)
        #config.enable_stream(rs.RS2_STREAM_ACCEL, RS2_FORMAT_MOTION_XYZ32F, 200)
        #config.enable_stream(rs.RS2_STREAM_GYRO, RS2_FORMAT_MOTION_XYZ32F, 200)
    
        # Start streaming
        
        self.pipeline.start(config)
        #depth_sensor = pp.get_device().first_depth_sensor()
        #depth_scale = depth_sensor.get_depth_scale()

    #def get_scale(self):
        #global depth_scale
        #return depth_scale
    def get_frame(self):
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        #accel = frames[0].as_motion_frame().get_motion_data()
        #gyro = frames[1].as_motion_frame().get_motion_data()
        #ts = frames.get_timestamp()
        gyro_frame = frames.first_or_default(rs.stream.gyro)
        gyro = gyro_frame.as_motion_frame().get_motion_data()

        # Get accel data
        accel_frame = frames.first_or_default(rs.stream.accel)
        accel = accel_frame.as_motion_frame().get_motion_data()
        ts = gyro_frame.get_timestamp()
        if not depth_frame or not color_frame :
            return False, None, None, None, None, None
        return True, depth_image, color_image, accel, gyro, ts
    def get_dframe(self):
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        
        depth_image = np.asanyarray(depth_frame.get_data())
        if not depth_frame :
            return False, None
        return True, depth_image
    def get_imu(self):
        frames = self.pipeline.wait_for_frames()
        gyro_frame = frames.first_or_default(rs.stream.gyro)
        gyro = gyro_frame.as_motion_frame().get_motion_data()

        # Get accel data
        accel_frame = frames.first_or_default(rs.stream.accel)
        accel = accel_frame.as_motion_frame().get_motion_data()
        ts = gyro_frame.get_timestamp()
        #motion_frame = frames.get_motion_frame()
        #accel = motion_frame.get_motion_data()
        #gyro = motion_frame.get_motion_data()
        depth_frame = frames.get_depth_frame()
        depth_image = np.asanyarray(depth_frame.get_data())
        if not gyro_frame or not accel_frame :
            return False, None, None, None, None, False
        elif not depth_frame and not (not gyro_frame or not accel_frame) :
            return True, accel, gyro, None, ts, False
        checkdf = True
        return  True, accel, gyro, depth_image, ts, True
    def imu(self):
        frames = self.pipeline.wait_for_frames()
    def release(self):
        self.pipeline.stop()
        
