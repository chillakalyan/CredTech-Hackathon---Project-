#!/bin/bash
# ================================
# CredTech Hackathon Run Script
# ================================

echo "🚀 Starting CredTech Hackathon Project..."

# Step 1: Create virtual environment (optional)
if [ ! -d "venv" ]; then
  echo "📦 Creating virtual environment..."
  python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Step 2: Install requirements
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 3: Run data pipeline (fetch APIs & save CSVs)
echo "📊 Running data pipeline..."
python src/pipeline.py

# Step 4: Launch Streamlit dashboard
echo "🖥️ Launching Streamlit dashboard..."
streamlit run src/app.py

