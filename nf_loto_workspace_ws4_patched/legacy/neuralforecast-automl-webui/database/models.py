"""
SQLAlchemyモデル定義

データベーススキーマに対応するPythonクラスを定義
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import uuid4

from sqlalchemy import Column, String, Integer, Float, Boolean, Text, TIMESTAMP, ForeignKey, BigInteger, JSON, Enum as SQLEnum, CheckConstraint, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from .connection import Base


# ==========================================
# Enum定義
# ==========================================

class ExperimentStatus(str, enum.Enum):
    """実験ステータス"""
    PENDING = 'pending'
    RUNNING = 'running'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'


class RunStatus(str, enum.Enum):
    """実行ステータス"""
    PENDING = 'pending'
    INITIALIZING = 'initializing'
    RUNNING = 'running'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'


class Backend(str, enum.Enum):
    """バックエンド"""
    OPTUNA = 'optuna'
    RAY = 'ray'


class ArtifactType(str, enum.Enum):
    """アーティファクトタイプ"""
    MODEL = 'model'
    CHECKPOINT = 'checkpoint'
    CONFIG = 'config'
    PREDICTIONS = 'predictions'
    PLOTS = 'plots'
    LOGS = 'logs'
    OTHER = 'other'


class TrialState(str, enum.Enum):
    """試行状態"""
    RUNNING = 'running'
    COMPLETE = 'complete'
    PRUNED = 'pruned'
    FAILED = 'failed'


class LogLevel(str, enum.Enum):
    """ログレベル"""
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'


class NotificationType(str, enum.Enum):
    """通知タイプ"""
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    SUCCESS = 'success'


# ==========================================
# モデル定義
# ==========================================

class Experiment(Base):
    """実験"""
    __tablename__ = 'experiments'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    status = Column(SQLEnum(ExperimentStatus), nullable=False, default=ExperimentStatus.PENDING)
    user_id = Column(String(255))
    tags = Column(JSONB, default=[])
    
    # Relationships
    training_runs = relationship("TrainingRun", back_populates="experiment", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Experiment(id={self.id}, name='{self.name}', status={self.status})>"
    
    def to_dict(self) -> Dict[str, Any]:
        """辞書形式に変換"""
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'status': self.status.value if self.status else None,
            'user_id': self.user_id,
            'tags': self.tags
        }


class Dataset(Base):
    """データセット"""
    __tablename__ = 'datasets'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False, unique=True)
    file_path = Column(Text, nullable=False)
    file_size_mb = Column(Float, nullable=False)
    n_series = Column(Integer, nullable=False)
    avg_length = Column(Float, nullable=False)
    has_exogenous = Column(Boolean, default=False)
    has_static = Column(Boolean, default=False)
    uploaded_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    metadata = Column(JSONB, default={})
    
    # Relationships
    training_runs = relationship("TrainingRun", back_populates="dataset")
    
    def __repr__(self):
        return f"<Dataset(id={self.id}, name='{self.name}', n_series={self.n_series})>"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': str(self.id),
            'name': self.name,
            'file_path': self.file_path,
            'file_size_mb': self.file_size_mb,
            'n_series': self.n_series,
            'avg_length': self.avg_length,
            'has_exogenous': self.has_exogenous,
            'has_static': self.has_static,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None,
            'metadata': self.metadata
        }


class TrainingRun(Base):
    """学習実行"""
    __tablename__ = 'training_runs'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    experiment_id = Column(UUID(as_uuid=True), ForeignKey('experiments.id', ondelete='CASCADE'), nullable=False)
    dataset_id = Column(UUID(as_uuid=True), ForeignKey('datasets.id', ondelete='SET NULL'))
    model_name = Column(String(100), nullable=False)
    status = Column(SQLEnum(RunStatus), nullable=False, default=RunStatus.PENDING)
    start_time = Column(TIMESTAMP, nullable=False, server_default=func.now())
    end_time = Column(TIMESTAMP)
    duration_seconds = Column(Float)
    error_message = Column(Text)
    error_traceback = Column(Text)
    backend = Column(SQLEnum(Backend), nullable=False)
    num_samples = Column(Integer)
    num_completed_samples = Column(Integer, default=0)
    best_loss = Column(Float)
    best_trial_id = Column(Integer)
    config = Column(JSONB, nullable=False, default={})
    
    # Relationships
    experiment = relationship("Experiment", back_populates="training_runs")
    dataset = relationship("Dataset", back_populates="training_runs")
    resource_metrics = relationship("ResourceMetrics", back_populates="training_run", cascade="all, delete-orphan")
    parameters = relationship("RunParameter", back_populates="training_run", cascade="all, delete-orphan")
    results = relationship("RunResult", back_populates="training_run", cascade="all, delete-orphan")
    artifacts = relationship("ModelArtifact", back_populates="training_run", cascade="all, delete-orphan")
    predictions = relationship("Prediction", back_populates="training_run", cascade="all, delete-orphan")
    optimization_history = relationship("OptimizationHistory", back_populates="training_run", cascade="all, delete-orphan")
    logs = relationship("Log", back_populates="training_run", cascade="all, delete-orphan")
    
    __table_args__ = (
        CheckConstraint('duration_seconds IS NULL OR duration_seconds >= 0', name='duration_check'),
        Index('idx_training_runs_experiment_id', 'experiment_id'),
        Index('idx_training_runs_status', 'status'),
        Index('idx_training_runs_start_time', 'start_time'),
        Index('idx_training_runs_model_name', 'model_name'),
    )
    
    def __repr__(self):
        return f"<TrainingRun(id={self.id}, model={self.model_name}, status={self.status})>"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': str(self.id),
            'experiment_id': str(self.experiment_id),
            'dataset_id': str(self.dataset_id) if self.dataset_id else None,
            'model_name': self.model_name,
            'status': self.status.value if self.status else None,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration_seconds': self.duration_seconds,
            'error_message': self.error_message,
            'backend': self.backend.value if self.backend else None,
            'num_samples': self.num_samples,
            'num_completed_samples': self.num_completed_samples,
            'best_loss': self.best_loss,
            'best_trial_id': self.best_trial_id,
            'config': self.config
        }


class ResourceMetrics(Base):
    """リソースメトリクス"""
    __tablename__ = 'resource_metrics'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    run_id = Column(UUID(as_uuid=True), ForeignKey('training_runs.id', ondelete='CASCADE'), nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False, server_default=func.now())
    
    # CPU
    cpu_percent = Column(Float)
    cpu_count = Column(Integer)
    
    # Memory
    memory_used_mb = Column(Float)
    memory_total_mb = Column(Float)
    memory_percent = Column(Float)
    memory_available_mb = Column(Float)
    
    # GPU
    gpu_utilization = Column(Float)
    gpu_count = Column(Integer, default=0)
    gpu_index = Column(Integer)
    
    # VRAM
    vram_used_mb = Column(Float)
    vram_total_mb = Column(Float)
    vram_percent = Column(Float)
    
    # Disk I/O
    disk_io_read_mb = Column(Float)
    disk_io_write_mb = Column(Float)
    disk_io_read_speed_mbps = Column(Float)
    disk_io_write_speed_mbps = Column(Float)
    
    # Network I/O
    network_sent_mb = Column(Float)
    network_recv_mb = Column(Float)
    network_sent_speed_mbps = Column(Float)
    network_recv_speed_mbps = Column(Float)
    
    # Process
    process_cpu_percent = Column(Float)
    process_memory_mb = Column(Float)
    process_threads = Column(Integer)
    
    # Relationships
    training_run = relationship("TrainingRun", back_populates="resource_metrics")
    
    __table_args__ = (
        Index('idx_resource_metrics_run_id', 'run_id'),
        Index('idx_resource_metrics_timestamp', 'timestamp'),
        Index('idx_resource_metrics_run_timestamp', 'run_id', 'timestamp'),
    )
    
    def __repr__(self):
        return f"<ResourceMetrics(run_id={self.run_id}, timestamp={self.timestamp})>"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'run_id': str(self.run_id),
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'cpu_percent': self.cpu_percent,
            'cpu_count': self.cpu_count,
            'memory_used_mb': self.memory_used_mb,
            'memory_total_mb': self.memory_total_mb,
            'memory_percent': self.memory_percent,
            'gpu_utilization': self.gpu_utilization,
            'gpu_count': self.gpu_count,
            'vram_used_mb': self.vram_used_mb,
            'vram_total_mb': self.vram_total_mb,
            'vram_percent': self.vram_percent,
            'disk_io_read_mb': self.disk_io_read_mb,
            'disk_io_write_mb': self.disk_io_write_mb,
            'network_sent_mb': self.network_sent_mb,
            'network_recv_mb': self.network_recv_mb,
            'process_cpu_percent': self.process_cpu_percent,
            'process_memory_mb': self.process_memory_mb,
            'process_threads': self.process_threads
        }


class RunParameter(Base):
    """実行パラメータ"""
    __tablename__ = 'run_parameters'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    run_id = Column(UUID(as_uuid=True), ForeignKey('training_runs.id', ondelete='CASCADE'), nullable=False)
    param_name = Column(String(255), nullable=False)
    param_value = Column(Text, nullable=False)
    param_type = Column(String(50), nullable=False)
    is_tunable = Column(Boolean, default=False)
    search_space = Column(JSONB)
    category = Column(String(100))
    
    # Relationships
    training_run = relationship("TrainingRun", back_populates="parameters")
    
    __table_args__ = (
        UniqueConstraint('run_id', 'param_name', name='run_parameters_unique'),
        Index('idx_run_parameters_run_id', 'run_id'),
        Index('idx_run_parameters_param_name', 'param_name'),
    )
    
    def __repr__(self):
        return f"<RunParameter(name={self.param_name}, value={self.param_value})>"


class RunResult(Base):
    """実行結果"""
    __tablename__ = 'run_results'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    run_id = Column(UUID(as_uuid=True), ForeignKey('training_runs.id', ondelete='CASCADE'), nullable=False)
    trial_number = Column(Integer)
    metric_name = Column(String(255), nullable=False)
    metric_value = Column(Float, nullable=False)
    metric_type = Column(String(50))
    is_best = Column(Boolean, default=False)
    step = Column(Integer)
    
    # Relationships
    training_run = relationship("TrainingRun", back_populates="results")
    
    __table_args__ = (
        UniqueConstraint('run_id', 'trial_number', 'metric_name', 'step', name='run_results_unique'),
        Index('idx_run_results_run_id', 'run_id'),
        Index('idx_run_results_metric_name', 'metric_name'),
    )
    
    def __repr__(self):
        return f"<RunResult(metric={self.metric_name}, value={self.metric_value})>"


class ModelArtifact(Base):
    """モデルアーティファクト"""
    __tablename__ = 'model_artifacts'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    run_id = Column(UUID(as_uuid=True), ForeignKey('training_runs.id', ondelete='CASCADE'), nullable=False)
    artifact_type = Column(SQLEnum(ArtifactType), nullable=False)
    file_path = Column(Text, nullable=False)
    file_size_mb = Column(Float)
    description = Column(Text)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    metadata = Column(JSONB, default={})
    
    # Relationships
    training_run = relationship("TrainingRun", back_populates="artifacts")
    
    __table_args__ = (
        Index('idx_model_artifacts_run_id', 'run_id'),
        Index('idx_model_artifacts_artifact_type', 'artifact_type'),
    )
    
    def __repr__(self):
        return f"<ModelArtifact(type={self.artifact_type}, path={self.file_path})>"


class Prediction(Base):
    """予測結果"""
    __tablename__ = 'predictions'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    run_id = Column(UUID(as_uuid=True), ForeignKey('training_runs.id', ondelete='CASCADE'), nullable=False)
    unique_id = Column(String(255), nullable=False)
    ds = Column(TIMESTAMP, nullable=False)
    y_actual = Column(Float)
    y_pred = Column(Float, nullable=False)
    y_lower = Column(Float)
    y_upper = Column(Float)
    residual = Column(Float)
    
    # Relationships
    training_run = relationship("TrainingRun", back_populates="predictions")
    
    __table_args__ = (
        UniqueConstraint('run_id', 'unique_id', 'ds', name='predictions_unique'),
        Index('idx_predictions_run_id', 'run_id'),
        Index('idx_predictions_unique_id', 'unique_id'),
        Index('idx_predictions_ds', 'ds'),
    )
    
    def __repr__(self):
        return f"<Prediction(series={self.unique_id}, date={self.ds}, pred={self.y_pred})>"


class OptimizationHistory(Base):
    """最適化履歴"""
    __tablename__ = 'optimization_history'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    run_id = Column(UUID(as_uuid=True), ForeignKey('training_runs.id', ondelete='CASCADE'), nullable=False)
    trial_number = Column(Integer, nullable=False)
    trial_state = Column(SQLEnum(TrialState), nullable=False)
    value = Column(Float)
    datetime_start = Column(TIMESTAMP, nullable=False)
    datetime_complete = Column(TIMESTAMP)
    duration = Column(Float)
    params = Column(JSONB, nullable=False)
    user_attrs = Column(JSONB, default={})
    system_attrs = Column(JSONB, default={})
    
    # Relationships
    training_run = relationship("TrainingRun", back_populates="optimization_history")
    
    __table_args__ = (
        UniqueConstraint('run_id', 'trial_number', name='optimization_history_unique'),
        Index('idx_optimization_history_run_id', 'run_id'),
        Index('idx_optimization_history_trial_number', 'trial_number'),
    )
    
    def __repr__(self):
        return f"<OptimizationHistory(trial={self.trial_number}, state={self.trial_state})>"


class Log(Base):
    """ログ"""
    __tablename__ = 'logs'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    run_id = Column(UUID(as_uuid=True), ForeignKey('training_runs.id', ondelete='CASCADE'))
    timestamp = Column(TIMESTAMP, nullable=False, server_default=func.now())
    level = Column(SQLEnum(LogLevel), nullable=False)
    logger_name = Column(String(255))
    message = Column(Text, nullable=False)
    module = Column(String(255))
    function_name = Column(String(255))
    line_number = Column(Integer)
    exception = Column(Text)
    extra = Column(JSONB, default={})
    
    # Relationships
    training_run = relationship("TrainingRun", back_populates="logs")
    
    __table_args__ = (
        Index('idx_logs_run_id', 'run_id'),
        Index('idx_logs_timestamp', 'timestamp'),
        Index('idx_logs_level', 'level'),
    )
    
    def __repr__(self):
        return f"<Log(level={self.level}, message={self.message[:50]})>"


class Notification(Base):
    """通知"""
    __tablename__ = 'notifications'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(String(255), nullable=False)
    type = Column(SQLEnum(NotificationType), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    read_at = Column(TIMESTAMP)
    related_run_id = Column(UUID(as_uuid=True), ForeignKey('training_runs.id', ondelete='SET NULL'))
    metadata = Column(JSONB, default={})
    
    __table_args__ = (
        Index('idx_notifications_user_id', 'user_id'),
        Index('idx_notifications_created_at', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Notification(type={self.type}, title={self.title})>"


class SystemConfig(Base):
    """システム設定"""
    __tablename__ = 'system_config'
    
    key = Column(String(255), primary_key=True)
    value = Column(Text, nullable=False)
    value_type = Column(String(50), nullable=False)
    description = Column(Text)
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    updated_by = Column(String(255))
    
    def __repr__(self):
        return f"<SystemConfig(key={self.key}, value={self.value})>"
