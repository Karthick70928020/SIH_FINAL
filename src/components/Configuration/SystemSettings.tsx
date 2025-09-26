import React from 'react';
import { motion } from 'framer-motion';
import { useAppContext } from '../../contexts/AppContext';

const SystemSettings: React.FC = () => {
  const { config, updateConfig } = useAppContext();

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          General Settings
        </h3>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Packet Buffer Size
            </label>
            <select
              value={config.bufferSize}
              onChange={(e) => updateConfig({ bufferSize: Number(e.target.value) })}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
            >
              <option value={500}>500 packets</option>
              <option value={1000}>1,000 packets</option>
              <option value={5000}>5,000 packets</option>
              <option value={10000}>10,000 packets</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Analysis Depth
            </label>
            <select
              value={config.analysisDepth}
              onChange={(e) => updateConfig({ analysisDepth: e.target.value as any })}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
            >
              <option value="basic">Basic</option>
              <option value="intermediate">Intermediate</option>
              <option value="deep">Deep Analysis</option>
            </select>
          </div>

          <div className="flex items-center">
            <input
              id="darkMode"
              type="checkbox"
              checked={config.darkMode}
              onChange={(e) => updateConfig({ darkMode: e.target.checked })}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label htmlFor="darkMode" className="ml-2 block text-sm text-gray-700 dark:text-gray-300">
              Enable Dark Mode
            </label>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default SystemSettings;