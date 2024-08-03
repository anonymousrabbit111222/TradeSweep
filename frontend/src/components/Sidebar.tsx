// Sidebar.tsx
import React, { useState } from 'react';
import {
  Box,
  Button,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  TextField,
  Typography,
  Paper,
  InputBase,
  IconButton,
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

const Sidebar: React.FC = () => {
  const [command, setCommand] = useState('');
  const [history, setHistory] = useState<string[]>([]);

  const handleCommandChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setCommand(event.target.value);
  };

  const handleCommandSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    if (command.trim() !== '') {
      setHistory([...history, command]);
      setCommand('');
    }
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, width: '30%' }}>
      <FormControl fullWidth>
        <InputLabel>Data.csv</InputLabel>
        <Select
          value=""
          label="Data.csv"
          sx={{
            backgroundColor:'#EBF0F8',
            '& .MuiOutlinedInput-notchedOutline': {
              border: 'none'
            },
            '&:hover .MuiOutlinedInput-notchedOutline': {
              border: 'none'
            },
            '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
              border: 'none'
            },
            borderRadius: 5
          }}
        >
          <MenuItem value="">Select a file</MenuItem>
          {/* Add file options */}
        </Select>
      </FormControl>
      <TextField
        multiline
        rows={15}
        placeholder="Generated Code"
        variant="outlined"
        sx={{
          backgroundColor:'#EBF0F8',
          borderRadius: 5,
          '& .MuiOutlinedInput-notchedOutline': {
            border: 'none'
          },
          '&:hover .MuiOutlinedInput-notchedOutline': {
            border: 'none'
          },
          '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
            border: 'none'
          }
        }}
      />
      <Box sx={{ display: 'flex', gap: 1 }}>
        <Button variant="contained" sx={{ borderRadius: 25, flexGrow: 1, backgroundColor:'#EAEAEA', color:"black" }}>
          Apply
        </Button>
        <Button variant="contained" sx={{ borderRadius: 25, flexGrow: 1 , backgroundColor:'#EAEAEA', color:"black"}}>
          Modify
        </Button>
      </Box>

      <Paper
        sx={{
          p: 1,
          display: 'flex',
          flexDirection: 'column',
          gap: 2,
          borderRadius: 5,
          backgroundColor: '#f5f5f5',
        }}
      >
        <Box
          sx={{
            p: 1,
            borderRadius: 5,
            backgroundColor: '#EBF0F8',
            minHeight: 200,
            overflowY: 'auto',
          }}
        >
          {history.map((item, index) => (
            <Typography key={index} variant="body2">
              {item}
            </Typography>
          ))}
        </Box>
        <Paper
          component="form"
          sx={{
            p: '4px 4px',
            display: 'flex',
            alignItems: 'center',
            borderRadius: 5,
            backgroundColor: '#EBF0F8',
            color: 'black',
          }}
          onSubmit={handleCommandSubmit}
        >
          <InputBase
            sx={{ ml: 1, flex: 1 }}
            placeholder="I want to..."
            value={command}
            onChange={handleCommandChange}
          />
          <IconButton type="submit" sx={{ p: '10px' }} aria-label="send">
            <SendIcon />
          </IconButton>
        </Paper>
      </Paper>
    </Box>
  );
};

export default Sidebar;