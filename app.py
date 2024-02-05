from ChatGptAgent import GPTAgent
from LocalChatAgent import LocalChatAgent

if __name__ == "__main__":
    # model = GPTAgent()
    model = LocalChatAgent()

    while True:
        # Do something
        question = input('Enter your question: ')

        if not question.strip() :
            break

        print(f'AI answer: {model.answer(question)}')

