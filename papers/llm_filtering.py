from openai import OpenAI

from papers import config


def is_relevant(title, keywords=None, model="gpt-3.5-turbo", api_key=None):
    
    client = OpenAI(api_key=api_key)

    if keywords:
        message = f"Title of the publication: '{title}'\nKeywords: {', '.join(keywords)}"
    else:
        message = f"Title of the publication: '{title}'"

    with open(config.LOCAL_FILTERING_PROMPT_PATH, "r") as f:
        prompt = f.read()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": message}
        ]
    )

    return "yes" in response.choices[0].message.content.lower()


class LLMFilter:
    def __init__(self, df):
        """
        Initialize the ArticleFilter class with a DataFrame.

        Args:
            df (pd.DataFrame): DataFrame containing articles with their details.
        """
        self.df = df

    def filter_articles(self):
        """
        Interactively asks the user to decide whether to retain each article in the DataFrame.

        Returns:
            pd.DataFrame: A filtered DataFrame containing only the articles retained by the user.
        """
        retained_indices = []

        for index, article in self.df.iterrows():
            if is_relevant(title=article['Title'], keywords=article['Keywords'], api_key=config.OPENAI_API_KEY):
                retained_indices.append(index)

        # Filter the DataFrame to only include retained articles
        return self.df.loc[retained_indices]
