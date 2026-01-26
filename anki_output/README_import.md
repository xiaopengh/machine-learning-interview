# Anki Import Instructions

## Files Generated

- `anki_basic_cards.txt` - Standard Q&A flashcards
- `anki_cloze_cards.txt` - Cloze deletion flashcards
- `anki_images/` - Downloaded images for cards

## How to Import

### Step 1: Copy Images to Anki Media Folder

Copy all files from `anki_images/` to your Anki media folder:
- **Windows**: `%APPDATA%\Anki2\<profile>\collection.media`
- **Mac**: `~/Library/Application Support/Anki2/<profile>/collection.media`
- **Linux**: `~/.local/share/Anki2/<profile>/collection.media`

### Step 2: Import Basic Cards

1. Open Anki
2. File → Import
3. Select `anki_basic_cards.txt`
4. Set:
   - Type: Basic
   - Deck: (create new or select existing)
   - Fields separated by: Tab
   - Field 1: Front
   - Field 2: Back
   - Field 3: Tags
5. Click Import

### Step 3: Import Cloze Cards

1. File → Import
2. Select `anki_cloze_cards.txt`
3. Set:
   - Type: Cloze
   - Fields separated by: Tab
   - Field 1: Text
   - Field 2: Tags
4. Click Import

## Tag Structure

Cards are tagged with the format: `Category::Subcategory`

Categories:
- ML (Machine Learning)
- DL (Deep Learning)
- Math (Mathematics)
- Tools (Spark, XGBoost, TensorFlow)
- RecSys (Recommender Systems)

Subcategories include:
- BasicConcepts, FeatureEngineering
- KNN, SVM, NaiveBayes, LinearRegression, LogisticRegression
- FM, DecisionTree, RandomForest, GBDT, KMeans, PCA
- DNN, CNN, RNN
- Spark, XGBoost, TensorFlow
- Probability, Optimization

## Customization

### Adding More Translations

Edit `term_translations.py` to add more Chinese-English term pairs.

### Regenerating Cards

Run `python convert_to_anki.py` to regenerate all cards.

## Notes

- Cards include English translations for key ML terms in parentheses
- LaTeX math is converted to `<anki-mathjax>` tags for native Anki rendering (no extra setup needed)
- Images are downloaded locally for offline use
- Zhihu equation images are automatically converted to LaTeX
- Cloze cards are generated for definitions, lists, and key formulas
