import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Search, Filter, Download, AlertTriangle, Shield } from 'lucide-react';
import { useAppContext } from '../../contexts/AppContext';
import { PacketData } from '../../types';

const PacketTable: React.FC = () => {
  const { packets } = useAppContext();
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [sortBy, setSortBy] = useState('timestamp');

  const filteredPackets = packets.filter((packet) => {
    const matchesSearch = 
      packet.source_ip.includes(searchTerm) ||
      packet.destination_ip.includes(searchTerm) ||
      packet.protocol.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesFilter = 
      filterType === 'all' || 
      (filterType === 'anomalies' && packet.is_anomaly) ||
      (filterType === 'normal' && !packet.is_anomaly);

    return matchesSearch && matchesFilter;
  }).sort((a, b) => {
    switch (sortBy) {
      case 'timestamp':
        return new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime();
      case 'source_ip':
        return a.source_ip.localeCompare(b.source_ip);
      case 'protocol':
        return a.protocol.localeCompare(b.protocol);
      default:
        return 0;
    }
  });

  const exportLogs = () => {
    const dataStr = JSON.stringify(filteredPackets, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'network_logs.json';
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700"
    >
      <div className="p-6 border-b border-gray-200 dark:border-gray-700">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
          <div className="flex items-center space-x-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search by IP or protocol..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 w-64"
              />
            </div>

            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Packets</option>
              <option value="anomalies">Anomalies Only</option>
              <option value="normal">Normal Only</option>
            </select>

            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
            >
              <option value="timestamp">Sort by Time</option>
              <option value="source_ip">Sort by Source IP</option>
              <option value="protocol">Sort by Protocol</option>
            </select>
          </div>

          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={exportLogs}
            className="flex items-center space-x-2 px-4 py-2 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600 transition-colors"
          >
            <Download className="w-4 h-4" />
            <span>Export Logs</span>
          </motion.button>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Time
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Source IP
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Destination IP
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Protocol
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Length
              </th>
            </tr>
          </thead>
          <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            {filteredPackets.length === 0 ? (
              <tr>
                <td colSpan={6} className="px-6 py-12 text-center text-gray-500 dark:text-gray-400">
                  No packets match your current filters
                </td>
              </tr>
            ) : (
              filteredPackets.map((packet) => (
                <motion.tr
                  key={packet.id}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                >
                  <td className="px-6 py-4 whitespace-nowrap">
                    {packet.is_anomaly ? (
                      <div className="flex items-center text-red-500">
                        <AlertTriangle className="w-4 h-4 mr-1" />
                        <span className="text-xs font-medium">Anomaly</span>
                      </div>
                    ) : (
                      <div className="flex items-center text-green-500">
                        <Shield className="w-4 h-4 mr-1" />
                        <span className="text-xs font-medium">Normal</span>
                      </div>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                    {new Date(packet.timestamp).toLocaleTimeString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-900 dark:text-white">
                    {packet.source_ip}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-900 dark:text-white">
                    {packet.destination_ip}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="px-2 py-1 text-xs font-medium bg-blue-100 dark:bg-blue-900/20 text-blue-800 dark:text-blue-400 rounded-full">
                      {packet.protocol}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                    {packet.length} bytes
                  </td>
                </motion.tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </motion.div>
  );
};

export default PacketTable;