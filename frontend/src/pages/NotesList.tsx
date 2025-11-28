import type { Note } from "../types/note";
import NoteCard from "../components/NoteCard";
import { Container, Typography } from "@mui/material";

function NotesList({ notes, loading }: { notes: Note[]; loading: boolean }) {
  if (loading) {
    return <Typography>Loading notes...</Typography>;
  }
  return (
    <Container sx={{ mt: 4 }}>
      {notes.map((note) => {
        return <NoteCard key={note.id} note={note}></NoteCard>;
      })}
    </Container>
  );
}

export default NotesList;
