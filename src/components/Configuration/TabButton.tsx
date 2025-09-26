import React from 'react';
import { motion } from 'framer-motion';
import { Video as LucideIcon } from 'lucide-react';

interface TabButtonProps {
  active: boolean;
  onClick: () => void;
  icon: LucideIcon;
  label: string;
}

const TabButton: React.FC<TabButtonProps> = ({ active, onClick, icon: Icon, label }) => {
  return (
    <motion.button
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      className={`flex items-center space-x-3 px-4 py-3 rounded-lg font-medium transition-all duration-200 ${
        active
          ? 'bg-blue-500 text-white shadow-md'
          : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 border border-gray-200 dark:border-gray-700'
      }`}
    >
      <Icon className="w-5 h-5" />
      <span>{label}</span>
    </motion.button>
  );
};

export default TabButton;