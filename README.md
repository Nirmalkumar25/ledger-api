# Ledger Report Search API

## Project Overview

This **FastAPI** project implements a secure, high-performance, **search-only API** for viewing ledger entries.

### Key Features

- **Advanced filtering** via query parameters  
- **Entity-level data and column isolation**  
- **Basic rate limiting** (100 requests/hour per IP) — implemented *without* third-party packages

---

## Tech Stack

| Layer       | Technology     |
|-------------|----------------|
| Language    | Python 3.13.5  |
| Web Framework | FastAPI     |
| ORM         | SQLAlchemy     |
| Database    | PostgreSQL     |

---

## Getting Started

Follow these simple steps to run the project locally:

### 1. Clone the Repo

```bash
git clone https://github.com/Nirmalkumar25/ledger-api.git
cd ledger-api
```

### 2. Set Up a Virtual Environment

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
```

### 3. Install the Required Packages

```bash
pip install fastapi uvicorn sqlalchemy psycopg2
```
### 4. PostgreSQL Database Setup

Ensure you have a PostgreSQL database running. Create a database named `ledger_db` (or any name of your choice).

### 5. Add Your PostgreSQL Database URL

Edit the `config.py` file and add your database connection string:

```python
DATABASE_URL = "postgresql://<username>:<password>@<host>:<port>/<database_name>"
```

**Example:**

```python
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/ledger_db"
```
### 6. Start the Server

```bash
uvicorn main:app --reload
```

Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to explore the Swagger docs.

---

## Project Structure

```
ledger-api/
├── main.py           # Main entry point (routes & logic)
├── models.py         # Database models
├── database.py       # DB connection setup
├── rate_limiter.py   # Handles IP-based rate limiting
├── utils.py          # Column visibility helper functions
├── config.py         # Configuration values
└── README.md         # Project setup & usage guide
```

---

## Sample SQL Data

### Create Tables (If not created)

```sql
CREATE TABLE ledger_entries (
  id INTEGER PRIMARY KEY,
  entity_id INTEGER,
  loan_no TEXT,
  disbursement_date DATE,
  customer_id TEXT,
  name TEXT,
  address TEXT,
  mobile_number TEXT,
  particulars TEXT,
  amount REAL
);

CREATE TABLE column_visibility (
  id SERIAL PRIMARY KEY,
  entity_id INTEGER,
  column_name TEXT
);
```

### Insert Sample Entries

```sql
INSERT INTO ledger_entries VALUES
(1, 1, 'MTY-A10000', '2025-06-24', 'C-00009', 'Nirmal', 'mayiladu', 'Gold Chains, Gold Bangles', 25000, '9876543210'),
(2, 2, 'MTY-C10001', '2025-07-05', 'C-00010', 'Divya', 'Thanjavur', 'Gold Necklace', 30000, '9123456780'),
(3, 3, 'MTY-C10002', '2025-07-06', 'C-00011', 'Priya', 'Trichy', 'Silver Anklets', 10000, '8987654321');

INSERT INTO column_visibility VALUES
(1,1, 'loan_no'), (2,1, 'disbursement_date'), (3,1, 'customer_id'),
(4,1, 'name'), (5,1, 'address'), (6,1, 'particulars'), (7,1, 'mobile_number'),
(8,2, 'loan_no'), (9,2, 'customer_id'), (10,2, 'name'), (11,2, 'particulars'),
(12,3, 'loan_no'), (13,3, 'name'), (14,3, 'particulars');
```

---

## Try a Sample API Call

```http
GET /search?entity_id=1&name=nirmal&area=mayiladu
```

The response will include only the columns allowed for `entity_id=1`.

---

## Built-in Rate Limiting

To prevent misuse:

- Limit: 100 requests/hour per IP
- Exceeding the limit? You’ll see:

```json
{
  "detail": "Rate limit exceeded"
}
```
