import React from 'react';
import { motion } from 'framer-motion';
import { AlertTriangle, Shield, Clock } from 'lucide-react';
import { useAppContext } from '../../contexts/AppContext';

const RecentPackets: React.FC = () => {
  const { packets } = useAppContext();
  const recentPackets = packets.slice(0, 5);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700"
    >
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
        <Clock className="w-5 h-5 mr-2" />
        Recent Packets
      </h3>
      
      <div className="space-y-3">
        {recentPackets.length === 0 ? (
          <p className="text-gray-500 dark:text-gray-400 text-center py-8">
            No packets captured yet
          </p>
        ) : (
          recentPackets.map((packet) => (
            <motion.div
              key={packet.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className={`p-4 rounded-lg border-l-4 ${
                packet.is_anomaly
                  ? 'border-red-500 bg-red-50 dark:bg-red-900/20'
                  : 'border-green-500 bg-green-50 dark:bg-green-900/20'
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  {packet.is_anomaly ? (
                    <AlertTriangle className="w-4 h-4 text-red-500" />
                  ) : (
                    <Shield className="w-4 h-4 text-green-500" />
                  )}
                  <div>
                    <div className="text-sm font-medium text-gray-900 dark:text-white">
                      {packet.source_ip} → {packet.destination_ip}
                    </div>
                    <div className="text-xs text-gray-500 dark:text-gray-400">
                      {packet.protocol} • {packet.length} bytes
                    </div>
                  </div>
                </div>
                <div className="text-xs text-gray-500 dark:text-gray-400">
                  {new Date(packet.timestamp).toLocaleTimeString()}
                </div>
              </div>
            </motion.div>
          ))
        )}
      </div>
    </motion.div>
  );
};

export default RecentPackets;