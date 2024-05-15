from typing import List, Dict

PROMPT_LIMIT = 3750

def chunk_text(text: str, chunk_size: int = 200) -> List[str]:
    """
    Split text into chunks of a specified size.

    Args:
        text (str): The text to be chunked.
        chunk_size (int): The maximum size of each chunk.

    Returns:
        List[str]: A list of text chunks.
    """
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += sentence + '. '
        else:
            chunks.append(current_chunk)
            current_chunk = sentence + '. '
    if current_chunk:
        chunks.append(current_chunk)

    return chunks

def build_prompt(query: str, context_chunks: List[str]) -> str:
    """
    Build a prompt for the language model using the query and context chunks.

    Args:
        query (str): The query to be answered.
        context_chunks (List[str]): The context chunks to be included in the prompt.

    Returns:
        str: The constructed prompt.
    """
    print(f"Number of context chunks received: {len(context_chunks)}")
    prompt_start = (
        "Answer the question based on the context below. If you don't know the answer based on the context provided below, just respond with 'I don't know' instead of making up an answer. Don't start your response with the word 'Answer:'"
        "Context:\n"
    )
    prompt_end = f"\n\nQuestion: {query}\nAnswer:"
    prompt = ""
    for i in range(1, len(context_chunks)):
        if len("\n\n---\n\n".join(context_chunks[:i])) >= PROMPT_LIMIT:
            prompt = (
                prompt_start +
                "\n\n---\n\n".join(context_chunks[:i-1]) +
                prompt_end
            )
            break
        elif i == len(context_chunks)-1:
            prompt = (
                prompt_start +
                "\n\n---\n\n".join(context_chunks) +
                prompt_end
            )

    if not prompt:
        prompt = prompt_start + "No sufficient context available." + prompt_end

    print(f"Final prompt length: {len(prompt)}")
    
    return prompt   

def construct_messages_list(chat_history: List[Dict[str, str]], prompt: str) -> List[Dict[str, str]]:
    """
    Construct a list of messages for the language model based on chat history and the new prompt.

    Args:
        chat_history (List[Dict[str, str]]): The history of the chat.
        prompt (str): The new prompt to be added to the messages.

    Returns:
        List[Dict[str, str]]: A list of messages for the language model.
    """
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    
    for message in chat_history:
        if message['isBot']:
            messages.append({"role": "system", "content": message["text"]})
        else:
            messages.append({"role": "user", "content": message["text"]})

    messages[-1]["content"] = prompt    
    
    return messages
