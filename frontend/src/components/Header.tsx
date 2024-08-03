import React from 'react';
import {
  AppBar,
  Box,
  Toolbar,
  Typography,
  InputBase,
  IconButton,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';

const Header: React.FC = () => {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static" sx={{ backgroundColor: 'white', boxShadow: 'none' }}>
        <Toolbar>
          <Typography variant="h6" component="div" className="TradeSweep" sx={{ flexGrow: 0 }}>
            TradeSweep
          </Typography>

          <Box sx={{ flexGrow: 1 }} />

          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              backgroundColor: '#EBF0F8', // Set to white to blend with AppBar
              borderRadius: '25px',
              padding: '4px 8px',
              width: 700,
              '& .MuiInputBase-root': { // Targeting the input base root for consistent styling
                color: 'black', // Change the color to black for visibility
                flexGrow: 1,
              },
              '& .MuiIconButton-root': { // Targeting the IconButton root
                color: 'black', // Ensuring the icon button is visible
              },
            }}
          >
            <InputBase
              placeholder="Search CSV..."
              sx={{
                color: 'inherit', // Inherits color from parent which is black
                marginLeft: 1,
                flexGrow: 1,
              }}
            />
            <IconButton sx={{ color: 'inherit' }}>
              <SearchIcon />
            </IconButton>
          </Box>

          <Box sx={{ flexGrow: 1 }} />
          <Box
            sx={{
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              backgroundColor: '#D9D9D9',
              color: 'black',
              borderRadius: '50%', // Makes the Box circular
              width: 40, // Width of the circle
              height: 40, // Height of the circle, should be the same as width for a perfect circle
            }}
          >
            <Typography
              variant="body1"
              sx={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                width: '100%', // Ensures the text is centered
                height: '100%', // Ensures the text is vertically centered
              }}
            >
              TS
            </Typography>
          </Box>
        </Toolbar>
      </AppBar>
    </Box>
  );
};

export default Header;
