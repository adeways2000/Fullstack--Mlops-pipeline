"""
Database models for MLOps monitoring and alerting.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean, JSON
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from src.models.model_registry import Base

class ModelMetrics(Base):
    """Real-time model performance metrics."""
    
    __tablename__ = 'model_metrics'
    
    id = Column(Integer, primary_key=True)
    model_version_id = Column(Integer, ForeignKey('model_versions.id'))
    deployment_id = Column(Integer, ForeignKey('deployments.id'))
    
    # Timestamp
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Performance metrics
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    auc_score = Column(Float)
    
    # Operational metrics
    prediction_count = Column(Integer, default=0)
    error_count = Column(Integer, default=0)
    avg_latency = Column(Float)  # in milliseconds
    p95_latency = Column(Float)
    p99_latency = Column(Float)
    
    # Resource metrics
    cpu_usage = Column(Float)
    memory_usage = Column(Float)
    gpu_usage = Column(Float)
    
    # Custom metrics
    custom_metrics = Column(JSON)
    
    def __repr__(self):
        return f"<ModelMetrics(model_version_id={self.model_version_id}, timestamp='{self.timestamp}')>"
    
    def to_dict(self):
        """Convert metrics to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'model_version_id': self.model_version_id,
            'deployment_id': self.deployment_id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'accuracy': self.accuracy,
            'precision': self.precision,
            'recall': self.recall,
            'f1_score': self.f1_score,
            'auc_score': self.auc_score,
            'prediction_count': self.prediction_count,
            'error_count': self.error_count,
            'avg_latency': self.avg_latency,
            'p95_latency': self.p95_latency,
            'p99_latency': self.p99_latency,
            'cpu_usage': self.cpu_usage,
            'memory_usage': self.memory_usage,
            'gpu_usage': self.gpu_usage,
            'custom_metrics': self.custom_metrics
        }

class DriftDetection(Base):
    """Data and concept drift detection results."""
    
    __tablename__ = 'drift_detection'
    
    id = Column(Integer, primary_key=True)
    model_version_id = Column(Integer, ForeignKey('model_versions.id'))
    
    # Timestamp
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Drift type
    drift_type = Column(String(20), nullable=False)  # data_drift, concept_drift, prediction_drift
    
    # Drift detection results
    drift_detected = Column(Boolean, default=False)
    drift_score = Column(Float)
    threshold = Column(Float)
    
    # Feature-level drift (for data drift)
    feature_drifts = Column(JSON)  # {feature_name: drift_score}
    
    # Statistical test results
    test_statistic = Column(Float)
    p_value = Column(Float)
    test_method = Column(String(50))  # ks_test, chi2_test, psi, etc.
    
    # Data window information
    reference_window_start = Column(DateTime)
    reference_window_end = Column(DateTime)
    current_window_start = Column(DateTime)
    current_window_end = Column(DateTime)
    
    # Sample sizes
    reference_sample_size = Column(Integer)
    current_sample_size = Column(Integer)
    
    # Additional metadata
    extra_metadata = Column(JSON)
    
    def __repr__(self):
        return f"<DriftDetection(drift_type='{self.drift_type}', drift_detected={self.drift_detected})>"
    
    def to_dict(self):
        """Convert drift detection to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'model_version_id': self.model_version_id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'drift_type': self.drift_type,
            'drift_detected': self.drift_detected,
            'drift_score': self.drift_score,
            'threshold': self.threshold,
            'feature_drifts': self.feature_drifts,
            'test_statistic': self.test_statistic,
            'p_value': self.p_value,
            'test_method': self.test_method,
            'reference_window_start': self.reference_window_start.isoformat() if self.reference_window_start else None,
            'reference_window_end': self.reference_window_end.isoformat() if self.reference_window_end else None,
            'current_window_start': self.current_window_start.isoformat() if self.current_window_start else None,
            'current_window_end': self.current_window_end.isoformat() if self.current_window_end else None,
            'reference_sample_size': self.reference_sample_size,
            'current_sample_size': self.current_sample_size,
            'metadata': self.extra_metadata
        }

class Alert(Base):
    """Alert management for monitoring system."""
    
    __tablename__ = 'alerts'
    
    id = Column(Integer, primary_key=True)
    
    # Alert identification
    alert_id = Column(String(50), unique=True, nullable=False)
    alert_type = Column(String(30), nullable=False)  # performance, drift, error, resource
    severity = Column(String(20), default='medium')  # low, medium, high, critical
    
    # Alert content
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    
    # Source information
    model_version_id = Column(Integer, ForeignKey('model_versions.id'))
    deployment_id = Column(Integer, ForeignKey('deployments.id'))
    source_component = Column(String(50))  # training, deployment, monitoring, etc.
    
    # Alert status
    status = Column(String(20), default='active')  # active, acknowledged, resolved, suppressed
    
    # Timing
    triggered_at = Column(DateTime, default=datetime.utcnow)
    acknowledged_at = Column(DateTime)
    resolved_at = Column(DateTime)
    
    # Notification
    notification_sent = Column(Boolean, default=False)
    notification_channels = Column(JSON)  # email, slack, webhook, etc.
    
    # Metadata
    alert_metadata = Column(JSON)
    tags = Column(JSON)
    
    def __repr__(self):
        return f"<Alert(alert_type='{self.alert_type}', severity='{self.severity}', status='{self.status}')>"
    
    def to_dict(self):
        """Convert alert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'alert_id': self.alert_id,
            'alert_type': self.alert_type,
            'severity': self.severity,
            'title': self.title,
            'message': self.message,
            'model_version_id': self.model_version_id,
            'deployment_id': self.deployment_id,
            'source_component': self.source_component,
            'status': self.status,
            'triggered_at': self.triggered_at.isoformat() if self.triggered_at else None,
            'acknowledged_at': self.acknowledged_at.isoformat() if self.acknowledged_at else None,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'notification_sent': self.notification_sent,
            'notification_channels': self.notification_channels,
            'metadata': self.alert_metadata,
            'tags': self.tags
        }

class PredictionLog(Base):
    """Log of model predictions for monitoring and feedback."""
    
    __tablename__ = 'prediction_logs'
    
    id = Column(Integer, primary_key=True)
    model_version_id = Column(Integer, ForeignKey('model_versions.id'))
    deployment_id = Column(Integer, ForeignKey('deployments.id'))
    
    # Request information
    request_id = Column(String(50), unique=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Input data (hashed or anonymized for privacy)
    input_hash = Column(String(64))  # SHA-256 hash of input
    input_features = Column(JSON)  # Feature names and types (not values)
    
    # Prediction results
    prediction = Column(JSON)
    prediction_probability = Column(JSON)
    confidence_score = Column(Float)
    
    # Performance metrics
    latency = Column(Float)  # in milliseconds
    
    # Feedback (if available)
    actual_outcome = Column(JSON)
    feedback_timestamp = Column(DateTime)
    feedback_source = Column(String(50))  # user, system, batch_update
    
    # Metadata
    user_id = Column(String(50))
    session_id = Column(String(50))
    client_info = Column(JSON)
    
    def __repr__(self):
        return f"<PredictionLog(request_id='{self.request_id}', timestamp='{self.timestamp}')>"
    
    def to_dict(self):
        """Convert prediction log to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'model_version_id': self.model_version_id,
            'deployment_id': self.deployment_id,
            'request_id': self.request_id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'input_hash': self.input_hash,
            'input_features': self.input_features,
            'prediction': self.prediction,
            'prediction_probability': self.prediction_probability,
            'confidence_score': self.confidence_score,
            'latency': self.latency,
            'actual_outcome': self.actual_outcome,
            'feedback_timestamp': self.feedback_timestamp.isoformat() if self.feedback_timestamp else None,
            'feedback_source': self.feedback_source,
            'user_id': self.user_id,
            'session_id': self.session_id,
            'client_info': self.client_info
        }

class ModelHealth(Base):
    """Model health status tracking."""
    
    __tablename__ = 'model_health'
    
    id = Column(Integer, primary_key=True)
    model_version_id = Column(Integer, ForeignKey('model_versions.id'))
    deployment_id = Column(Integer, ForeignKey('deployments.id'))
    
    # Timestamp
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Health status
    overall_health = Column(String(20), default='healthy')  # healthy, degraded, unhealthy
    health_score = Column(Float)  # 0-100 score
    
    # Component health
    prediction_health = Column(String(20), default='healthy')
    performance_health = Column(String(20), default='healthy')
    resource_health = Column(String(20), default='healthy')
    data_health = Column(String(20), default='healthy')
    
    # Health checks
    last_prediction_time = Column(DateTime)
    error_rate = Column(Float)
    avg_response_time = Column(Float)
    
    # Resource utilization
    cpu_utilization = Column(Float)
    memory_utilization = Column(Float)
    disk_utilization = Column(Float)
    
    # Data quality indicators
    data_quality_score = Column(Float)
    missing_data_rate = Column(Float)
    
    # Additional health indicators
    health_indicators = Column(JSON)
    
    def __repr__(self):
        return f"<ModelHealth(overall_health='{self.overall_health}', health_score={self.health_score})>"
    
    def to_dict(self):
        """Convert model health to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'model_version_id': self.model_version_id,
            'deployment_id': self.deployment_id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'overall_health': self.overall_health,
            'health_score': self.health_score,
            'prediction_health': self.prediction_health,
            'performance_health': self.performance_health,
            'resource_health': self.resource_health,
            'data_health': self.data_health,
            'last_prediction_time': self.last_prediction_time.isoformat() if self.last_prediction_time else None,
            'error_rate': self.error_rate,
            'avg_response_time': self.avg_response_time,
            'cpu_utilization': self.cpu_utilization,
            'memory_utilization': self.memory_utilization,
            'disk_utilization': self.disk_utilization,
            'data_quality_score': self.data_quality_score,
            'missing_data_rate': self.missing_data_rate,
            'health_indicators': self.health_indicators
        }

