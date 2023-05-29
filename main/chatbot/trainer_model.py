from typing import Tuple

import nltk
import json
import pickle
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD
import random

from nltk import TreebankWordTokenizer
from nltk.stem import WordNetLemmatizer

from main.tools.tools import return_sorted_list_object


class TrainerModel:

    def __init__(self, *, download: bool):
        self.__download_nltk(download)
        self.words = []
        self.classes = []
        self.documents = []
        self.initial_training_data = []
        self.ignore_words = ['?', '!', ',', '.', '@', 'xD']
        self.lemmatizer = WordNetLemmatizer()
        self.conversations = json.loads(open('conversations.json', encoding='utf-8').read())

    def trainer(self):
        self.__tokenize_text_based_on_regular_expressions()
        self.words = self.__lemmatize_word_with_check_ignore_list()
        self.words = return_sorted_list_object(self.words)
        self.classes = return_sorted_list_object(self.classes)
        self.__write_pickled_representation_object(self.words, 'list_words.pkl')
        self.__write_pickled_representation_object(self.classes, 'cls.pkl')

        output_list = [0] * len(self.classes)
        self.__prepare_the_initial_test_data(output_list)
        random.shuffle(self.initial_training_data)
        training = self.__create_array(self.initial_training_data)

        train_requests = list(training[:, 0])
        train_conversations = list(training[:, 1])
        print("Stworzono dane testowe.")

        training_data_requests_tuple = (len(train_requests[0]),)
        length_training_conversations = len(train_conversations[0])

        array_train_requests = self.__create_array(train_requests)
        array_train_conversations = self.__create_array(train_conversations)

        model = Sequential()

        self.__add_layers_to_model(model, training_data_requests_tuple, length_training_conversations)
        model.compile(loss='categorical_crossentropy',
                      optimizer=self.__create_sgd_object(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True),
                      metrics=['accuracy'])

        fitting_model = model.fit(array_train_requests, array_train_conversations, epochs=200, batch_size=5,
                                  verbose=1)
        try:
            model.save('chatbot_model.h5', fitting_model)
            print("Model stworzono")
        except Exception:
            print("Nie zapisano modelu")

    def __create_array(self, arg):
        return np.array(arg)

    def __add_layers_to_model(self, model: Sequential, training_data_requests_tuple: Tuple[int],
                              length_training_conversations: int):

        self.__create_layer_with_arguments(model=model, input_shape=training_data_requests_tuple, activation='relu',
                                           units=128)
        model.add(Dropout(0.5))
        self.__create_layer_with_arguments(model=model, activation='relu', units=64)
        model.add(Dropout(0.5))
        self.__create_layer_with_arguments(model=model, activation='softmax', units=length_training_conversations)

    def __create_layer_with_arguments(self, *, model: Sequential, units: int, activation: str,
                                      input_shape: Tuple[int] = None):
        if input_shape is not None:
            return model.add(Dense(input_shape=input_shape, activation=activation, units=units))
        else:
            return model.add(Dense(activation=activation, units=units))

    def __prepare_the_initial_test_data(self, output_list: list):
        for doc in self.documents:
            locker = []
            pattern_words = self.__lemmatize_word(doc[0])
            for w in self.words:
                locker.append(1) if w in pattern_words else locker.append(0)
            output_row = list(output_list)
            output_row[self.classes.index(doc[1])] = 1
            self.initial_training_data.append([locker, output_row])

    def __download_nltk(self, download: bool):
        if download:
            nltk.download()

    def __create_sgd_object(self, *, learning_rate: float, decay: float, momentum: float, nesterov: bool):
        return SGD(learning_rate=learning_rate, decay=decay, momentum=momentum, nesterov=nesterov)

    def __tokenize_text_based_on_regular_expressions(self):
        """TreebankWordTokenizer odpowiada za tokenizacje."""
        for intent in self.conversations['conversations']:
            for req in intent['requests']:
                word_tokenizer = TreebankWordTokenizer().tokenize(req)
                self.words.extend(word_tokenizer)
                self.documents.append((word_tokenizer, intent['section']))
                if intent['section'] not in self.classes:
                    self.classes.append(intent['section'])

    def __lemmatize_word_with_check_ignore_list(self):
        """Sprawdza czy słowo znajduje się WordNet, jeśli nie to zwraca niezmienione."""
        return [self.lemmatizer.lemmatize(word=lemmatize_word.lower()) for lemmatize_word in self.words if
                lemmatize_word not in self.ignore_words]

    def __lemmatize_word(self, pattern_words):
        """Sprawdza czy słowo znajduje się WordNet, jeśli nie to zwraca niezmienione."""
        return [self.lemmatizer.lemmatize(word.lower()) for word in pattern_words]

    def __write_pickled_representation_object(self, list_words: list, name_file: str):
        """Serializacja obiektów pythonoowych na otwartym pliku."""
        pickle.dump(list_words, open(name_file, 'wb'))


if __name__ == '__main__':
    TrainerModel(download=False).trainer()
