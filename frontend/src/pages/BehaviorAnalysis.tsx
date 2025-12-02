import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Dataset {
  dataset_id: string;
  name: string;
  status: string;
  total_records: number | null;
  treatment_count: number | null;
  control_count: number | null;
  churn_rate_treatment: number | null;
  churn_rate_control: number | null;
  created_at: string | null;
  completed_at: string | null;
}

interface DatasetStats {
  dataset_id: string;
  total_customers: number;
  segments: { [key: string]: number };
  risk_levels: { [key: string]: number };
  avg_churn_risk: number;
  avg_clv: number;
  treatment_effect: number;
}

const BehaviorAnalysis: React.FC = () => {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [selectedDataset, setSelectedDataset] = useState<string | null>(null);
  const [stats, setStats] = useState<DatasetStats | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  // Form state
  const [datasetName, setDatasetName] = useState('');
  const [datasetType, setDatasetType] = useState<'criteo' | 'hillstrom' | 'financial' | 'b2b' | 'telco'>('criteo');
  const [file, setFile] = useState<File | null>(null);

  const API_BASE = 'http://localhost:5000/api/v1';

  useEffect(() => {
    fetchDatasets();
  }, []);

  useEffect(() => {
    if (selectedDataset) {
      fetchStats(selectedDataset);
    }
  }, [selectedDataset]);

  const fetchDatasets = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_BASE}/behavior/datasets`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setDatasets(response.data);
    } catch (error) {
      console.error('Error fetching datasets:', error);
    }
  };

  const fetchStats = async (datasetId: string) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_BASE}/behavior/datasets/${datasetId}/stats`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!file || !datasetName) {
      alert('Please provide dataset name and file');
      return;
    }

    setUploading(true);
    setUploadProgress(0);

    try {
      const token = localStorage.getItem('token');
      const formData = new FormData();
      formData.append('file', file);
      formData.append('dataset_name', datasetName);
      formData.append('dataset_type', datasetType);
      formData.append('auto_train', 'true');

      const response = await axios.post(
        `${API_BASE}/behavior/upload-data`,
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'
          },
          onUploadProgress: (progressEvent) => {
            const progress = progressEvent.total
              ? Math.round((progressEvent.loaded * 100) / progressEvent.total)
              : 0;
            setUploadProgress(progress);
          }
        }
      );

      alert(`Dataset uploaded successfully! Status: ${response.data.status}`);

      // Reset form
      setDatasetName('');
      setFile(null);
      setUploading(false);
      setUploadProgress(0);

      // Refresh datasets
      fetchDatasets();
    } catch (error) {
      console.error('Error uploading dataset:', error);
      alert('Error uploading dataset');
      setUploading(false);
    }
  };

  const getStatusBadge = (status: string) => {
    const colors: { [key: string]: string } = {
      uploading: 'bg-blue-100 text-blue-800',
      processing: 'bg-yellow-100 text-yellow-800',
      normalizing: 'bg-purple-100 text-purple-800',
      completed: 'bg-green-100 text-green-800',
      failed: 'bg-red-100 text-red-800'
    };

    return (
      <span className={`px-2 py-1 rounded-full text-xs font-semibold ${colors[status] || 'bg-gray-100 text-gray-800'}`}>
        {status.toUpperCase()}
      </span>
    );
  };

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Customer Behavior Analysis</h1>

      {/* Upload Section */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Upload Dataset</h2>

        <form onSubmit={handleUpload} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Dataset Name
            </label>
            <input
              type="text"
              value={datasetName}
              onChange={(e) => setDatasetName(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="e.g., Q4 2024 Customer Data"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Dataset Type
            </label>
            <select
              value={datasetType}
              onChange={(e) => setDatasetType(e.target.value as any)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="criteo">Criteo (Advertising)</option>
              <option value="hillstrom">Hillstrom (Email Marketing)</option>
              <option value="financial">Financial Services</option>
              <option value="b2b">B2B SaaS</option>
              <option value="telco">Telecom</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              CSV File
            </label>
            <input
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
            {file && (
              <p className="mt-2 text-sm text-gray-600">
                Selected: {file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)
              </p>
            )}
          </div>

          {uploading && (
            <div>
              <div className="w-full bg-gray-200 rounded-full h-2.5">
                <div
                  className="bg-blue-600 h-2.5 rounded-full transition-all duration-300"
                  style={{ width: `${uploadProgress}%` }}
                ></div>
              </div>
              <p className="text-sm text-gray-600 mt-2">Uploading... {uploadProgress}%</p>
            </div>
          )}

          <button
            type="submit"
            disabled={uploading}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            {uploading ? 'Uploading...' : 'Upload & Process'}
          </button>
        </form>

        <div className="mt-4 p-4 bg-blue-50 rounded-md">
          <h3 className="font-semibold text-sm text-blue-900 mb-2">What happens after upload?</h3>
          <ul className="text-sm text-blue-800 space-y-1">
            <li>✓ Schema normalized to universal RFM framework</li>
            <li>✓ ML models trained (churn prediction + uplift modeling)</li>
            <li>✓ Behavior summaries generated for each customer</li>
            <li>✓ Intervention recommendations calculated</li>
          </ul>
        </div>
      </div>

      {/* Datasets List */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Your Datasets</h2>

        {datasets.length === 0 ? (
          <p className="text-gray-600">No datasets uploaded yet. Upload your first dataset above!</p>
        ) : (
          <div className="space-y-3">
            {datasets.map((dataset) => (
              <div
                key={dataset.dataset_id}
                className={`p-4 border rounded-lg cursor-pointer transition-all ${
                  selectedDataset === dataset.dataset_id
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
                onClick={() => setSelectedDataset(dataset.dataset_id)}
              >
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h3 className="font-semibold text-lg">{dataset.name}</h3>
                    <p className="text-sm text-gray-600">ID: {dataset.dataset_id}</p>
                  </div>
                  {getStatusBadge(dataset.status)}
                </div>

                {dataset.total_records && (
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-3 text-sm">
                    <div>
                      <p className="text-gray-600">Total Records</p>
                      <p className="font-semibold">{dataset.total_records.toLocaleString()}</p>
                    </div>
                    <div>
                      <p className="text-gray-600">Treatment Group</p>
                      <p className="font-semibold">{dataset.treatment_count?.toLocaleString() || 'N/A'}</p>
                    </div>
                    <div>
                      <p className="text-gray-600">Control Group</p>
                      <p className="font-semibold">{dataset.control_count?.toLocaleString() || 'N/A'}</p>
                    </div>
                    <div>
                      <p className="text-gray-600">Baseline Uplift</p>
                      <p className="font-semibold">
                        {dataset.churn_rate_control && dataset.churn_rate_treatment
                          ? `${((dataset.churn_rate_control - dataset.churn_rate_treatment) * 100).toFixed(2)}%`
                          : 'N/A'}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Dataset Statistics */}
      {stats && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Dataset Statistics</h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <div className="bg-blue-50 p-4 rounded-lg">
              <p className="text-sm text-blue-600 font-semibold">Total Customers</p>
              <p className="text-3xl font-bold text-blue-900">{stats.total_customers.toLocaleString()}</p>
            </div>

            <div className="bg-purple-50 p-4 rounded-lg">
              <p className="text-sm text-purple-600 font-semibold">Avg Churn Risk</p>
              <p className="text-3xl font-bold text-purple-900">{stats.avg_churn_risk.toFixed(1)}%</p>
            </div>

            <div className="bg-green-50 p-4 rounded-lg">
              <p className="text-sm text-green-600 font-semibold">Avg CLV</p>
              <p className="text-3xl font-bold text-green-900">${stats.avg_clv.toFixed(2)}</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Segments */}
            <div>
              <h3 className="font-semibold mb-3">Customer Segments</h3>
              <div className="space-y-2">
                {Object.entries(stats.segments).map(([segment, count]) => (
                  <div key={segment} className="flex justify-between items-center p-2 bg-gray-50 rounded">
                    <span className="text-sm font-medium">{segment}</span>
                    <span className="text-sm text-gray-600">
                      {count} ({((count / stats.total_customers) * 100).toFixed(1)}%)
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Risk Levels */}
            <div>
              <h3 className="font-semibold mb-3">Risk Levels</h3>
              <div className="space-y-2">
                {Object.entries(stats.risk_levels).map(([level, count]) => {
                  const colors: { [key: string]: string } = {
                    Critical: 'bg-red-50 text-red-700',
                    High: 'bg-orange-50 text-orange-700',
                    Medium: 'bg-yellow-50 text-yellow-700',
                    Low: 'bg-green-50 text-green-700'
                  };

                  return (
                    <div
                      key={level}
                      className={`flex justify-between items-center p-2 rounded ${colors[level] || 'bg-gray-50'}`}
                    >
                      <span className="text-sm font-medium">{level}</span>
                      <span className="text-sm">
                        {count} ({((count / stats.total_customers) * 100).toFixed(1)}%)
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          <div className="mt-6 p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg">
            <p className="text-sm font-semibold text-gray-700">Treatment Effect</p>
            <p className="text-2xl font-bold text-gray-900">
              {(stats.treatment_effect * 100).toFixed(2)}% reduction in churn
            </p>
            <p className="text-sm text-gray-600 mt-1">
              Customers who received treatment had {(stats.treatment_effect * 100).toFixed(2)}% lower churn rate
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default BehaviorAnalysis;
