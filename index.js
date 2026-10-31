const express = require('express');
const path = require('path');

let sqlite = null;
let sqlite3 = null;
try {
  sqlite = require('sqlite');
  sqlite3 = require('sqlite3');
} catch (e) {
  // Serverless fallback if native C++ bindings cannot load
}

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 3000;
const dbPath = path.join(__dirname, 'books.db');

let db = null;

// Initial book seed for in-memory fallback (used if native sqlite3 binary is restricted on serverless platforms)
let inMemoryBooks = [
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

// Task 3: Initialize SQLite DB and Start Server
const initializeDBAndServer = async () => {
  try {
    if (sqlite && sqlite3) {
      db = await sqlite.open({
        filename: dbPath,
        driver: sqlite3.Database
      });
      console.log('Connected to SQLite database successfully');
    }
    app.listen(PORT, () => {
      console.log(`Server Running at http://localhost:${PORT}/`);
    });
  } catch (error) {
    console.log(`DB Error: ${error.message}`);
    if (!process.env.VERCEL) {
      process.exit(1);
    }
  }
};

initializeDBAndServer();

// Root route
app.get('/', (request, response) => {
  response.send('Books Database CRUD API (Lab 2) - Vinod Kumar');
});

// Task 4 & 5: GET /books/ - Get all books
app.get(['/books', '/books/'], async (request, response) => {
  if (db) {
    const getBooksQuery = `
      SELECT
        *
      FROM
        book
      ORDER BY
        id ASC;
    `;
    const booksList = await db.all(getBooksQuery);
    return response.send(booksList);
  }
  response.send(inMemoryBooks);
});

// Task 4 & 5: GET /books/:bookId/ - Get single book by ID
app.get(['/books/:bookId', '/books/:bookId/'], async (request, response) => {
  const { bookId } = request.params;
  if (db) {
    const getBookQuery = `
      SELECT
        *
      FROM
        book
      WHERE
        id = ?;
    `;
    const book = await db.get(getBookQuery, [bookId]);
    if (book === undefined) {
      return response.status(404).send('Requested Book Not Found');
    }
    return response.send(book);
  }

  const book = inMemoryBooks.find((b) => b.id === parseInt(bookId));
  if (!book) {
    return response.status(404).send('Requested Book Not Found');
  }
  response.send(book);
});

// Task 4 & 5: POST /books/ - Add a new book
app.post(['/books', '/books/'], async (request, response) => {
  const bookData = request.body;
  const { title, author, price, pages } = bookData;

  if (db) {
    const insertBookQuery = `
      INSERT INTO
        book (title, author, price, pages)
      VALUES
        (?, ?, ?, ?);
    `;
    const dbResult = await db.run(insertBookQuery, [title, author, price, pages]);
    const bookId = dbResult.lastID;
    return response.status(201).send({ newBookId: bookId, message: 'New Book Added Successfully' });
  }

  const newId = inMemoryBooks.length > 0 ? Math.max(...inMemoryBooks.map((b) => b.id)) + 1 : 1;
  const newBook = { id: newId, title, author, price: parseInt(price), pages: parseInt(pages) };
  inMemoryBooks.push(newBook);
  response.status(201).send({ newBookId: newId, message: 'New Book Added Successfully' });
});

// Task 4 & 5: PUT /books/:bookId/ - Update an existing book
app.put(['/books/:bookId', '/books/:bookId/'], async (request, response) => {
  const { bookId } = request.params;
  const bookData = request.body;
  const { title, author, price, pages } = bookData;

  if (db) {
    const updateBookQuery = `
      UPDATE
        book
      SET
        title = ?,
        author = ?,
        price = ?,
        pages = ?
      WHERE
        id = ?;
    `;
    await db.run(updateBookQuery, [title, author, price, pages, bookId]);
    return response.send('Book Record Updated Successfully');
  }

  const index = inMemoryBooks.findIndex((b) => b.id === parseInt(bookId));
  if (index !== -1) {
    inMemoryBooks[index] = {
      ...inMemoryBooks[index],
      title: title || inMemoryBooks[index].title,
      author: author || inMemoryBooks[index].author,
      price: price ? parseInt(price) : inMemoryBooks[index].price,
      pages: pages ? parseInt(pages) : inMemoryBooks[index].pages
    };
    return response.send('Book Record Updated Successfully');
  }
  response.status(404).send('Requested Book Not Found');
});

// Task 4 & 5: DELETE /books/:bookId/ - Remove a book
app.delete(['/books/:bookId', '/books/:bookId/'], async (request, response) => {
  const { bookId } = request.params;

  if (db) {
    const deleteBookQuery = `
      DELETE FROM
        book
      WHERE
        id = ?;
    `;
    await db.run(deleteBookQuery, [bookId]);
    return response.send('Book Record Removed Successfully');
  }

  inMemoryBooks = inMemoryBooks.filter((b) => b.id !== parseInt(bookId));
  response.send('Book Record Removed Successfully');
});

module.exports = app;

