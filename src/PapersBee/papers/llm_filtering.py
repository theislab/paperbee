from typing import List, Optional

import pandas as pd
from openai import OpenAI
from papers import config


def is_relevant(
    client: OpenAI,
    filtering_prompt: str,
    title: str,
    keywords: Optional[List[str]] = None,
    model: str = "gpt-3.5-turbo",
) -> bool:
    """
    Determines if a publication is relevant based on its title and optional keywords using an LLM (Language Model).

    Args:
        client (OpenAI): The OpenAI client used to interact with the API.
        filtering_prompt (str): The prompt used to instruct the LLM on relevance filtering.
        title (str): The title of the publication.
        keywords (Optional[List[str]]): A list of keywords associated with the publication. Defaults to None.
        model (str): The model to use for the API call. Defaults to "gpt-3.5-turbo".

    Returns:
        bool: True if the publication is deemed relevant, otherwise False.
    """
    if keywords:
        message = f"Title of the publication: '{title}'\nKeywords: {', '.join(keywords)}"
    else:
        message = f"Title of the publication: '{title}'"

    response = client.chat.completions.create(
        model=model, messages=[{"role": "system", "content": filtering_prompt}, {"role": "user", "content": message}]
    )
    content = response.choices[0].message.content
    if content is not None:
        return "yes" in content.lower()
    else:
        return False


class LLMFilter:
    """
    A class to filter articles using an LLM (Language Model) based on titles and optional keywords.

    Args:
        df (pd.DataFrame): DataFrame containing the articles to be filtered.
        client (OpenAI): An instance of OpenAI client for making API calls.
        model (str): The model to use for filtering. Defaults to "gpt-3.5-turbo".
        filtering_prompt (str): The prompt content for filtering the articles.
    """

    def __init__(self, df: pd.DataFrame, model: str = "gpt-3.5-turbo") -> None:
        """
        Initializes the LLMFilter with a DataFrame of articles and an LLM model.

        Args:
            df (pd.DataFrame): The DataFrame containing articles with their details.
            model (str): The model to use for filtering. Defaults to "gpt-3.5-turbo".
        """
        self.df: pd.DataFrame = df
        self.client: OpenAI = OpenAI(api_key=config.OPENAI_API_KEY)
        self.model: str = model

        with open(config.LOCAL_FILTERING_PROMPT_PATH) as f:
            self.filtering_prompt: str = f.read()

    def filter_articles(self) -> pd.DataFrame:
        """
        Filters the articles in the DataFrame by determining their relevance using the LLM.

        Returns:
            pd.DataFrame: A filtered DataFrame containing only the articles deemed relevant by the LLM.
        """
        retained_indices: List[int] = []

        for index, article in self.df.iterrows():
            if is_relevant(
                client=self.client,
                filtering_prompt=self.filtering_prompt,
                title=article["Title"],
                keywords=article.get("Keywords"),
                model=self.model,
            ):
                retained_indices.append(index)

        # Return a DataFrame containing only the retained articles
        return self.df.loc[retained_indices]
