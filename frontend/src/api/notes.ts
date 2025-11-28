import type { NoteCreate, NoteUpdate } from "../types/note";

const API = "http://localhost:8000";

export async function getNotes() {
  return fetch(`${API}/notes`).then((r) => {
    return r.json();
  });
}

export async function createNote(data: NoteCreate) {
  const res = await fetch(`${API}/notes`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  return res.json();
}

export async function getNote(id: number) {
  return fetch(`${API}/notes/${id}`).then((r) => r.json());
}

export async function updateNote(id: number, data: NoteUpdate) {
  return fetch(`${API}/notes/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  }).then((r) => r.json());
}

export async function deleteNote(id: number) {
  return fetch(`${API}/notes/${id}`, {
    method: "DELETE",
  });
}
