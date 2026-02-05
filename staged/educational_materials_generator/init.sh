#!/bin/bash
# Quick initialization script for Educational Materials Generator

set -e

PROJECT_DIR="/Users/b.saab/repos/crewai_bsaab/staged/educational_materials_generator"

echo "🚀 Initializing Educational Materials Generator..."
echo ""

# Step 1: Navigate to project
cd "$PROJECT_DIR"
echo "✓ Changed to project directory"

# Step 2: Create .env file
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Created .env from template"
else
    echo "⚠ .env already exists, skipping"
fi

# Step 3: Create additional directories
mkdir -p output/{stage_1_discovery,stage_2_curriculum,stage_3_content,stage_4_assessment,stage_5_qa}
echo "✓ Created output directories"

# Step 4: Check Python version
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $PYTHON_VERSION"

# Step 5: Install dependencies (if pip available)
if command -v pip &> /dev/null; then
    echo ""
    echo "📦 Installing dependencies..."
    pip install crewai pydantic python-dotenv requests litellm --quiet
    echo "✓ Dependencies installed"
fi

# Step 6: Check Ollama
if command -v ollama &> /dev/null; then
    echo "✓ Ollama found"
    echo ""
    echo "📥 To pull required models, run:"
    echo "   ollama pull llama2:13b-chat"
    echo "   ollama pull mistral:7b-instruct"
else
    echo "⚠ Ollama not found. Install from: https://ollama.ai"
fi

echo ""
echo "✅ Initialization complete!"
echo ""
echo "📚 Next steps:"
echo "1. Edit .env with your configuration"
echo "2. Pull Ollama models if not already done"
echo "3. Start Ollama: ollama serve"
echo "4. Review SETUP_COMPLETE.md for implementation roadmap"
echo ""
