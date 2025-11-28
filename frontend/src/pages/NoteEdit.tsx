import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { getNote, updateNote } from "../api/notes";
import type { Note } from "../types/note";
import { TextField, Button, Stack, Typography, Box } from "@mui/material";

export default function NoteEdit() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [note, setNote] = useState<Note | null>(null);
  const [loading, setLoading] = useState(true);

  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");
  const [tags, setTags] = useState("");

  useEffect(() => {
    if (!id) return;

    getNote(Number(id))
      .then((data: Note) => {
        setNote(data);
        setTitle(data.title);
        setBody(data.body);
        setTags(data.tags.join(", "));
      })
      .finally(() => setLoading(false));
  }, [id]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    await updateNote(Number(id), {
      title,
      body,
      tags: tags
        .split(",")
        .map((t) => t.trim())
        .filter(Boolean),
    });

    navigate(`/notes/${id}`);
  }

  if (loading) return <Typography>Loading...</Typography>;
  if (!note) return <Typography>Sorry, note not found</Typography>;

  return (
    <Box sx={{ maxWidth: 600, mx: "auto", mt: 4 }}>
      <Typography variant="h4" sx={{ mb: 2 }}>
        Create Note
      </Typography>

      <form onSubmit={handleSubmit}>
        <Stack spacing={2}>
          <TextField
            label="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            fullWidth
            required
          />

          <TextField
            label="Body"
            value={body}
            onChange={(e) => setBody(e.target.value)}
            multiline
            rows={4}
            required
          />

          <TextField
            label="Tags (',')"
            value={tags}
            onChange={(e) => setTags(e.target.value)}
            fullWidth
          />

          <Button
            type="submit"
            variant="contained"
            size="large"
            disabled={loading}
          >
            {loading ? "Saving..." : "Save"}
          </Button>
        </Stack>
      </form>
    </Box>
  );
}
