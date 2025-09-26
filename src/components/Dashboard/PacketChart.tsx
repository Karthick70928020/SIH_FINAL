import React from 'react';
import { motion } from 'framer-motion';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';
import { useAppContext } from '../../contexts/AppContext';

const PacketChart: React.FC = () => {
  const { chartData } = useAppContext();

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700"
    >
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        Real-time Packet Flow
      </h3>
      
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
            <XAxis 
              dataKey="timestamp" 
              className="text-gray-600 dark:text-gray-400"
            />
            <YAxis className="text-gray-600 dark:text-gray-400" />
            <Tooltip 
              contentStyle={{
                backgroundColor: 'rgba(255, 255, 255, 0.95)',
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
                color: '#374151'
              }}
            />
            <Legend />
            <Line
              type="monotone"
              dataKey="packets"
              stroke="#3B82F6"
              strokeWidth={2}
              dot={{ fill: '#3B82F6', strokeWidth: 2, r: 4 }}
              name="Packets"
            />
            <Line
              type="monotone"
              dataKey="anomalies"
              stroke="#EF4444"
              strokeWidth={2}
              dot={{ fill: '#EF4444', strokeWidth: 2, r: 4 }}
              name="Anomalies"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </motion.div>
  );
};

export default PacketChart;