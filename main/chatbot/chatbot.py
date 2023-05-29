import nltk
import json
import random
import pickle
import numpy as np
from nltk import TreebankWordTokenizer
from nltk.stem import WordNetLemmatizer
from keras.models import load_model


class ChatBot:
    def __init__(self):
        self.word_net = WordNetLemmatizer()
        self.model = load_model('main/chatbot/chatbot_model.h5')
        self.conversations = json.loads(open('main/chatbot/conversations.json', encoding='utf-8').read())
        self.words = pickle.load(open('main/chatbot/list_words.pkl', 'rb'))
        self.classes = pickle.load(open('main/chatbot/cls.pkl', 'rb'))
        self.ERROR_LIMIT = 0.25

    def chatbot_response(self, msg: str):
        request_with_probability = self.__return_list_predict_words(msg, self.model)
        answer_chatbot = self.__getResponse(request_with_probability, self.conversations)
        return answer_chatbot

    def __getResponse(self, request_with_probability, conversations_json):
        section = request_with_probability[0]['request']
        list_of_conversations = conversations_json['conversations']
        result = ''
        for i in list_of_conversations:
            if (i['section'] == section):
                result = random.choice(i['responses'])
                break
            else:
                result = "Zadałeś niepoprawnie pytanie"
        return result

    def __clean_sentence_with_tokenizer_word(self, sentence):
        word_tokenizer = TreebankWordTokenizer().tokenize(sentence)
        sentence_words = [self.word_net.lemmatize(word.lower()) for word in word_tokenizer]
        return sentence_words

    def __return_list_predict_words(self, sentence, model):
        np_array_words = self.__create_np_array_with_words(sentence, self.words)
        section = model.predict(np.array([np_array_words]))[0]
        results = [[i, r] for i, r in enumerate(section) if r > self.ERROR_LIMIT]
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({"request": self.classes[r[0]], "probability": str(r[1])})
        return return_list

    def __create_np_array_with_words(self, sentence, words):
        sentence_words = self.__clean_sentence_with_tokenizer_word(sentence)
        array_zero = [0] * len(words)
        for sentence in sentence_words:
            for index, word in enumerate(words):
                if word == sentence:
                    array_zero[index] = 1
        return (np.array(array_zero))
