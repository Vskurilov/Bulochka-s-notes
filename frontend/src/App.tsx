import NotesList from "./pages/NotesList";
import { useEffect, useState } from "react";
import { getNotes } from "./api/notes";
import type { Note } from "./types/note";
import Header from "./components/Header";
import { Container } from "@mui/material";
import { Route, Routes, useLocation } from "react-router-dom";
import NoteCreate from "./pages/NoteCreate";
import NoteView from "./pages/NoteView";
import NoteEdit from "./pages/NoteEdit";

function App() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [loading, setLoading] = useState(true);

  const location = useLocation();

  useEffect(() => {
    if (location.pathname === "/") {
      getNotes()
        .then((data) => setNotes(data))
        .finally(() => setLoading(false));
    }
  }, [location.pathname]);

  return (
    <>
      <Header />
      <Container sx={{ mt: 4 }}>
        <Routes>
          <Route
            path="/"
            element={<NotesList notes={notes} loading={loading} />}
          ></Route>
          <Route path="/notes/:id" element={<NoteView />} />
          <Route path="/create" element={<NoteCreate />} />
          <Route path="/notes/:id/edit" element={<NoteEdit />} />
        </Routes>
      </Container>
    </>
  );
}

export default App;
