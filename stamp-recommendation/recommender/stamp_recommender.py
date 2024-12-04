import pandas as pd
from typing import List, Set
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

class StampRecommender:
    def __init__(self, df: pd.DataFrame, preprocess: bool = False):
        """
        Initialize the recommender with a DataFrame containing stamp data.
        
        Args:
            df (pd.DataFrame): DataFrame with columns ['name', 'release_date', 'denomination', 
                             'quantity', 'tokenized_name']
            preprocess (bool): Whether to preprocess the data or assume it's already processed
        """
        self.df = df
        self.display_columns = ['name', 'release_date', 'denomination', 'quantity']
        
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        if preprocess:
            self._preprocess_data()

    def preprocess_text(self, text: str) -> List[str]:
        """
        Preprocess text by tokenizing, removing stop words, and lemmatizing.
        
        Args:
            text (str): Input text to preprocess
            
        Returns:
            List[str]: List of preprocessed tokens
        """

        text = str(text).lower()
        
        # Tokenize
        tokens = word_tokenize(text)
        print(f"Original tokens: {tokens}")
        
        # Remove stop words and punctuation, then lemmatize
        processed_tokens = []
        for token in tokens:
            if token.isalnum() and token not in self.stop_words:
                lemmatized = self.lemmatizer.lemmatize(token)
                processed_tokens.append(lemmatized)
        
        print(f"Processed tokens: {processed_tokens}")
        return processed_tokens

    def _preprocess_data(self):
        """Preprocess the DataFrame and save it to CSV."""
        # Create tokenized_name column
        self.df['tokenized_name'] = self.df['name'].apply(self.preprocess_text)
        
        # Remove unnecessary columns
        columns_to_remove = ["sl_no", "printer", "fdc_images", "brochure_pdf"]
        self.df = self.df.drop(columns=[col for col in columns_to_remove if col in self.df.columns])
        
        # Save preprocessed data
        self.df.to_csv('preprocessed_stamps_data.csv', index=False)
        print("Preprocessed data saved to 'preprocessed_stamps_data.csv'")

    def get_available_stamps(self) -> List[str]:
        return self.df['name'].tolist()

    def get_recommendations(self, stamp_name: str, min_relevance: float = None) -> pd.DataFrame:
        """
        Get all stamps that contain any of the tokens from the input stamp name.
        
        Args:
            stamp_name (str): Name of the stamp to get recommendations for
            min_relevance (float): Ignored parameter (kept for backwards compatibility)
            
        Returns:
            pd.DataFrame: Matching stamps
        """

        if 'tokenized_name' not in self.df.columns:
            print("Creating tokenized_name column...")
            self.df['tokenized_name'] = self.df['name'].apply(self.preprocess_text)
        
        # Tokenize the input stamp name
        input_tokens = set(token.lower() for token in self.preprocess_text(stamp_name))
        print(f"\nSearching for stamps containing any of these tokens: {input_tokens}\n")
        
        # Find all stamps that contain any of the input tokens
        matching_stamps = self.df[
            self.df['tokenized_name'].apply(
                lambda x: bool(set(map(str.lower, x)) & input_tokens)
            )
        ]
        
        # Remove exact matches
        matching_stamps = matching_stamps[
            matching_stamps['name'].str.lower() != stamp_name.lower()
        ]
        
        print(f"\nFound {len(matching_stamps)} matching stamps")
        
        return matching_stamps[self.display_columns] 