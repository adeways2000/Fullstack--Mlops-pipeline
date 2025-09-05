"""
Database models for the MLOps model registry.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

Base = declarative_base()

class ModelVersion(Base):
    """Model version registry for tracking ML models."""
    
    __tablename__ = 'model_versions'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    version = Column(String(20), nullable=False)
    algorithm = Column(String(50), nullable=False)
    framework = Column(String(30), nullable=False, default='scikit-learn')
    
    # Model metadata
    description = Column(Text)
    tags = Column(JSON)  # Store tags as JSON array
    
    # Performance metrics
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    auc_score = Column(Float)
    
    # Training information
    training_dataset_size = Column(Integer)
    training_duration = Column(Float)  # in seconds
    hyperparameters = Column(JSON)
    
    # File paths and artifacts
    model_path = Column(String(255))
    artifacts_path = Column(String(255))
    
    # Status and lifecycle
    status = Column(String(20), default='registered')  # registered, validated, deployed, archived
    stage = Column(String(20), default='development')  # development, staging, production
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deployed_at = Column(DateTime)
    
    # Relationships
    experiments = relationship("Experiment", back_populates="model_version")
    deployments = relationship("Deployment", back_populates="model_version")
    
    def __repr__(self):
        return f"<ModelVersion(name='{self.name}', version='{self.version}', status='{self.status}')>"
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'version': self.version,
            'algorithm': self.algorithm,
            'framework': self.framework,
            'description': self.description,
            'tags': self.tags,
            'accuracy': self.accuracy,
            'precision': self.precision,
            'recall': self.recall,
            'f1_score': self.f1_score,
            'auc_score': self.auc_score,
            'training_dataset_size': self.training_dataset_size,
            'training_duration': self.training_duration,
            'hyperparameters': self.hyperparameters,
            'status': self.status,
            'stage': self.stage,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'deployed_at': self.deployed_at.isoformat() if self.deployed_at else None
        }

class Experiment(Base):
    """Experiment tracking for model training runs."""
    
    __tablename__ = 'experiments'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    run_id = Column(String(50), unique=True, nullable=False)
    
    # Experiment metadata
    description = Column(Text)
    tags = Column(JSON)
    
    # Training configuration
    dataset_name = Column(String(100))
    dataset_version = Column(String(20))
    feature_set = Column(JSON)
    
    # Model configuration
    algorithm = Column(String(50), nullable=False)
    hyperparameters = Column(JSON)
    
    # Results
    metrics = Column(JSON)
    artifacts = Column(JSON)
    
    # Status and timing
    status = Column(String(20), default='running')  # running, completed, failed, cancelled
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    duration = Column(Float)  # in seconds
    
    # Resource usage
    cpu_usage = Column(Float)
    memory_usage = Column(Float)
    gpu_usage = Column(Float)
    
    # Relationships
    model_version_id = Column(Integer, ForeignKey('model_versions.id'))
    model_version = relationship("ModelVersion", back_populates="experiments")
    
    def __repr__(self):
        return f"<Experiment(name='{self.name}', run_id='{self.run_id}', status='{self.status}')>"
    
    def to_dict(self):
        """Convert experiment to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'run_id': self.run_id,
            'description': self.description,
            'tags': self.tags,
            'dataset_name': self.dataset_name,
            'dataset_version': self.dataset_version,
            'feature_set': self.feature_set,
            'algorithm': self.algorithm,
            'hyperparameters': self.hyperparameters,
            'metrics': self.metrics,
            'artifacts': self.artifacts,
            'status': self.status,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration': self.duration,
            'cpu_usage': self.cpu_usage,
            'memory_usage': self.memory_usage,
            'gpu_usage': self.gpu_usage,
            'model_version_id': self.model_version_id
        }

class Deployment(Base):
    """Deployment tracking for model deployments."""
    
    __tablename__ = 'deployments'
    
    id = Column(Integer, primary_key=True)
    deployment_id = Column(String(50), unique=True, nullable=False)
    
    # Deployment metadata
    name = Column(String(100), nullable=False)
    description = Column(Text)
    environment = Column(String(20), nullable=False)  # development, staging, production
    
    # Deployment configuration
    deployment_type = Column(String(20), default='blue_green')  # blue_green, canary, rolling
    traffic_percentage = Column(Float, default=100.0)
    
    # Infrastructure
    endpoint_url = Column(String(255))
    instance_type = Column(String(50))
    instance_count = Column(Integer, default=1)
    
    # Status and timing
    status = Column(String(20), default='deploying')  # deploying, active, inactive, failed, rolled_back
    deployed_at = Column(DateTime, default=datetime.utcnow)
    last_health_check = Column(DateTime)
    
    # Performance metrics
    request_count = Column(Integer, default=0)
    error_count = Column(Integer, default=0)
    avg_latency = Column(Float)
    
    # Relationships
    model_version_id = Column(Integer, ForeignKey('model_versions.id'))
    model_version = relationship("ModelVersion", back_populates="deployments")
    
    def __repr__(self):
        return f"<Deployment(name='{self.name}', environment='{self.environment}', status='{self.status}')>"
    
    def to_dict(self):
        """Convert deployment to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'deployment_id': self.deployment_id,
            'name': self.name,
            'description': self.description,
            'environment': self.environment,
            'deployment_type': self.deployment_type,
            'traffic_percentage': self.traffic_percentage,
            'endpoint_url': self.endpoint_url,
            'instance_type': self.instance_type,
            'instance_count': self.instance_count,
            'status': self.status,
            'deployed_at': self.deployed_at.isoformat() if self.deployed_at else None,
            'last_health_check': self.last_health_check.isoformat() if self.last_health_check else None,
            'request_count': self.request_count,
            'error_count': self.error_count,
            'avg_latency': self.avg_latency,
            'model_version_id': self.model_version_id
        }

class DatasetVersion(Base):
    """Dataset version tracking for reproducibility."""
    
    __tablename__ = 'dataset_versions'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    version = Column(String(20), nullable=False)
    
    # Dataset metadata
    description = Column(Text)
    source = Column(String(255))
    format = Column(String(20))  # csv, parquet, json, etc.
    
    # Data statistics
    row_count = Column(Integer)
    column_count = Column(Integer)
    file_size = Column(Integer)  # in bytes
    
    # Data quality metrics
    missing_values = Column(JSON)
    data_types = Column(JSON)
    statistics = Column(JSON)
    
    # File information
    file_path = Column(String(255))
    checksum = Column(String(64))  # SHA-256 hash
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<DatasetVersion(name='{self.name}', version='{self.version}')>"
    
    def to_dict(self):
        """Convert dataset to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'source': self.source,
            'format': self.format,
            'row_count': self.row_count,
            'column_count': self.column_count,
            'file_size': self.file_size,
            'missing_values': self.missing_values,
            'data_types': self.data_types,
            'statistics': self.statistics,
            'file_path': self.file_path,
            'checksum': self.checksum,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

