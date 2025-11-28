import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { getNote } from "../api/notes";
import type { Note } from "../types/note";
import { Typography, Chip, Stack, Button } from "@mui/material";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from "@mui/material";
import { deleteNote } from "../api/notes";

export default function NoteView() {
  const navigate = useNavigate();

  const { id } = useParams();
  const [note, setNote] = useState<Note | null>(null);
  const [loading, setLoading] = useState(true);

  const [open, setOpen] = useState(false);

  useEffect(() => {
    if (!id) return;

    getNote(Number(id))
      .then((data) => setNote(data))
      .finally(() => setLoading(false));
  }, [id]);
  if (!note) return <Typography>Sorry, note not found</Typography>;

  const handleDelete = async () => {
    await deleteNote(note.id);
    navigate("/");
  };

  if (loading) return <Typography>Loading...</Typography>;

  return (
    <>
      <Typography variant="h4" sx={{ mb: 2 }}>
        {note.title}
      </Typography>

      <Typography sx={{ mb: 2 }}>{note.body}</Typography>

      <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
        {note.tags.map((tag) => (
          <Chip key={tag} label={tag} variant="outlined" />
        ))}
      </Stack>

      <Stack direction="row" spacing={2}>
        <Button
          variant="contained"
          component={Link}
          to={`/notes/${note.id}/edit`}
        >
          Edit
        </Button>

        <Button color="error" variant="outlined" onClick={() => setOpen(true)}>
          Delete
        </Button>
      </Stack>

      <Dialog open={open} onClose={() => setOpen(false)}>
        <DialogTitle>Delete note?</DialogTitle>
        <DialogContent>
          <Typography>This action cannot be undone.</Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button color="error" onClick={handleDelete}>
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
