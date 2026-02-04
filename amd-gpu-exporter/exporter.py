#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

def read_file(path):
    try:
        with open(path, 'r') as f:
            return f.read().strip()
    except (IOError, OSError):
        return None

class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != '/metrics':
            self.send_response(404)
            self.end_headers()
            return

        metrics = []
        base = '/sys/class/drm/card0/device'

        # GPU Usage
        gpu_busy = read_file(f'{base}/gpu_busy_percent')
        if gpu_busy:
            metrics.append(f'amd_gpu_busy_percent {gpu_busy}')

        # VRAM
        vram_used = read_file(f'{base}/mem_info_vram_used')
        vram_total = read_file(f'{base}/mem_info_vram_total')
        if vram_used:
            metrics.append(f'amd_gpu_vram_used_bytes {vram_used}')
        if vram_total:
            metrics.append(f'amd_gpu_vram_total_bytes {vram_total}')

        # GTT (system memory used by GPU)
        gtt_used = read_file(f'{base}/mem_info_gtt_used')
        gtt_total = read_file(f'{base}/mem_info_gtt_total')
        if gtt_used:
            metrics.append(f'amd_gpu_gtt_used_bytes {gtt_used}')
        if gtt_total:
            metrics.append(f'amd_gpu_gtt_total_bytes {gtt_total}')

        # Temperature (if available)
        temp_path = '/sys/class/drm/card0/device/hwmon'
        if os.path.exists(temp_path):
            for hwmon in os.listdir(temp_path):
                temp_file = f'{temp_path}/{hwmon}/temp1_input'
                temp = read_file(temp_file)
                if temp:
                    # Convert millidegrees to degrees
                    metrics.append(f'amd_gpu_temperature_celsius {int(temp)/1000}')
                    break

        output = '\n'.join(metrics) + '\n'

        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(output.encode())

    def log_message(self, format, *args):
        pass  # Suppress logging

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 9101), MetricsHandler)
    print('AMD GPU Exporter running on port 9101')
    server.serve_forever()
