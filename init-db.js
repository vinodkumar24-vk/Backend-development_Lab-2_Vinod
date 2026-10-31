const path = require('path');
const { open } = require('sqlite');
const sqlite3 = require('sqlite3');

const dbPath = path.join(__dirname, 'books.db');

const initialBooks = [
  { id: 1, title: 'Atomic Habits', author: 'James Clear', price: 499, pages: 320 },
  { id: 2, title: 'Deep Work', author: 'Cal Newport', price: 450, pages: 304 },
  { id: 3, title: 'Python Crash Course', author: 'Eric Matthes', price: 850, pages: 544 },
  { id: 4, title: 'Fluent Python', author: 'Luciano Ramalho', price: 1150, pages: 792 },
  { id: 5, title: 'Operating System Concepts', author: 'Peter B. Galvin', price: 990, pages: 976 },
  { id: 6, title: 'Computer Networking: A Top-Down Approach', author: 'James Kurose', price: 1100, pages: 864 },
  { id: 7, title: 'Learning SQL', author: 'Alan Beaulieu', price: 550, pages: 380 },
  { id: 8, title: 'System Design Interview', author: 'Alex Xu', price: 1250, pages: 300 },
  { id: 9, title: 'Structure and Interpretation of Computer Programs', author: 'Harold Abelson', price: 1300, pages: 657 },
  { id: 10, title: 'Automate the Boring Stuff with Python', author: 'Al Sweigart', price: 680, pages: 504 }
];

async function setupDatabase() {
  const db = await open({
    filename: dbPath,
    driver: sqlite3.Database
  });

  console.log('Connected to SQLite database at:', dbPath);

  await db.exec(`
    DROP TABLE IF EXISTS book;
    CREATE TABLE book (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      title TEXT NOT NULL,
      author TEXT NOT NULL,
      price INTEGER NOT NULL,
      pages INTEGER NOT NULL
    );
  `);

  console.log('Created table "book".');

  for (const book of initialBooks) {
    await db.run(
      `INSERT INTO book (id, title, author, price, pages) VALUES (?, ?, ?, ?, ?);`,
      [book.id, book.title, book.author, book.price, book.pages]
    );
  }

  const rows = await db.all('SELECT * FROM book;');
  console.log(`Successfully seeded ${rows.length} books into the database:`);
  console.table(rows);

  await db.close();
  console.log('Database setup complete.');
}

setupDatabase().catch((err) => {
  console.error('Error setting up database:', err);
  process.exit(1);
});

