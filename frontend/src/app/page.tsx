// Home.tsx
'use client';
import React from 'react';
import { Box } from '@mui/material';
import DataTable from '../components/DataTable';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';

const Home: React.FC = () => {
  return (
    <Box>
      <Header />
      <Box sx={{ display: 'flex', gap: 4, p: 4 }}>
        <DataTable />
        <Sidebar />
      </Box>
    </Box>
  );
};

export default Home;