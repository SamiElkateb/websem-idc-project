import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import Container from '@mui/material/Container';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import Tooltip from '@mui/material/Tooltip';
import MenuItem from '@mui/material/MenuItem';
import AdbIcon from '@mui/icons-material/Adb';
import logo from '/logo.png';
import { Link } from '@mui/material';

const pages = ['Recipe List'];

const Header = () => {
  const [anchorElNav, setAnchorElNav] = React.useState<null | HTMLElement>(null);
  const [anchorElUser, setAnchorElUser] = React.useState<null | HTMLElement>(null);

  const handleOpenNavMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElNav(event.currentTarget);
  };
  const handleOpenUserMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
  };

  return (
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
};
export default Header;
