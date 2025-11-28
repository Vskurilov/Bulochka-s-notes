export interface Note {
  id: number;
  title: string;
  body: string;
  tags: string[];
}

export type NoteCreate = Omit<Note, "id">;

export type NoteUpdate = Partial<NoteCreate>;
