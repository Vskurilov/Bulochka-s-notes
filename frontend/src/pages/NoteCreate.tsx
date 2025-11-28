import React, { useState } from "react";
import { TextField, Button, Stack, Typography, Box } from "@mui/material";
import { createNote } from "../api/notes";
import { useNavigate } from "react-router-dom";
import type { Note } from "../types/note";

export default function NoteCreate() {
  const navigate = useNavigate();

  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");
  const [tags, setTags] = useState("");

  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);

    const newNote = {
      title,
      body,
      tags: tags
        .split(",")
        .map((t) => t.trim())
        .filter(Boolean),
    };

    const created: Note = await createNote(newNote);
    navigate(`/notes/${created.id}`);
  }

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
            {loading ? "Creating..." : "Create"}
          </Button>
        </Stack>
      </form>
    </Box>
  );
}
