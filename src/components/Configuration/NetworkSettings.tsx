import React from 'react';
import { motion } from 'framer-motion';
import { useAppContext } from '../../contexts/AppContext';

const NetworkSettings: React.FC = () => {
  const { config, updateConfig, networkInterfaces } = useAppContext();

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Network Configuration
        </h3>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Network Interface
            </label>
            <select
              value={config.networkInterface}
              onChange={(e) => updateConfig({ networkInterface: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
            >
              {networkInterfaces.map(interface => (
                <option key={interface.name} value={interface.name}>
                  {interface.name} - {interface.description}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Packet Buffer Size
            </label>
            <div className="flex items-center space-x-4">
              <input
                type="range"
                min="100"
                max="10000"
                step="100"
                value={config.bufferSize}
                onChange={(e) => updateConfig({ bufferSize: Number(e.target.value) })}
                className="flex-1"
              />
              <span className="text-sm font-medium text-gray-900 dark:text-white min-w-0">
                {config.bufferSize} packets
              </span>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Analysis Depth
            </label>
            <div className="grid grid-cols-3 gap-2">
              {(['basic', 'intermediate', 'deep'] as const).map((depth) => (
                <motion.button
                  key={depth}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => updateConfig({ analysisDepth: depth })}
                  className={`px-4 py-2 rounded-lg font-medium capitalize transition-colors ${
                    config.analysisDepth === depth
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                  }`}
                >
                  {depth}
                </motion.button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default NetworkSettings;