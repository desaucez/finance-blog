// src/db/database.ts
import * as SQLite from 'expo-sqlite';

export const db = SQLite.openDatabase('vulkrx.db');

export const initDB = () => {
  db.transaction(tx => {
    tx.executeSql(
      `CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER PRIMARY KEY NOT NULL,
        name TEXT NOT NULL,
        sets INTEGER,
        reps INTEGER,
        weight REAL
      );`
    );
  });
};
