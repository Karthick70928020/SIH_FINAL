import React from 'react';
import { motion } from 'framer-motion';
import { Moon, Sun, Activity, Pause, Play, Download } from 'lucide-react';
import { useAppContext } from '../../contexts/AppContext';

const Header: React.FC = () => {
  const { config, updateConfig, isCapturing, setIsCapturing } = useAppContext();

  const toggleDarkMode = () => {
    updateConfig({ darkMode: !config.darkMode });
  };

  const toggleCapture = () => {
    setIsCapturing(!isCapturing);
    // TODO: Send command to backend
  };

  const exportLogs = () => {
    // TODO: Implement log export
    console.log('Exporting logs...');
  };

  return (
    <motion.header 
      initial={{ y: -60 }}
      animate={{ y: 0 }}
      className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4 ml-64"
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            {isCapturing && (
              <motion.div
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ repeat: Infinity, duration: 1 }}
                className="w-3 h-3 bg-green-500 rounded-full"
              />
            )}
            <span className="text-sm font-medium text-gray-600 dark:text-gray-300">
              {isCapturing ? 'Capturing Live' : 'Idle'}
            </span>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={toggleCapture}
            className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-medium transition-colors ${
              isCapturing
                ? 'bg-red-500 text-white hover:bg-red-600'
                : 'bg-green-500 text-white hover:bg-green-600'
            }`}
          >
            {isCapturing ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
            <span>{isCapturing ? 'Stop' : 'Start'}</span>
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={exportLogs}
            className="flex items-center space-x-2 px-4 py-2 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600 transition-colors"
          >
            <Download className="w-4 h-4" />
            <span>Export</span>
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={toggleDarkMode}
            className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
          >
            {config.darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
          </motion.button>
        </div>
      </div>
    </motion.header>
  );
};

export default Header;