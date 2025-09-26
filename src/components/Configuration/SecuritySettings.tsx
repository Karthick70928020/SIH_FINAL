import React from 'react';
import { motion } from 'framer-motion';
import { Shield, Lock, Key } from 'lucide-react';
import { useAppContext } from '../../contexts/AppContext';

const SecuritySettings: React.FC = () => {
  const { config, updateConfig } = useAppContext();

  const algorithms = [
    { value: 'RSA', label: 'RSA', description: 'Asymmetric encryption with public/private key pairs' },
    { value: 'SHA', label: 'SHA-256', description: 'Secure Hash Algorithm for data integrity' },
    { value: 'AES-256', label: 'AES-256', description: 'Advanced Encryption Standard 256-bit' },
    { value: 'AES-192', label: 'AES-192', description: 'Advanced Encryption Standard 192-bit' },
  ] as const;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
          <Shield className="w-5 h-5 mr-2" />
          Encryption Configuration
        </h3>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
              Encryption Algorithm
            </label>
            <div className="grid grid-cols-2 gap-3">
              {algorithms.map((algorithm) => (
                <motion.button
                  key={algorithm.value}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => updateConfig({ encryptionAlgorithm: algorithm.value })}
                  className={`p-4 rounded-lg border text-left transition-colors ${
                    config.encryptionAlgorithm === algorithm.value
                      ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                      : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500'
                  }`}
                >
                  <div className="flex items-center space-x-2 mb-2">
                    <Lock className="w-4 h-4" />
                    <span className="font-medium text-gray-900 dark:text-white">
                      {algorithm.label}
                    </span>
                  </div>
                  <p className="text-xs text-gray-600 dark:text-gray-400">
                    {algorithm.description}
                  </p>
                </motion.button>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
          <Key className="w-5 h-5 mr-2" />
          Security Features
        </h3>
        
        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
            <div>
              <h4 className="font-medium text-green-900 dark:text-green-400">Auto-Encryption</h4>
              <p className="text-sm text-green-700 dark:text-green-300">
                All exported logs are automatically encrypted
              </p>
            </div>
            <div className="w-3 h-3 bg-green-500 rounded-full"></div>
          </div>
          
          <div className="flex items-center justify-between p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
            <div>
              <h4 className="font-medium text-blue-900 dark:text-blue-400">Secure Transport</h4>
              <p className="text-sm text-blue-700 dark:text-blue-300">
                WebSocket connections use TLS encryption
              </p>
            </div>
            <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
          </div>
          
          <div className="flex items-center justify-between p-4 bg-orange-50 dark:bg-orange-900/20 rounded-lg">
            <div>
              <h4 className="font-medium text-orange-900 dark:text-orange-400">Data Integrity</h4>
              <p className="text-sm text-orange-700 dark:text-orange-300">
                Hash verification ensures data hasn't been tampered with
              </p>
            </div>
            <div className="w-3 h-3 bg-orange-500 rounded-full"></div>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default SecuritySettings;