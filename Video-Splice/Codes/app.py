'''服务主文件'''
# app.py
from flask import Flask, request
import threading
import subprocess
from stream_utils import get_video_streams, read_frames, postprocess_frame
from test import process_frame_pair
from spatial_network import SpatialNet
from temporal_network import TemporalNet
from smooth_network import SmoothNet
import torch

app = Flask(__name__)

def load_models():
    spatial_net = SpatialNet().cuda().eval()
    temporal_net = TemporalNet().cuda().eval()
    smooth_net = SmoothNet().cuda().eval()
    spatial_net.load_state_dict(torch.load('full_model_ssd/spatial_warp.pth')['model'])
    temporal_net.load_state_dict(torch.load('full_model_ssd/temporal_warp.pth')['model'])
    smooth_net.load_state_dict(torch.load('full_model_ssd/smooth_warp.pth')['model'])
    return spatial_net, temporal_net, smooth_net

@app.route('/stitch', methods=['POST'])
def stitch_stream():
    data = request.json
    url1, url2 = data['url1'], data['url2']
    output_url = data['output_url']

    spatial_net, temporal_net, smooth_net = load_models()
    cap1, cap2 = get_video_streams(url1, url2)
    buffer = {'initialized': False}

    frame1, frame2 = read_frames(cap1, cap2)
    if frame1 is None or frame2 is None:
        return "Failed to read streams", 500

    frame, width, height = process_frame_pair(frame1, frame2, spatial_net, temporal_net, smooth_net, buffer)
    if frame is not None:
        ffmpeg_process = start_ffmpeg_stream(output_url, width, height)

    def stream_thread():
        while True:
            frame1, frame2 = read_frames(cap1, cap2)
            if frame1 is None or frame2 is None:
                break
            frame, _, _ = process_frame_pair(frame1, frame2, spatial_net, temporal_net, smooth_net, buffer)
            if frame is not None:
                frame = postprocess_frame(frame)
                write_frame(ffmpeg_process, frame)

    threading.Thread(target=stream_thread, daemon=True).start()
    return f"Streaming started at {output_url}", 200

def start_ffmpeg_stream(output_url, width, height, fps=30):
    command = [
        'ffmpeg',
        '-y', '-re',
        '-f', 'rawvideo',
        '-vcodec', 'rawvideo',
        '-pix_fmt', 'bgr24',
        '-s', f'{width}x{height}',
        '-r', str(fps),
        '-i', '-',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-f', 'flv' if output_url.endswith('flv') else 'rtsp',
        output_url
    ]
    return subprocess.Popen(command, stdin=subprocess.PIPE)

def write_frame(process, frame):
    process.stdin.write(frame.tobytes())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)