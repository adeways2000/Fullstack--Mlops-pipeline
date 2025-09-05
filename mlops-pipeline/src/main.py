import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uuid
import json

# Import models
from src.models.model_registry import Base, ModelVersion, Experiment, Deployment, DatasetVersion
from src.models.monitoring import ModelMetrics, DriftDetection, Alert, PredictionLog, ModelHealth

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'mlops-pipeline-secret-key-2024'

# Enable CORS for all routes
CORS(app)

# Database configuration
database_path = os.path.join(os.path.dirname(__file__), 'database', 'mlops.db')
os.makedirs(os.path.dirname(database_path), exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{database_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create database engine and session
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables
Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        return db
    finally:
        pass

# API Routes

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'MLOps Pipeline',
        'version': '1.0.0',
        'timestamp': datetime.utcnow().isoformat()
    })

# Model Registry API
@app.route('/api/models', methods=['GET'])
def list_models():
    """List all model versions."""
    db = get_db()
    try:
        models = db.query(ModelVersion).all()
        return jsonify([model.to_dict() for model in models])
    finally:
        db.close()

@app.route('/api/models', methods=['POST'])
def register_model():
    """Register a new model version."""
    data = request.get_json()
    db = get_db()
    try:
        model = ModelVersion(
            name=data.get('name'),
            version=data.get('version'),
            algorithm=data.get('algorithm'),
            framework=data.get('framework', 'scikit-learn'),
            description=data.get('description'),
            tags=data.get('tags', []),
            accuracy=data.get('accuracy'),
            precision=data.get('precision'),
            recall=data.get('recall'),
            f1_score=data.get('f1_score'),
            auc_score=data.get('auc_score'),
            training_dataset_size=data.get('training_dataset_size'),
            training_duration=data.get('training_duration'),
            hyperparameters=data.get('hyperparameters', {}),
            model_path=data.get('model_path'),
            artifacts_path=data.get('artifacts_path')
        )
        db.add(model)
        db.commit()
        db.refresh(model)
        return jsonify(model.to_dict()), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/models/<int:model_id>', methods=['GET'])
def get_model(model_id):
    """Get model details."""
    db = get_db()
    try:
        model = db.query(ModelVersion).filter(ModelVersion.id == model_id).first()
        if not model:
            return jsonify({'error': 'Model not found'}), 404
        return jsonify(model.to_dict())
    finally:
        db.close()

@app.route('/api/models/<int:model_id>/promote', methods=['PUT'])
def promote_model(model_id):
    """Promote model to production."""
    data = request.get_json()
    db = get_db()
    try:
        model = db.query(ModelVersion).filter(ModelVersion.id == model_id).first()
        if not model:
            return jsonify({'error': 'Model not found'}), 404
        
        model.stage = data.get('stage', 'production')
        model.status = 'deployed'
        model.deployed_at = datetime.utcnow()
        db.commit()
        
        return jsonify(model.to_dict())
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

# Experiment Tracking API
@app.route('/api/experiments', methods=['GET'])
def list_experiments():
    """List all experiments."""
    db = get_db()
    try:
        experiments = db.query(Experiment).all()
        return jsonify([exp.to_dict() for exp in experiments])
    finally:
        db.close()

@app.route('/api/experiments', methods=['POST'])
def create_experiment():
    """Create a new experiment."""
    data = request.get_json()
    db = get_db()
    try:
        experiment = Experiment(
            name=data.get('name'),
            run_id=data.get('run_id', str(uuid.uuid4())),
            description=data.get('description'),
            tags=data.get('tags', []),
            dataset_name=data.get('dataset_name'),
            dataset_version=data.get('dataset_version'),
            feature_set=data.get('feature_set', []),
            algorithm=data.get('algorithm'),
            hyperparameters=data.get('hyperparameters', {}),
            status='running'
        )
        db.add(experiment)
        db.commit()
        db.refresh(experiment)
        return jsonify(experiment.to_dict()), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

# Deployment API
@app.route('/api/deployments', methods=['GET'])
def list_deployments():
    """List all deployments."""
    db = get_db()
    try:
        deployments = db.query(Deployment).all()
        return jsonify([dep.to_dict() for dep in deployments])
    finally:
        db.close()

@app.route('/api/deployments', methods=['POST'])
def create_deployment():
    """Create a new deployment."""
    data = request.get_json()
    db = get_db()
    try:
        deployment = Deployment(
            deployment_id=data.get('deployment_id', str(uuid.uuid4())),
            name=data.get('name'),
            description=data.get('description'),
            environment=data.get('environment', 'production'),
            deployment_type=data.get('deployment_type', 'blue_green'),
            traffic_percentage=data.get('traffic_percentage', 100.0),
            endpoint_url=data.get('endpoint_url'),
            instance_type=data.get('instance_type'),
            instance_count=data.get('instance_count', 1),
            model_version_id=data.get('model_version_id'),
            status='deploying'
        )
        db.add(deployment)
        db.commit()
        db.refresh(deployment)
        return jsonify(deployment.to_dict()), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

# Monitoring API
@app.route('/api/monitoring/metrics', methods=['GET'])
def get_metrics():
    """Get model performance metrics."""
    db = get_db()
    try:
        metrics = db.query(ModelMetrics).order_by(ModelMetrics.timestamp.desc()).limit(100).all()
        return jsonify([metric.to_dict() for metric in metrics])
    finally:
        db.close()

@app.route('/api/monitoring/metrics', methods=['POST'])
def log_metrics():
    """Log model performance metrics."""
    data = request.get_json()
    db = get_db()
    try:
        metrics = ModelMetrics(
            model_version_id=data.get('model_version_id'),
            deployment_id=data.get('deployment_id'),
            accuracy=data.get('accuracy'),
            precision=data.get('precision'),
            recall=data.get('recall'),
            f1_score=data.get('f1_score'),
            auc_score=data.get('auc_score'),
            prediction_count=data.get('prediction_count', 0),
            error_count=data.get('error_count', 0),
            avg_latency=data.get('avg_latency'),
            p95_latency=data.get('p95_latency'),
            p99_latency=data.get('p99_latency'),
            cpu_usage=data.get('cpu_usage'),
            memory_usage=data.get('memory_usage'),
            gpu_usage=data.get('gpu_usage'),
            custom_metrics=data.get('custom_metrics', {})
        )
        db.add(metrics)
        db.commit()
        db.refresh(metrics)
        return jsonify(metrics.to_dict()), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/monitoring/drift', methods=['GET'])
def get_drift_detection():
    """Get drift detection results."""
    db = get_db()
    try:
        drift_results = db.query(DriftDetection).order_by(DriftDetection.timestamp.desc()).limit(50).all()
        return jsonify([result.to_dict() for result in drift_results])
    finally:
        db.close()

@app.route('/api/monitoring/alerts', methods=['GET'])
def get_alerts():
    """Get active alerts."""
    db = get_db()
    try:
        alerts = db.query(Alert).filter(Alert.status == 'active').order_by(Alert.triggered_at.desc()).all()
        return jsonify([alert.to_dict() for alert in alerts])
    finally:
        db.close()

# Prediction API
@app.route('/api/predict', methods=['POST'])
def predict():
    """Make a prediction (mock implementation)."""
    data = request.get_json()
    
    # Mock prediction logic
    import random
    prediction = random.choice([0, 1])
    probability = random.random()
    confidence = random.uniform(0.7, 0.95)
    
    # Log prediction
    db = get_db()
    try:
        log_entry = PredictionLog(
            request_id=str(uuid.uuid4()),
            model_version_id=data.get('model_version_id', 1),
            deployment_id=data.get('deployment_id', 1),
            input_hash='mock_hash',
            input_features=list(data.get('features', {}).keys()),
            prediction={'class': prediction},
            prediction_probability={'class_0': 1-probability, 'class_1': probability},
            confidence_score=confidence,
            latency=random.uniform(10, 100),
            user_id=data.get('user_id'),
            session_id=data.get('session_id')
        )
        db.add(log_entry)
        db.commit()
    except Exception as e:
        print(f"Error logging prediction: {e}")
    finally:
        db.close()
    
    return jsonify({
        'prediction': prediction,
        'probability': probability,
        'confidence': confidence,
        'model_version': '1.0.0',
        'timestamp': datetime.utcnow().isoformat()
    })

# Dashboard API
@app.route('/api/dashboard/overview', methods=['GET'])
def dashboard_overview():
    """Get dashboard overview data."""
    db = get_db()
    try:
        # Get counts
        model_count = db.query(ModelVersion).count()
        experiment_count = db.query(Experiment).count()
        deployment_count = db.query(Deployment).count()
        active_alerts = db.query(Alert).filter(Alert.status == 'active').count()
        
        # Get recent metrics
        recent_metrics = db.query(ModelMetrics).order_by(ModelMetrics.timestamp.desc()).first()
        
        return jsonify({
            'model_count': model_count,
            'experiment_count': experiment_count,
            'deployment_count': deployment_count,
            'active_alerts': active_alerts,
            'recent_metrics': recent_metrics.to_dict() if recent_metrics else None,
            'timestamp': datetime.utcnow().isoformat()
        })
    finally:
        db.close()

# Initialize sample data
@app.route('/api/init-sample-data', methods=['POST'])
def init_sample_data():
    """Initialize sample data for demonstration."""
    db = get_db()
    try:
        # Create sample model
        model = ModelVersion(
            name='fraud_detection_model',
            version='1.0.0',
            algorithm='random_forest',
            framework='scikit-learn',
            description='Fraud detection model for credit card transactions',
            tags=['fraud', 'classification', 'production'],
            accuracy=0.95,
            precision=0.92,
            recall=0.88,
            f1_score=0.90,
            auc_score=0.96,
            training_dataset_size=10000,
            training_duration=120.5,
            hyperparameters={'n_estimators': 100, 'max_depth': 10},
            status='deployed',
            stage='production'
        )
        db.add(model)
        db.commit()
        db.refresh(model)
        
        # Create sample deployment
        deployment = Deployment(
            deployment_id='fraud-model-prod-001',
            name='Fraud Detection Production',
            description='Production deployment of fraud detection model',
            environment='production',
            deployment_type='blue_green',
            traffic_percentage=100.0,
            endpoint_url='https://api.company.com/fraud/predict',
            instance_type='t3.medium',
            instance_count=3,
            model_version_id=model.id,
            status='active'
        )
        db.add(deployment)
        db.commit()
        
        # Create sample metrics
        import random
        for i in range(10):
            metrics = ModelMetrics(
                model_version_id=model.id,
                deployment_id=deployment.id,
                accuracy=random.uniform(0.90, 0.96),
                precision=random.uniform(0.88, 0.94),
                recall=random.uniform(0.85, 0.92),
                f1_score=random.uniform(0.87, 0.93),
                prediction_count=random.randint(100, 1000),
                error_count=random.randint(0, 10),
                avg_latency=random.uniform(50, 150),
                cpu_usage=random.uniform(20, 80),
                memory_usage=random.uniform(30, 70)
            )
            db.add(metrics)
        
        db.commit()
        return jsonify({'message': 'Sample data initialized successfully'})
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

# Static file serving
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return jsonify({
                'message': 'MLOps Pipeline API',
                'version': '1.0.0',
                'endpoints': [
                    '/api/health',
                    '/api/models',
                    '/api/experiments',
                    '/api/deployments',
                    '/api/monitoring/metrics',
                    '/api/monitoring/drift',
                    '/api/monitoring/alerts',
                    '/api/predict',
                    '/api/dashboard/overview'
                ]
            })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
