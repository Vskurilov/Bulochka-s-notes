import { Link } from "react-router-dom";
import type { Note } from "../types/note";
import {
  Card,
  CardContent,
  Typography,
  Chip,
  Stack,
  Button,
} from "@mui/material";

function NoteCard({ note }: { note: Note }) {
  return (
    <Card sx={{ mb: 2 }}>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          {note.title}
        </Typography>

        <Typography variant="body1" sx={{ mb: 1 }}>
          {note.body}
        </Typography>

        <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
          {note.tags.map((tag) => (
            <Chip key={tag} label={tag} variant="outlined" />
          ))}
        </Stack>

        <Button
          variant="contained"
          color="primary"
          component={Link}
          to={`/notes/${note.id}`}
        >
          Открыть
        </Button>
      </CardContent>
    </Card>
  );
}

export default NoteCard;
