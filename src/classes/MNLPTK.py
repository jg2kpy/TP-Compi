from classes.Tokens import Tokens

class MNLPTK:

    def __init__(self, tokens_directory='./tokens/', verbose=False):

        self.tokens = Tokens()
        self.tokens.token_dir = tokens_directory
        self.tokens_score = {
            'MUY_MALAS': -10,
            'MALAS': -5,
            'NEUTRAS': 0,
            'BUENAS': 5,
            'MUY_BUENAS': 10
        }
        self.verbose = verbose

        # Leer archivos de tokens y procesarlos
        for token_name in self.tokens_score.keys():
            try:
                with open(f'{tokens_directory}{token_name}.txt', 'r', encoding='utf-8') as token_file:
                    tokenized_text = self.tokenizer(token_file.read())
                    self.tokens.from_text(token_name, tokenized_text)
            except FileNotFoundError:
                print(f"Error: Fichero '{tokens_directory}{token_name}.txt' no encontrado.")
            except IOError as e:
                print(f"Error de E/S '{tokens_directory}{token_name}.txt': {e}")
            except Exception as e:
                print(f"Error inesperado: {e}")

        self.greetings = self.load_phrases(f'{tokens_directory}SALUDOS.txt')
        self.farewells = self.load_phrases(f'{tokens_directory}DESPEDIDAS.txt')

    def load_phrases(self, file_path):
        phrases = []
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = self.tokenizer(line)
                    phrases.append(line)
        except FileNotFoundError:
            print(f"Error: Fichero '{file_path}' no encontrado.")
        except IOError as e:
            print(f"Error de E/S '{file_path}': {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")
        return phrases

    score_labels = {
        90: '(5/5 MUY BUENO)',
        75: '(4/5 BUENO)',
        25: '(3/5 NEUTRO)',
        10: '(2/5 MALO)',
        0: '(1/5 MUY MALO)'
    }

    def score(self, file_dir, user):
        print(f'Procesando archivo {file_dir}...')
        new_lexamas, final_score, lexemas_used, tokenized_text = self.lexical_analyzer(file_dir)
        if new_lexamas > 0:
            print(f'Nuevos lexemas detectados: {new_lexamas} a NEUTRAS\n')

        final_score = round((final_score + 10) * 5, 2)
        if user == 'ATC':
            greetings = self.verify(tokenized_text, self.greetings)
            farewells = self.verify(tokenized_text, self.farewells)
            if greetings:
                print('Saludo detectado +5 puntos')
                final_score += 5
            else:
                print('Saludo no detectado -10 puntos')
                final_score -= 10
            if farewells:
                print('Despedida detectada +5 puntos')
                final_score += 5
            else:
                print('Despedida no detectada -10 puntos')
                final_score -= 10

        for cut_point in sorted(self.score_labels.keys(), reverse=True):
            if final_score > cut_point:
                score = self.score_labels[cut_point]

                if user == 'EXP':
                    self.list_lexemas(lexemas_used)

                print(f'Puntuación {user}: {final_score} {score}\n')

                return final_score

    def lexical_analyzer(self, file_dir):
        lexemas_used = {}

        with open(file_dir, 'r', encoding='utf-8') as input_file:
            try:
                tokenized_text = self.tokenizer(input_file.read())
                partial_score = 0
                non_neutral_lexemas = 1
                new_lexamas = 0

                for lexemas in tokenized_text:
                    token = self.tokens.get(lexemas)
                    if token:
                        partial_score += self.tokens_score[token]
                        if self.tokens_score[token] != 0:
                            non_neutral_lexemas += 1
                    else:
                        self.tokens.add(lexemas, 'NEUTRAS')
                        new_lexamas += 1

                    lexemas_used[lexemas] = self.tokens.hash_table[lexemas]

                return (new_lexamas, partial_score / non_neutral_lexemas, lexemas_used, tokenized_text)
            except FileNotFoundError:
                print(f"Error: Fichero '{file_dir}' no encontrado.")
            except IOError as e:
                print(f"Error de E/S '{file_dir}': {e}")
            except Exception as e:
                print(f"Error inesperado: {e}")

    punctuation_signs_spanish = '¡!¿?".,;:()[]{}<>-—–"«»“”‘’'

    def tokenizer(self, text):
        processed_words = []
        for word in text.split():
            clean_word = word.strip(self.punctuation_signs_spanish)
            clean_word = clean_word.lower()
            processed_words.append(clean_word)
        return processed_words

    def verify(self, tokenized_text, words_to_verify):
        detected = False

        for word_sequence in words_to_verify:
            sequence_length = len(word_sequence)
            for i in range(len(tokenized_text) - sequence_length + 1):
                if tokenized_text[i:i + sequence_length] == word_sequence:
                    detected = True
                    break
            if detected:
                break

        return detected

    def list_lexemas(self, lexemas_used):
        print('Lexemas usados:')
        list_lexemas = []
        for token1 in self.tokens_score.keys():
            if token1 != 'NEUTRAS':
                for lexema, token2 in lexemas_used.items():
                    if token1 == token2:
                        list_lexemas.append(lexema)
                if list_lexemas:
                    print(f'{token1}: {", ".join(list_lexemas)}')
                list_lexemas = []
        print()
