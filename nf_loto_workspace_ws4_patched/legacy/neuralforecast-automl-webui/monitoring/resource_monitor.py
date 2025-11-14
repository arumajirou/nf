"""
リソース監視モジュール

CPU、メモリ、GPU、ディスクI/O、ネットワークI/Oをリアルタイムで監視
"""

import os
import time
import psutil
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from threading import Thread, Event
from datetime import datetime

logger = logging.getLogger(__name__)

# GPU監視のオプショナルインポート
try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False
    logger.warning("GPUtil not installed. GPU monitoring disabled.")

try:
    from py3nvml import py3nvml as nvml
    NVML_AVAILABLE = True
except ImportError:
    NVML_AVAILABLE = False
    logger.warning("py3nvml not installed. Advanced GPU monitoring disabled.")


@dataclass
class ResourceSnapshot:
    """リソース使用状況のスナップショット"""
    timestamp: datetime
    
    # CPU
    cpu_percent: float
    cpu_count: int
    
    # Memory
    memory_used_mb: float
    memory_total_mb: float
    memory_percent: float
    memory_available_mb: float
    
    # GPU (optional)
    gpu_utilization: Optional[float] = None
    gpu_count: int = 0
    gpu_index: Optional[int] = None
    
    # VRAM (optional)
    vram_used_mb: Optional[float] = None
    vram_total_mb: Optional[float] = None
    vram_percent: Optional[float] = None
    
    # Disk I/O
    disk_io_read_mb: Optional[float] = None
    disk_io_write_mb: Optional[float] = None
    disk_io_read_speed_mbps: Optional[float] = None
    disk_io_write_speed_mbps: Optional[float] = None
    
    # Network I/O
    network_sent_mb: Optional[float] = None
    network_recv_mb: Optional[float] = None
    network_sent_speed_mbps: Optional[float] = None
    network_recv_speed_mbps: Optional[float] = None
    
    # Process-specific
    process_cpu_percent: Optional[float] = None
    process_memory_mb: Optional[float] = None
    process_threads: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """辞書形式に変換"""
        d = asdict(self)
        d['timestamp'] = self.timestamp.isoformat()
        return d


class ResourceMonitor:
    """リソース監視クラス"""
    
    def __init__(
        self,
        interval: float = 1.0,
        track_gpu: bool = True,
        track_disk: bool = True,
        track_network: bool = True,
        track_process: bool = True,
        process_pid: Optional[int] = None
    ):
        """
        Args:
            interval: 監視間隔（秒）
            track_gpu: GPU監視を有効化
            track_disk: ディスクI/O監視を有効化
            track_network: ネットワークI/O監視を有効化
            track_process: プロセス固有の監視を有効化
            process_pid: 監視するプロセスID（Noneの場合は現在のプロセス）
        """
        self.interval = interval
        self.track_gpu = track_gpu and GPU_AVAILABLE
        self.track_disk = track_disk
        self.track_network = track_network
        self.track_process = track_process
        
        # プロセス情報
        self.process = psutil.Process(process_pid or os.getpid())
        
        # GPU初期化
        if self.track_gpu and NVML_AVAILABLE:
            try:
                nvml.nvmlInit()
                self.gpu_count = nvml.nvmlDeviceGetCount()
                logger.info(f"NVML initialized. {self.gpu_count} GPU(s) detected.")
            except Exception as e:
                logger.warning(f"Failed to initialize NVML: {e}")
                self.track_gpu = False
                self.gpu_count = 0
        elif self.track_gpu:
            self.gpu_count = len(GPUtil.getGPUs())
            logger.info(f"GPUtil initialized. {self.gpu_count} GPU(s) detected.")
        else:
            self.gpu_count = 0
        
        # ディスクI/O初期値
        self._last_disk_io = psutil.disk_io_counters() if self.track_disk else None
        self._last_disk_time = time.time()
        
        # ネットワークI/O初期値
        self._last_net_io = psutil.net_io_counters() if self.track_network else None
        self._last_net_time = time.time()
        
        # 監視ループ制御
        self._stop_event = Event()
        self._monitor_thread: Optional[Thread] = None
        self._snapshots: List[ResourceSnapshot] = []
        self._max_snapshots = 1000  # メモリ管理のため最大数を制限
    
    def get_snapshot(self) -> ResourceSnapshot:
        """現在のリソース使用状況を取得"""
        timestamp = datetime.now()
        
        # CPU
        cpu_percent = psutil.cpu_percent(interval=0.1)
        cpu_count = psutil.cpu_count()
        
        # Memory
        mem = psutil.virtual_memory()
        memory_used_mb = mem.used / (1024 ** 2)
        memory_total_mb = mem.total / (1024 ** 2)
        memory_percent = mem.percent
        memory_available_mb = mem.available / (1024 ** 2)
        
        # GPU (optional)
        gpu_utilization = None
        gpu_index = None
        vram_used_mb = None
        vram_total_mb = None
        vram_percent = None
        
        if self.track_gpu:
            if NVML_AVAILABLE:
                try:
                    # メインGPU（インデックス0）の情報を取得
                    handle = nvml.nvmlDeviceGetHandleByIndex(0)
                    gpu_info = nvml.nvmlDeviceGetUtilizationRates(handle)
                    gpu_utilization = gpu_info.gpu
                    
                    mem_info = nvml.nvmlDeviceGetMemoryInfo(handle)
                    vram_used_mb = mem_info.used / (1024 ** 2)
                    vram_total_mb = mem_info.total / (1024 ** 2)
                    vram_percent = (mem_info.used / mem_info.total) * 100
                    gpu_index = 0
                except Exception as e:
                    logger.debug(f"Failed to get GPU info: {e}")
            else:
                try:
                    gpus = GPUtil.getGPUs()
                    if gpus:
                        gpu = gpus[0]
                        gpu_utilization = gpu.load * 100
                        vram_used_mb = gpu.memoryUsed
                        vram_total_mb = gpu.memoryTotal
                        vram_percent = gpu.memoryUtil * 100
                        gpu_index = gpu.id
                except Exception as e:
                    logger.debug(f"Failed to get GPU info: {e}")
        
        # Disk I/O
        disk_io_read_mb = None
        disk_io_write_mb = None
        disk_io_read_speed_mbps = None
        disk_io_write_speed_mbps = None
        
        if self.track_disk:
            try:
                current_disk_io = psutil.disk_io_counters()
                current_time = time.time()
                
                if self._last_disk_io:
                    time_delta = current_time - self._last_disk_time
                    read_bytes = current_disk_io.read_bytes - self._last_disk_io.read_bytes
                    write_bytes = current_disk_io.write_bytes - self._last_disk_io.write_bytes
                    
                    disk_io_read_mb = read_bytes / (1024 ** 2)
                    disk_io_write_mb = write_bytes / (1024 ** 2)
                    disk_io_read_speed_mbps = (read_bytes / time_delta) / (1024 ** 2)
                    disk_io_write_speed_mbps = (write_bytes / time_delta) / (1024 ** 2)
                
                self._last_disk_io = current_disk_io
                self._last_disk_time = current_time
            except Exception as e:
                logger.debug(f"Failed to get disk I/O info: {e}")
        
        # Network I/O
        network_sent_mb = None
        network_recv_mb = None
        network_sent_speed_mbps = None
        network_recv_speed_mbps = None
        
        if self.track_network:
            try:
                current_net_io = psutil.net_io_counters()
                current_time = time.time()
                
                if self._last_net_io:
                    time_delta = current_time - self._last_net_time
                    sent_bytes = current_net_io.bytes_sent - self._last_net_io.bytes_sent
                    recv_bytes = current_net_io.bytes_recv - self._last_net_io.bytes_recv
                    
                    network_sent_mb = sent_bytes / (1024 ** 2)
                    network_recv_mb = recv_bytes / (1024 ** 2)
                    network_sent_speed_mbps = (sent_bytes / time_delta) / (1024 ** 2)
                    network_recv_speed_mbps = (recv_bytes / time_delta) / (1024 ** 2)
                
                self._last_net_io = current_net_io
                self._last_net_time = current_time
            except Exception as e:
                logger.debug(f"Failed to get network I/O info: {e}")
        
        # Process-specific
        process_cpu_percent = None
        process_memory_mb = None
        process_threads = None
        
        if self.track_process:
            try:
                process_cpu_percent = self.process.cpu_percent(interval=0.1)
                process_memory_mb = self.process.memory_info().rss / (1024 ** 2)
                process_threads = self.process.num_threads()
            except Exception as e:
                logger.debug(f"Failed to get process info: {e}")
        
        return ResourceSnapshot(
            timestamp=timestamp,
            cpu_percent=cpu_percent,
            cpu_count=cpu_count,
            memory_used_mb=memory_used_mb,
            memory_total_mb=memory_total_mb,
            memory_percent=memory_percent,
            memory_available_mb=memory_available_mb,
            gpu_utilization=gpu_utilization,
            gpu_count=self.gpu_count,
            gpu_index=gpu_index,
            vram_used_mb=vram_used_mb,
            vram_total_mb=vram_total_mb,
            vram_percent=vram_percent,
            disk_io_read_mb=disk_io_read_mb,
            disk_io_write_mb=disk_io_write_mb,
            disk_io_read_speed_mbps=disk_io_read_speed_mbps,
            disk_io_write_speed_mbps=disk_io_write_speed_mbps,
            network_sent_mb=network_sent_mb,
            network_recv_mb=network_recv_mb,
            network_sent_speed_mbps=network_sent_speed_mbps,
            network_recv_speed_mbps=network_recv_speed_mbps,
            process_cpu_percent=process_cpu_percent,
            process_memory_mb=process_memory_mb,
            process_threads=process_threads
        )
    
    def start(self):
        """監視を開始"""
        if self._monitor_thread and self._monitor_thread.is_alive():
            logger.warning("Monitor already running")
            return
        
        self._stop_event.clear()
        self._monitor_thread = Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()
        logger.info(f"Resource monitor started (interval={self.interval}s)")
    
    def stop(self):
        """監視を停止"""
        if not self._monitor_thread or not self._monitor_thread.is_alive():
            logger.warning("Monitor not running")
            return
        
        self._stop_event.set()
        self._monitor_thread.join(timeout=5)
        logger.info("Resource monitor stopped")
    
    def _monitor_loop(self):
        """監視ループ"""
        while not self._stop_event.is_set():
            try:
                snapshot = self.get_snapshot()
                self._snapshots.append(snapshot)
                
                # メモリ管理：古いスナップショットを削除
                if len(self._snapshots) > self._max_snapshots:
                    self._snapshots = self._snapshots[-self._max_snapshots:]
                
            except Exception as e:
                logger.error(f"Error in monitor loop: {e}")
            
            time.sleep(self.interval)
    
    def get_snapshots(self, last_n: Optional[int] = None) -> List[ResourceSnapshot]:
        """
        スナップショットを取得
        
        Args:
            last_n: 最新のN件を取得（Noneの場合は全件）
        
        Returns:
            List[ResourceSnapshot]: スナップショットのリスト
        """
        if last_n:
            return self._snapshots[-last_n:]
        return self._snapshots.copy()
    
    def clear_snapshots(self):
        """スナップショットをクリア"""
        self._snapshots.clear()
        logger.info("Snapshots cleared")
    
    def get_summary(self) -> Dict[str, Any]:
        """監視サマリーを取得"""
        if not self._snapshots:
            return {}
        
        cpu_percents = [s.cpu_percent for s in self._snapshots]
        mem_percents = [s.memory_percent for s in self._snapshots]
        
        summary = {
            'total_snapshots': len(self._snapshots),
            'duration_seconds': (self._snapshots[-1].timestamp - self._snapshots[0].timestamp).total_seconds() if len(self._snapshots) > 1 else 0,
            'cpu': {
                'avg': sum(cpu_percents) / len(cpu_percents),
                'max': max(cpu_percents),
                'min': min(cpu_percents),
            },
            'memory': {
                'avg': sum(mem_percents) / len(mem_percents),
                'max': max(mem_percents),
                'min': min(mem_percents),
            }
        }
        
        # GPU情報
        if self.track_gpu:
            gpu_utils = [s.gpu_utilization for s in self._snapshots if s.gpu_utilization is not None]
            if gpu_utils:
                summary['gpu'] = {
                    'avg': sum(gpu_utils) / len(gpu_utils),
                    'max': max(gpu_utils),
                    'min': min(gpu_utils),
                }
            
            vram_percents = [s.vram_percent for s in self._snapshots if s.vram_percent is not None]
            if vram_percents:
                summary['vram'] = {
                    'avg': sum(vram_percents) / len(vram_percents),
                    'max': max(vram_percents),
                    'min': min(vram_percents),
                }
        
        return summary
    
    def __enter__(self):
        """コンテキストマネージャー: with文のサポート"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """コンテキストマネージャー: 終了時に停止"""
        self.stop()
        
        # NVML cleanup
        if self.track_gpu and NVML_AVAILABLE:
            try:
                nvml.nvmlShutdown()
            except:
                pass
    
    def __del__(self):
        """デストラクタ"""
        if self._monitor_thread and self._monitor_thread.is_alive():
            self.stop()


def get_system_info() -> Dict[str, Any]:
    """システム情報を取得"""
    info = {
        'cpu_count': psutil.cpu_count(logical=False),
        'cpu_count_logical': psutil.cpu_count(logical=True),
        'memory_total_gb': psutil.virtual_memory().total / (1024 ** 3),
        'disk_total_gb': psutil.disk_usage('/').total / (1024 ** 3),
    }
    
    # GPU情報
    if GPU_AVAILABLE:
        gpus = GPUtil.getGPUs()
        info['gpu_count'] = len(gpus)
        info['gpus'] = [
            {
                'id': gpu.id,
                'name': gpu.name,
                'memory_total_mb': gpu.memoryTotal
            }
            for gpu in gpus
        ]
    else:
        info['gpu_count'] = 0
        info['gpus'] = []
    
    return info
