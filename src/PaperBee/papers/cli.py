from typing import List

import pandas as pd


class InteractiveCLIFilter:
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the ArticleFilter class with a DataFrame.

        Args:
            df (pd.DataFrame): DataFrame containing articles with their details.
        """
        self.df: pd.DataFrame = df

    def filter_articles(self) -> pd.DataFrame:
        """
        Interactively asks the user to decide whether to retain each article in the DataFrame.

        Returns:
            pd.DataFrame: A filtered DataFrame containing only the articles retained by the user.
        """
        retained_indices: List[int] = []

        for index, row in self.df.iterrows():
            if self.display_article(row):
                retained_indices.append(index)

        # Filter the DataFrame to only include retained articles
        return self.df.loc[retained_indices]

    def display_article(self, row: pd.Series) -> bool:
        """
        Display the details of a single article and prompt for user input.

        Args:
            row (pd.Series): A Series containing the details of an article.

        Returns:
            bool: True if the user chooses to retain the article, False otherwise.
        """
        print("\nArticle Details:")
        print(f"Title: {row['Title']}")
        print(f"Posted Date: {row['PostedDate']}")
        print(f"Keywords: {row['Keywords']}")
        print(f"Preprint: {row.get('IsPreprint', 'Not available')}")

        # Prompt the user to retain the article or not
        user_input: str = input("Retain this article? (y/n): ").strip().lower()
        while user_input not in ["y", "n"]:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")
            user_input = input("Retain this article? (y/n): ").strip().lower()

        return user_input == "y"
