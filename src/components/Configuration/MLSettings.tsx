import React from 'react';
import { motion } from 'framer-motion';
import { Brain, Target } from 'lucide-react';
import { useAppContext } from '../../contexts/AppContext';

const MLSettings: React.FC = () => {
  const { config, updateConfig } = useAppContext();

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
          <Brain className="w-5 h-5 mr-2" />
          Machine Learning Models
        </h3>
        
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
              Active Models
            </label>
            <div className="grid grid-cols-3 gap-3">
              {(['autoencoder', 'isolation_forest', 'both'] as const).map((model) => (
                <motion.button
                  key={model}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => updateConfig({ mlModel: model })}
                  className={`px-4 py-3 rounded-lg font-medium transition-colors text-center ${
                    config.mlModel === model
                      ? 'bg-blue-500 text-white shadow-md'
                      : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                  }`}
                >
                  {model === 'autoencoder' && 'Autoencoder'}
                  {model === 'isolation_forest' && 'Isolation Forest'}
                  {model === 'both' && 'Both Models'}
                </motion.button>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
              Feature Extraction Level
            </label>
            <div className="grid grid-cols-3 gap-3">
              {(['advanced', 'standard', 'low'] as const).map((level) => (
                <motion.button
                  key={level}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => updateConfig({ featureLevel: level })}
                  className={`px-4 py-3 rounded-lg font-medium capitalize transition-colors ${
                    config.featureLevel === level
                      ? 'bg-green-500 text-white shadow-md'
                      : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                  }`}
                >
                  {level}
                </motion.button>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
          <Target className="w-5 h-5 mr-2" />
          Model Information
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
            <h4 className="font-medium text-blue-900 dark:text-blue-400 mb-2">Autoencoder</h4>
            <p className="text-sm text-blue-700 dark:text-blue-300">
              Deep learning model that learns normal network patterns and identifies anomalies 
              by reconstruction error.
            </p>
          </div>
          
          <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
            <h4 className="font-medium text-green-900 dark:text-green-400 mb-2">Isolation Forest</h4>
            <p className="text-sm text-green-700 dark:text-green-300">
              Unsupervised algorithm that isolates anomalies by randomly selecting features 
              and split values.
            </p>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default MLSettings;