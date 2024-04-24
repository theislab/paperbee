from openai import OpenAI

from papers import config


def is_relevant(client, filtering_prompt, title, keywords=None, model="gpt-3.5-turbo"):
    if keywords:
        message = f"Title of the publication: '{title}'\nKeywords: {', '.join(keywords)}"
    else:
        message = f"Title of the publication: '{title}'"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": filtering_prompt},
            {"role": "user", "content": message}
        ]
    )

    return "yes" in response.choices[0].message.content.lower()


class LLMFilter:
    def __init__(self, df, model="gpt-3.5-turbo"):
        """
        Initialize the ArticleFilter class with a DataFrame.

        Args:
            df (pd.DataFrame): DataFrame containing articles with their details.
        """
        self.df = df
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.model = model
        with open(config.LOCAL_FILTERING_PROMPT_PATH, "r") as f:
            self.filtering_prompt = f.read()

    def filter_articles(self):
        """
        Interactively asks the user to decide whether to retain each article in the DataFrame.

        Returns:
            pd.DataFrame: A filtered DataFrame containing only the articles retained by the user.
        """
        retained_indices = []

        for index, article in self.df.iterrows():
            if is_relevant(client=self.client, filtering_prompt=self.filtering_prompt,
                           title=article['Title'], keywords=article['Keywords']):
                retained_indices.append(index)

        # Filter the DataFrame to only include retained articles
        return self.df.loc[retained_indices]
