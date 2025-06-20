# 🤖 AI Commander - WB95

**AI Commander** is a machine learning model designed to play and analyze tactical moves in historical wargames. This repo focuses on using the **Wielkie Bitwy 95 (WB95)** system by Taktyka i Strategia (Rules can be found here: https://gamers-hq.de/media/pdf/91/30/ff/WB_95_English.pdf). It interprets the current game state and suggests the most effective military actions, such as movement, engagement, fortification, or capturing objectives.

## 🎯 Project Goals

- Build a modular AI model for decision-making in hex-based wargames
- Translate detailed battlefield commands into compact, model-friendly tokens
- Train the model on operational patterns such as flanking, holding lines, or concentrating forces
- Deploy the model using Hugging Face for public access or future fine-tuning

## 🧩 Model Architecture Overview

More in [Documentation](docs/docs.md)

The model is composed of the following conceptual components:

1. **Tokenizer**  

Converts structured commands like:
<1_1_17/2/2/2><2371_FOREST><MOVE><1_1_17/2/2/1><2372_CLEAR>

into tokens tensors ready to be passed to further processing.

In future: Convert structured, but natural language-like commands into tokens, e.g.

**1st Company of the 2nd Mechanized Battalion of 17th 'Zoria' Mechanized Brigade, with 2 strength points, 2 remaining movement points, 2 base movement points moves from forest hex 2371 to clear hex 2372 spending 1 movement point.**

2. **Map Context Table**  
Encodes the map's features — hexes rated for mobility, defense, line-of-sight, and terrain types.

That layer would include various matrixes responsible for determining the most valulable points in terms of movement and defence. Using those matrixes will allow further processing.

3. **Operational Pattern Layer**  
Based on best terrain features (defence and manuever) encodes tactical motifs such as flanking, supporting, or pinning the enemy.

4. **Objective Context Table**  
Stores scenario-specific goals such as victory points, control zones, or strategic hexes.

5. **Decision Layer**  
Generates valid and optimal moves based on previous layers and outputs the selected action.

---

## 📦 Repository Structure

```yaml
ai-commander-wb95/
├── tokenizer.py        # Tokenizer that parses WB95-style commands into model-ready tokens
├── tensorizer.py       # Converts token sequences into numerical tensors
├── example_dataset.py  # Generates and prints sample commands and tokenized output
├── vocab.json          # Vocabulary mapping tokens to unique IDs
├── dataset.py          # PyTorch Dataset class for loading training data
├── model/              # Model architecture (planned or in development)
├── data/               # Placeholder for training/validation data
└── README.md
```

---

## 🧪 Example Input

Command (structured form):

<1_1_17/2/2/2><2371_FOREST><MOVE><1_1_17/2/2/1><2372_CLEAR>

Tokenized form:

```python
[
  "COMPANY_1", "BATTALION_1", "BRIGADE_17",
  "STRENGTH_2", "MANUEVER_2", "MOVEMENT_POINTS_2",
  "HEX_START_2371_FOREST", "ACTION_MOVE",
  "COMPANY_1", "BATTALION_1", "BRIGADE_17",
  "STRENGTH_2", "MANUEVER_2", "MOVEMENT_POINTS_1",
  "HEX_END_2372_CLEAR"
]

tensor([1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 9, 10])

## ❓ How To Use

git clone https://github.com/yourname/ai-commander-wb95.git
cd ai-commander-wb95

pip install -r requirements.txt

python example_dataset.py

## 📚 Future Plans
 Expand the tokenizer to support other actions (e.g. ATTACK, SUPPORT, FORTIFY)

 Add map analysis context for terrain and objectives

 Train the model using PyTorch or Hugging Face Transformers

 Create a UI interface or API to test live game states

 Upload trained model to Hugging Face Hub

## 🤝 Contributions
Contributions, ideas, and scenario-specific datasets are welcome!
Feel free to open an issue or submit a pull request.

## 🧠 Author
AI Commander is developed by Dariusz Janicki - enthusiast of historical strategy games and AI systems.
Wargaming meets deep learning — one hex at a time.

