# Alembic Database Migrations Guide

## Quick Start

### 1. Apply Initial Migration

```bash
alembic upgrade head
```

This creates the `users` table with all necessary columns and indexes.

### 2. Verify Migration Applied

```bash
alembic current
alembic history
```

---

## Migration Commands

### Create a New Migration

After modifying `app/models.py`, generate a migration:

```bash
alembic revision --autogenerate -m "Description of changes"
```

Example:

```bash
alembic revision --autogenerate -m "Add profile table"
```

This creates a new file in `alembic/versions/` with upgrade/downgrade functions.

### Apply Migrations

```bash
# Apply all pending migrations
alembic upgrade head

# Apply specific number of migrations
alembic upgrade +2

# Upgrade to specific revision
alembic upgrade <revision_id>
```

### Rollback Migrations

```bash
# Rollback one migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision_id>

# Rollback all
alembic downgrade base
```

### View Migration History

```bash
# Show migration history
alembic history

# Show current applied version
alembic current

# Show detailed information
alembic history --verbose
```

---

## Workflow

1. **Modify your model** in `app/models.py`
2. **Generate migration**: `alembic revision --autogenerate -m "message"`
3. **Review the generated file** in `alembic/versions/`
4. **Apply migration**: `alembic upgrade head`
5. **Commit** the migration file to version control

---

## Initial Migration Already Set Up

✅ Initial migration created: `001_initial_migration.py`
✅ Creates `users` table with:

- id (primary key)
- username (unique)
- email (unique)
- hashed_password
- is_active (default: true)
- created_at (auto-timestamp)
- updated_at (auto-timestamp)

---

## First Run (Development)

```bash
# 1. Make sure PostgreSQL is running with database created
# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply migrations
alembic upgrade head

# 4. Start the application
python main.py
```

---

## Production Best Practices

- Always review generated migrations before applying
- Test migrations on development database first
- Commit migration files to version control
- Use `alembic downgrade` for rollback if needed
- Never manually modify migration files in production
