from flask import Flask, request, render_template, Response, jsonify
import cv2
import numpy as np
import threading

app = Flask(__name__)


# 视频流字典
video_streams = {
    1: {'camera_open': False, 
        'paused_event': threading.Event(),
        'processor': None,
        'camera': cv2.VideoCapture(0)  # 使用本机摄像头
        },
    2: {'camera_open': False, 
        'paused_event': threading.Event(),
        'processor': None,
        'camera':None #未分配摄像头
        },
    3: {'camera_open': False, 
        'paused_event': threading.Event(),
        'processor': None,
        'camera': None # 未分配摄像头
        },
    4: {'camera_open': False, 
        'paused_event': threading.Event(),
        'processor': None,
         'camera': None # 未分配摄像头
        }
}
# 1. 视频流状态管理
class VideoProcessor:
    def __init__(self):
        self.parameters = {
            'brightness': 1.0,
            'contrast': 1.0,
            'saturation': 1.0,
            'sharpen': 0.0,
            'temperature': 0.0,
            'denoise': 0.0,
            'blur_amount': 0.0,
            'vignette': 0.0,
            'dehaze': 0.5,
            'gamma': 1.0,
            'edge_enhance': 0.0,
            'auto_white_balance': True
        }

    def update_parameters(self, parameters):
        self.parameters.update(parameters)

    def process_frame(self, frame):
        try:
            # 调整亮度和对比度
            beta = (self.parameters.get('brightness', 1.0) - 1.0) * 100
            frame = cv2.convertScaleAbs(frame, alpha=self.parameters.get('contrast', 1.0), beta=beta)
            
            # 调整饱和度
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype('float32')
            hsv[:, :, 1] *= self.parameters.get('saturation', 1.0)
            hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
            frame = cv2.cvtColor(hsv.astype('uint8'), cv2.COLOR_HSV2BGR)
            
            # 调整锐化
            if self.parameters.get('sharpen', 0) > 0:
                kernel = np.array([
                    [-1, -1, -1],
                    [-1, 9 + self.parameters['sharpen'], -1],
                    [-1, -1, -1]
                ])
                frame = cv2.filter2D(frame, -1, kernel)
            
            # 调整色温
            if self.parameters.get('temperature', 0) != 0:
                b, g, r = cv2.split(frame)
                if self.parameters['temperature'] > 0:
                    r = cv2.addWeighted(r, 1 + self.parameters['temperature'], r, 0, 0)
                else:
                    b = cv2.addWeighted(b, 1 - self.parameters['temperature'], b, 0, 0)
                frame = cv2.merge([b, g, r])
            
            # 调整降噪
            if self.parameters.get('denoise', 0) > 0:
                frame = cv2.fastNlMeansDenoisingColored(frame, None, self.parameters['denoise'] * 10, self.parameters['denoise'] * 10)
            
            # 调整模糊
            if self.parameters.get('blur_amount', 0) > 0:
                kernel_size = int(self.parameters['blur_amount'] * 10) * 2 + 1
                frame = cv2.GaussianBlur(frame, (kernel_size, kernel_size), 0)
            
            # 调整晕影
            if self.parameters.get('vignette', 0) > 0:
                rows, cols = frame.shape[:2]
                kernel_x = cv2.getGaussianKernel(cols, cols/2)
                kernel_y = cv2.getGaussianKernel(rows, rows/2)
                kernel = kernel_y * kernel_x.T
                mask = kernel / kernel.max()
                frame = frame * (1 - self.parameters['vignette'] * (1 - mask)[:,:,np.newaxis])
            
            # 调整去雾化
            if self.parameters.get('dehaze', 0.5) != 0.5:
                frame = adjust_contrast(frame, 1.0 + self.parameters['dehaze'])
            
            # 调整伽马校正
            if self.parameters.get('gamma', 1.0) != 1.0:
                inv_gamma = 1.0 / self.parameters['gamma']
                table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
                frame = cv2.LUT(frame, table)
            
            # 调整边缘增强
            if self.parameters.get('edge_enhance', 0) > 0:
                kernel = np.array([
                    [0, -1, 0],
                    [-1, 5 + self.parameters['edge_enhance'], -1],
                    [0, -1, 0]
                ])
                frame = cv2.filter2D(frame, -1, kernel)
            
            # 调整自动白平衡
            if self.parameters.get('auto_white_balance', True):
                result = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
                avg_a = np.average(result[:, :, 1])
                avg_b = np.average(result[:, :, 2])
                result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
                result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
                frame = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
            
            return frame
        except Exception as e:
            print(f"Frame processing error: {e}")
            return frame

def adjust_contrast(image, level=1.0):
    mean = np.mean(image)
    return cv2.convertScaleAbs(image, alpha=level, beta=(1.0 - level) * mean)
#2. 视频帧生成函数
def gen_frames(stream_id):
    stream = video_streams.get(stream_id)
    if not stream:
        return
    if stream['camera_open']:
        if stream_id == 1 and not stream['camera'] :
           stream['camera']= cv2.VideoCapture(0)  # 使用本机摄像头
        while stream['camera_open']:
            if stream['paused_event'].is_set():
                continue
            if  stream_id == 1 and stream['camera']:
                success, frame = stream['camera'].read()
                if not success:
                    break
            else:
            # 未连接视频源，占位
                frame = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(frame, 'Camera not connected', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            frame = stream['processor'].process_frame(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                     b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
 #3. 路由和控制端点          
@app.route('/video_feed/<int:stream_id>')
def video_feed(stream_id):
    if stream_id not in video_streams:
        return "Invalid stream ID", 404
    if not video_streams[stream_id]['processor']:
        video_streams[stream_id]['processor'] = VideoProcessor()
    parameters = {
        'brightness': float(request.args.get('brightness', 1.0)),
        'contrast': float(request.args.get('contrast', 1.0)),
        'saturation': float(request.args.get('saturation', 1.0)),
        'sharpen': float(request.args.get('sharpen', 0)),
        'temperature': float(request.args.get('temperature', 0)),
        'denoise': float(request.args.get('denoise', 0)),
        'blur_amount': float(request.args.get('blur_amount', 0)),
        'vignette': float(request.args.get('vignette', 0)),
        'dehaze': float(request.args.get('dehaze', 0.5)),
        'gamma': float(request.args.get('gamma', 1.0)),
        'edge_enhance': float(request.args.get('edge_enhance', 0.0)),
        'auto_white_balance': request.args.get('auto_white_balance', 'true').lower() == 'true'
    }
    video_streams[stream_id]['processor'].update_parameters(parameters)
    return Response(gen_frames(stream_id), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_video/<int:stream_id>', methods=['POST'])
def start_video(stream_id):
    if stream_id in video_streams:
        video_streams[stream_id]['camera_open'] = True
        video_streams[stream_id]['paused_event'].clear()
        return jsonify({'status': 'started'})
    return "Invalid stream ID", 404

@app.route('/pause_video/<int:stream_id>', methods=['POST'])
def pause_video(stream_id):
    if stream_id in video_streams:
        video_streams[stream_id]['paused_event'].set()
        return jsonify({'status': 'paused'})
    return "Invalid stream ID", 404

@app.route('/resume_video/<int:stream_id>', methods=['POST'])
def resume_video(stream_id):
    if stream_id in video_streams:
        video_streams[stream_id]['paused_event'].clear()
        return jsonify({'status': 'resumed'})
    return "Invalid stream ID", 404

@app.route('/stop_video/<int:stream_id>', methods=['POST'])
def stop_video(stream_id):
    if stream_id in video_streams:
        video_streams[stream_id]['camera_open'] = False
        if video_streams[stream_id]['camera']:
            video_streams[stream_id]['camera'].release()
            video_streams[stream_id]['camera'] = None
        return jsonify({'status': 'stopped'})
    return "Invalid stream ID", 404

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)