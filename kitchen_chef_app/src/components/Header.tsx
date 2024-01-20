import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Button from '@mui/material/Button';
import logo from '/logo.png';
import { Link } from '@mui/material';
import React from 'react';

const pages = ['Recipe List'];

const Header:React.FC = () => (
  <AppBar position="static" color="transparent" elevation={0} sx={{ marginBottom: '2rem' }}>
    <Container maxWidth="md">
      <Box display="flex" sx={{ justifyContent: 'space-between', alignItems: 'center' }}>
        <Box>
          <Link href="/">
            <img
              srcSet={logo}
              src={logo}
              alt="logo"
              loading="lazy"
              height="100px"
            />
          </Link>
        </Box>
        <Box>
          {pages.map((page) => (
            <Button
              key={page}
              LinkComponent={Link}
              href="/"
              sx={{
                my: 2, color: 'black', display: 'block', fontSize: '1.2rem',
              }}
            >
              {page}
            </Button>
          ))}
        </Box>
      </Box>
    </Container>

  </AppBar>
);
export default Header;
