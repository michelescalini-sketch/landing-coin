CREATE TABLE landers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  wallet TEXT NOT NULL UNIQUE,
  signature TEXT NOT NULL UNIQUE,
  received_raw TEXT NOT NULL,
  balance_raw TEXT NOT NULL,
  confirmed_slot INTEGER NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX landers_created_at_idx ON landers(created_at);
