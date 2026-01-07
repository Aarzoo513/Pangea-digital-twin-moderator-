#!/bin/bash
# Migration script for Settings Tab feature

echo "🔧 Running database migrations for Settings Tab..."
echo ""

# Navigate to project directory
cd "$(dirname "$0")"

# Create migrations
echo "📝 Creating migrations..."
python manage.py makemigrations chat_moderator

# Apply migrations
echo "✅ Applying migrations..."
python manage.py migrate

echo ""
echo "✨ Migrations complete! You can now use the Settings tab."
echo "🚀 Restart your Django server if it's running."
