import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Alert, AlertDescription } from '@/components/ui/alert.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell, AreaChart, Area } from 'recharts'
import { 
  Cpu, Database, GitBranch, Activity, TrendingUp, Clock, AlertTriangle, 
  CheckCircle, Settings, Upload, Download, Play, Pause, RotateCcw,
  Eye, Edit, Trash2, Plus, Filter, Search, Bell, Users, Target
} from 'lucide-react'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('overview')
  const [models, setModels] = useState([
    {
      id: 1,
      name: 'fraud-detection-v2.1',
      version: '2.1.0',
      status: 'production',
      accuracy: 95.8,
      lastUpdated: '2024-01-15',
      deployments: 3,
      experiments: 12
    },
    {
      id: 2,
      name: 'customer-churn-v1.3',
      version: '1.3.2',
      status: 'staging',
      accuracy: 87.2,
      lastUpdated: '2024-01-14',
      deployments: 1,
      experiments: 8
    },
    {
      id: 3,
      name: 'recommendation-engine-v3.0',
      version: '3.0.1',
      status: 'development',
      accuracy: 92.1,
      lastUpdated: '2024-01-13',
      deployments: 0,
      experiments: 15
    }
  ])

  const [deployments, setDeployments] = useState([
    {
      id: 1,
      modelName: 'fraud-detection-v2.1',
      environment: 'production',
      strategy: 'blue-green',
      status: 'healthy',
      traffic: 100,
      instances: 5,
      cpu: 45,
      memory: 62,
      requests: 1250
    },
    {
      id: 2,
      modelName: 'fraud-detection-v2.0',
      environment: 'production',
      strategy: 'canary',
      status: 'draining',
      traffic: 0,
      instances: 2,
      cpu: 12,
      memory: 28,
      requests: 0
    },
    {
      id: 3,
      modelName: 'customer-churn-v1.3',
      environment: 'staging',
      strategy: 'rolling',
      status: 'healthy',
      traffic: 100,
      instances: 2,
      cpu: 38,
      memory: 55,
      requests: 340
    }
  ])

  const [experiments, setExperiments] = useState([
    {
      id: 1,
      name: 'fraud-detection-hyperopt',
      model: 'fraud-detection',
      status: 'completed',
      accuracy: 96.2,
      precision: 94.1,
      recall: 89.7,
      f1Score: 91.8,
      duration: '2h 34m',
      startTime: '2024-01-15 10:30'
    },
    {
      id: 2,
      name: 'churn-feature-selection',
      model: 'customer-churn',
      status: 'running',
      accuracy: 87.8,
      precision: 85.2,
      recall: 82.1,
      f1Score: 83.6,
      duration: '1h 12m',
      startTime: '2024-01-15 14:15'
    },
    {
      id: 3,
      name: 'recommendation-deep-learning',
      model: 'recommendation-engine',
      status: 'failed',
      accuracy: 0,
      precision: 0,
      recall: 0,
      f1Score: 0,
      duration: '45m',
      startTime: '2024-01-15 09:00'
    }
  ])

  const [alerts, setAlerts] = useState([
    {
      id: 1,
      type: 'drift',
      severity: 'high',
      message: 'Data drift detected in fraud-detection-v2.1',
      timestamp: '2024-01-15 15:30',
      model: 'fraud-detection-v2.1'
    },
    {
      id: 2,
      type: 'performance',
      severity: 'medium',
      message: 'Model accuracy dropped below threshold (85%)',
      timestamp: '2024-01-15 14:45',
      model: 'customer-churn-v1.3'
    },
    {
      id: 3,
      type: 'system',
      severity: 'low',
      message: 'High memory usage in production environment',
      timestamp: '2024-01-15 13:20',
      model: 'fraud-detection-v2.1'
    }
  ])

  const [systemMetrics, setSystemMetrics] = useState({
    totalModels: 12,
    activeDeployments: 8,
    runningExperiments: 3,
    totalAlerts: 15
  })

  // Mock performance data
  const performanceData = [
    { time: '00:00', accuracy: 95.2, latency: 45, throughput: 1200 },
    { time: '04:00', accuracy: 95.8, latency: 42, throughput: 980 },
    { time: '08:00', accuracy: 94.9, latency: 48, throughput: 1450 },
    { time: '12:00', accuracy: 95.5, latency: 44, throughput: 1680 },
    { time: '16:00', accuracy: 95.1, latency: 46, throughput: 1520 },
    { time: '20:00', accuracy: 95.7, latency: 43, throughput: 1380 }
  ]

  const resourceUsage = [
    { name: 'CPU', usage: 45, limit: 80 },
    { name: 'Memory', usage: 62, limit: 85 },
    { name: 'Storage', usage: 34, limit: 90 },
    { name: 'Network', usage: 28, limit: 70 }
  ]

  const modelStatusData = [
    { name: 'Production', value: 5, color: '#10b981' },
    { name: 'Staging', value: 3, color: '#f59e0b' },
    { name: 'Development', value: 4, color: '#3b82f6' }
  ]

  const getStatusColor = (status) => {
    switch (status) {
      case 'production': case 'healthy': case 'completed': return 'bg-green-100 text-green-800'
      case 'staging': case 'running': return 'bg-yellow-100 text-yellow-800'
      case 'development': case 'draining': case 'failed': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'high': return 'bg-red-100 text-red-800'
      case 'medium': return 'bg-yellow-100 text-yellow-800'
      case 'low': return 'bg-blue-100 text-blue-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  // Simulate real-time updates
  useEffect(() => {
    const interval = setInterval(() => {
      setSystemMetrics(prev => ({
        ...prev,
        totalAlerts: prev.totalAlerts + (Math.random() > 0.9 ? 1 : 0)
      }))
    }, 10000)

    return () => clearInterval(interval)
  }, [])

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto p-6">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Cpu className="h-8 w-8 text-blue-600" />
              <div>
                <h1 className="text-3xl font-bold text-gray-900">MLOps Dashboard</h1>
                <p className="text-gray-600">Machine Learning Operations Management Platform</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <Button variant="outline" size="sm">
                <Bell className="h-4 w-4 mr-2" />
                Alerts ({alerts.length})
              </Button>
              <Button size="sm">
                <Plus className="h-4 w-4 mr-2" />
                New Model
              </Button>
            </div>
          </div>
        </div>

        {/* System Overview Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Total Models</p>
                  <p className="text-2xl font-bold text-gray-900">{systemMetrics.totalModels}</p>
                </div>
                <Database className="h-8 w-8 text-blue-600" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Active Deployments</p>
                  <p className="text-2xl font-bold text-green-600">{systemMetrics.activeDeployments}</p>
                </div>
                <Activity className="h-8 w-8 text-green-600" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Running Experiments</p>
                  <p className="text-2xl font-bold text-orange-600">{systemMetrics.runningExperiments}</p>
                </div>
                <Target className="h-8 w-8 text-orange-600" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Active Alerts</p>
                  <p className="text-2xl font-bold text-red-600">{systemMetrics.totalAlerts}</p>
                </div>
                <AlertTriangle className="h-8 w-8 text-red-600" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Content Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-6">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="models">Models</TabsTrigger>
            <TabsTrigger value="deployments">Deployments</TabsTrigger>
            <TabsTrigger value="experiments">Experiments</TabsTrigger>
            <TabsTrigger value="monitoring">Monitoring</TabsTrigger>
            <TabsTrigger value="alerts">Alerts</TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Performance Metrics */}
              <Card>
                <CardHeader>
                  <CardTitle>Model Performance (24h)</CardTitle>
                  <CardDescription>Accuracy, latency, and throughput trends</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={performanceData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="time" />
                      <YAxis />
                      <Tooltip />
                      <Line type="monotone" dataKey="accuracy" stroke="#10b981" strokeWidth={2} name="Accuracy %" />
                      <Line type="monotone" dataKey="latency" stroke="#f59e0b" strokeWidth={2} name="Latency (ms)" />
                    </LineChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              {/* Resource Usage */}
              <Card>
                <CardHeader>
                  <CardTitle>Resource Usage</CardTitle>
                  <CardDescription>Current system resource utilization</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {resourceUsage.map(resource => (
                      <div key={resource.name}>
                        <div className="flex justify-between text-sm mb-1">
                          <span>{resource.name}</span>
                          <span>{resource.usage}% / {resource.limit}%</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div 
                            className={`h-2 rounded-full ${resource.usage > resource.limit * 0.8 ? 'bg-red-600' : 'bg-blue-600'}`}
                            style={{ width: `${(resource.usage / resource.limit) * 100}%` }}
                          ></div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Model Status Distribution */}
              <Card>
                <CardHeader>
                  <CardTitle>Model Status Distribution</CardTitle>
                  <CardDescription>Models by deployment stage</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={250}>
                    <PieChart>
                      <Pie
                        data={modelStatusData}
                        cx="50%"
                        cy="50%"
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                        label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                      >
                        {modelStatusData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              {/* Recent Activity */}
              <Card>
                <CardHeader>
                  <CardTitle>Recent Activity</CardTitle>
                  <CardDescription>Latest model and deployment activities</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center gap-3 p-2 bg-green-50 rounded">
                      <CheckCircle className="h-4 w-4 text-green-600" />
                      <div className="text-sm">
                        <div className="font-medium">Model deployed successfully</div>
                        <div className="text-gray-500">fraud-detection-v2.1 to production</div>
                      </div>
                      <div className="text-xs text-gray-500 ml-auto">2m ago</div>
                    </div>
                    
                    <div className="flex items-center gap-3 p-2 bg-blue-50 rounded">
                      <Play className="h-4 w-4 text-blue-600" />
                      <div className="text-sm">
                        <div className="font-medium">Experiment started</div>
                        <div className="text-gray-500">churn-feature-selection</div>
                      </div>
                      <div className="text-xs text-gray-500 ml-auto">15m ago</div>
                    </div>
                    
                    <div className="flex items-center gap-3 p-2 bg-yellow-50 rounded">
                      <AlertTriangle className="h-4 w-4 text-yellow-600" />
                      <div className="text-sm">
                        <div className="font-medium">Drift alert triggered</div>
                        <div className="text-gray-500">Data drift in fraud-detection-v2.1</div>
                      </div>
                      <div className="text-xs text-gray-500 ml-auto">1h ago</div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Models Tab */}
          <TabsContent value="models" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Model Registry</CardTitle>
                <CardDescription>Manage and track all machine learning models</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {models.map(model => (
                    <div key={model.id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center gap-4">
                        <div>
                          <h3 className="font-medium">{model.name}</h3>
                          <p className="text-sm text-gray-500">Version {model.version}</p>
                        </div>
                        <Badge className={getStatusColor(model.status)}>
                          {model.status}
                        </Badge>
                      </div>
                      
                      <div className="flex items-center gap-6">
                        <div className="text-center">
                          <div className="text-sm font-medium">{model.accuracy}%</div>
                          <div className="text-xs text-gray-500">Accuracy</div>
                        </div>
                        <div className="text-center">
                          <div className="text-sm font-medium">{model.deployments}</div>
                          <div className="text-xs text-gray-500">Deployments</div>
                        </div>
                        <div className="text-center">
                          <div className="text-sm font-medium">{model.experiments}</div>
                          <div className="text-xs text-gray-500">Experiments</div>
                        </div>
                        
                        <div className="flex gap-2">
                          <Button variant="outline" size="sm">
                            <Eye className="h-4 w-4" />
                          </Button>
                          <Button variant="outline" size="sm">
                            <Edit className="h-4 w-4" />
                          </Button>
                          <Button variant="outline" size="sm">
                            <Play className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Deployments Tab */}
          <TabsContent value="deployments" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Active Deployments</CardTitle>
                <CardDescription>Monitor and manage model deployments across environments</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {deployments.map(deployment => (
                    <div key={deployment.id} className="p-4 border rounded-lg">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center gap-4">
                          <div>
                            <h3 className="font-medium">{deployment.modelName}</h3>
                            <p className="text-sm text-gray-500">{deployment.environment} • {deployment.strategy}</p>
                          </div>
                          <Badge className={getStatusColor(deployment.status)}>
                            {deployment.status}
                          </Badge>
                        </div>
                        
                        <div className="flex gap-2">
                          <Button variant="outline" size="sm">
                            <Settings className="h-4 w-4" />
                          </Button>
                          <Button variant="outline" size="sm">
                            <Pause className="h-4 w-4" />
                          </Button>
                          <Button variant="outline" size="sm">
                            <RotateCcw className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                      
                      <div className="grid grid-cols-2 md:grid-cols-6 gap-4 text-sm">
                        <div>
                          <div className="font-medium">{deployment.traffic}%</div>
                          <div className="text-gray-500">Traffic</div>
                        </div>
                        <div>
                          <div className="font-medium">{deployment.instances}</div>
                          <div className="text-gray-500">Instances</div>
                        </div>
                        <div>
                          <div className="font-medium">{deployment.cpu}%</div>
                          <div className="text-gray-500">CPU</div>
                        </div>
                        <div>
                          <div className="font-medium">{deployment.memory}%</div>
                          <div className="text-gray-500">Memory</div>
                        </div>
                        <div>
                          <div className="font-medium">{deployment.requests}</div>
                          <div className="text-gray-500">Requests/min</div>
                        </div>
                        <div>
                          <div className="font-medium">98.9%</div>
                          <div className="text-gray-500">Uptime</div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Experiments Tab */}
          <TabsContent value="experiments" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Experiment Tracking</CardTitle>
                <CardDescription>Track and compare model training experiments</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {experiments.map(experiment => (
                    <div key={experiment.id} className="p-4 border rounded-lg">
                      <div className="flex items-center justify-between mb-3">
                        <div>
                          <h3 className="font-medium">{experiment.name}</h3>
                          <p className="text-sm text-gray-500">{experiment.model} • Started {experiment.startTime}</p>
                        </div>
                        <div className="flex items-center gap-3">
                          <Badge className={getStatusColor(experiment.status)}>
                            {experiment.status}
                          </Badge>
                          <span className="text-sm text-gray-500">{experiment.duration}</span>
                        </div>
                      </div>
                      
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                        <div>
                          <div className="font-medium">{experiment.accuracy}%</div>
                          <div className="text-gray-500">Accuracy</div>
                        </div>
                        <div>
                          <div className="font-medium">{experiment.precision}%</div>
                          <div className="text-gray-500">Precision</div>
                        </div>
                        <div>
                          <div className="font-medium">{experiment.recall}%</div>
                          <div className="text-gray-500">Recall</div>
                        </div>
                        <div>
                          <div className="font-medium">{experiment.f1Score}%</div>
                          <div className="text-gray-500">F1 Score</div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Monitoring Tab */}
          <TabsContent value="monitoring" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Model Performance Trends</CardTitle>
                  <CardDescription>Real-time performance monitoring</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <AreaChart data={performanceData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="time" />
                      <YAxis />
                      <Tooltip />
                      <Area type="monotone" dataKey="throughput" stackId="1" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.6} />
                    </AreaChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>System Health</CardTitle>
                  <CardDescription>Infrastructure and service status</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between p-3 bg-green-50 rounded">
                      <div className="flex items-center gap-3">
                        <CheckCircle className="h-5 w-5 text-green-600" />
                        <span className="font-medium">API Gateway</span>
                      </div>
                      <Badge className="bg-green-100 text-green-800">Healthy</Badge>
                    </div>
                    
                    <div className="flex items-center justify-between p-3 bg-green-50 rounded">
                      <div className="flex items-center gap-3">
                        <CheckCircle className="h-5 w-5 text-green-600" />
                        <span className="font-medium">Model Serving</span>
                      </div>
                      <Badge className="bg-green-100 text-green-800">Healthy</Badge>
                    </div>
                    
                    <div className="flex items-center justify-between p-3 bg-yellow-50 rounded">
                      <div className="flex items-center gap-3">
                        <AlertTriangle className="h-5 w-5 text-yellow-600" />
                        <span className="font-medium">Data Pipeline</span>
                      </div>
                      <Badge className="bg-yellow-100 text-yellow-800">Warning</Badge>
                    </div>
                    
                    <div className="flex items-center justify-between p-3 bg-green-50 rounded">
                      <div className="flex items-center gap-3">
                        <CheckCircle className="h-5 w-5 text-green-600" />
                        <span className="font-medium">Monitoring</span>
                      </div>
                      <Badge className="bg-green-100 text-green-800">Healthy</Badge>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Alerts Tab */}
          <TabsContent value="alerts" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Active Alerts</CardTitle>
                <CardDescription>Monitor and manage system alerts and notifications</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {alerts.map(alert => (
                    <div key={alert.id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center gap-4">
                        <AlertTriangle className="h-5 w-5 text-red-600" />
                        <div>
                          <h3 className="font-medium">{alert.message}</h3>
                          <p className="text-sm text-gray-500">{alert.model} • {alert.timestamp}</p>
                        </div>
                      </div>
                      
                      <div className="flex items-center gap-3">
                        <Badge className={getSeverityColor(alert.severity)}>
                          {alert.severity}
                        </Badge>
                        <Button variant="outline" size="sm">
                          Acknowledge
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

export default App
