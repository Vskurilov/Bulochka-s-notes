import { AppBar, Button, Stack, Toolbar, Typography } from "@mui/material";
import { Link } from "react-router-dom";

function Header() {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography
          variant="h6"
          sx={{ flexGrow: 1, textDecoration: "none" }}
          component={Link}
          to="/"
          color="inherit"
        >
          Bulocka Notes
        </Typography>

        <Stack direction="row" spacing={2}>
          <Button color="inherit" component={Link} to="/create">
            Create note
          </Button>
        </Stack>
      </Toolbar>
    </AppBar>
  );
}

export default Header;
