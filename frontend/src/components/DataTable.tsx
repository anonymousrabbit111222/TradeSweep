// DataTable.tsx
import React from 'react';
import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';

const data = [
  {
    date: '2023-04-26',
    senderTaxId: '123456789',
    senderName: 'Sender 1',
    recipientName: 'Recipient 1',
    tradingCountry: 'Country 1',
    hsCode: '1234',
    usdValue: 1000,
  },
  {
    date: '2023-04-27',
    senderTaxId: '987654321',
    senderName: 'Sender 2',
    recipientName: 'Recipient 2',
    tradingCountry: 'Country 2',
    hsCode: '5678',
    usdValue: 2000,
  },
  // Add more data as needed
];

const DataTable: React.FC = () => {
  return (
    <TableContainer component={Paper} sx={{ width: '70%', height: 'calc(100vh - 64px - 32px)' }}>
      <Table stickyHeader>
        <TableHead>
          <TableRow>
            <TableCell>Date</TableCell>
            <TableCell>Sender Tax ID</TableCell>
            <TableCell>Sender Name</TableCell>
            <TableCell>Recipient Name</TableCell>
            <TableCell>Trading Country</TableCell>
            <TableCell>HS Code</TableCell>
            <TableCell>USD Value</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map((row, index) => (
            <TableRow key={index}>
              <TableCell>{row.date}</TableCell>
              <TableCell>{row.senderTaxId}</TableCell>
              <TableCell>{row.senderName}</TableCell>
              <TableCell>{row.recipientName}</TableCell>
              <TableCell>{row.tradingCountry}</TableCell>
              <TableCell>{row.hsCode}</TableCell>
              <TableCell>{row.usdValue}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default DataTable;