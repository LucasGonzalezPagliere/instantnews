import openai
import requests

# Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
openai.api_key = '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'
model_engine = "gpt-3.5-turbo"

def truncate_words(text, num_words):
    words = text.split()
    
    if len(words) > num_words:
        return " ".join(words[:num_words])
    else:
        return text
    
def truncate_content_to_fit(title, content, conversation_length, max_tokens=4096):
    tokens_per_word = 1.5  # Adjust this according to your needs
    words_allowed = int((max_tokens - conversation_length) / tokens_per_word)
    
    content_combined = f"{title} {content}"
    truncated_content = truncate_words(content, words_allowed - len(title.split()) - 1)  # -1 for the extra space
    
    tokens_combined = int(len(content_combined.split()) * tokens_per_word)
    
    if tokens_combined > max_tokens - conversation_length:
        return f"{title} {truncated_content}"
    else:
        return content_combined


def process_news_items(news_items):
    summaries = summarize_articles(news_items)
    top_three = select_top_three(summaries)
    formatted_items = format_items(top_three)

    return formatted_items

def summarize_articles(news_items):
    summaries = []

    for item in news_items:
        content = truncate_content_to_fit(item['title'], str(item['content']), conversation_length=1000) # Adjust conversation_length based on the token count of the conversation excluding the content
        summary = call_gpt4_api(content)
        summaries.append(summary)
    print("done summarizing articles")
    return summaries

def call_gpt4_api(content):
    print("Summarizing article: " + content)
    conversation = [
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes news articles. The summaries should be at least 5 sentences, but can be longer if more is needed."
            },
            {
                "role": "user",
                "content": f"Please summarize this article in at least 5 sentences: {content}"
            }
        ]
        
    response = openai.ChatCompletion.create(
            model=model_engine,
            messages=conversation,
            max_tokens=700,
            n=1,
            temperature=0.5
        )

    summary = response.choices[0].message["content"]
    print("Article summarized " + summary)
    return summary.strip()

def select_top_three(summaries):
    joined_summaries = ' ||| '.join(summaries)
    
    conversation = [
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes and picks the most important news articles."
            },
            {
                "role": "user",
                "content": f"Out of these summaries, select the three most important by providing their index numbers (starting from 1), separated by commas. Summaries: {joined_summaries}"
            }
        ]
        
    response = openai.ChatCompletion.create(
            model=model_engine,
            messages=conversation,
            max_tokens=500,
            n=1,
            temperature=0.5
        )

    selected_indices = response.choices[0].message["content"].strip().split(', ')
    selected_indices = [int(index) - 1 for index in selected_indices]  # Convert to zero-based index
    selected_summaries = [summaries[index] for index in selected_indices]

    print("selected: " + str(selected_summaries))
    print(len(selected_summaries))
    return selected_summaries

def format_items(top_three):
    formatted_items = []

    for summary in top_three:
        item_data = {
            'tweet': create_tweet(summary),
            'bulletPoints': create_bullet_points(summary)
        }
        formatted_items.append(item_data)

    return formatted_items

def create_tweet(summary):  
    conversation = [
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes news articles into Tweet-style summaries."
            },
            {
                "role": "user",
                "content": f"Please make a tweet for this news summary: {summary}"
            }
        ]
        
    response = openai.ChatCompletion.create(
            model=model_engine,
            messages=conversation,
            max_tokens=500,
            n=1,
            temperature=0.5
        )
    

    tweet = response.choices[0].message["content"].strip()
    return tweet

def create_bullet_points(summary):
    # response = openai.Completion.create(
    #     engine="gpt-3.5-turbo",
    #     prompt=f"Create 3 bullet points for the following news summary: {summary}",
    #     max_tokens=300,
    #     n=1,
    #     stop=None,
    #     temperature=0.7,
    # )

    conversation = [
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes news articles into bullet points."
            },
            {
                "role": "user",
                "content": f"Please make 3 to 7 bullet points for this news summary: {summary}"
            }
        ]
        
    response = openai.ChatCompletion.create(
            model=model_engine,
            messages=conversation,
            max_tokens=500,
            n=1,
            temperature=0.5
        )

    bullet_points = response.choices[0].message["content"].strip().split('\n')
    return bullet_points