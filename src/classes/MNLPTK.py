from classes.Tokens import Tokens

class MNLPTK:
    def __init__(self, tokens_directory='./tokens/', verbose=False):

        # Inicializar la clase Tokens
        self.tokens = Tokens()
        # Establecer el directorio de tokens
        self.tokens.token_dir = tokens_directory
        # Puntuaciones asociadas a cada categoría de tokens
        self.tokens_score = {
            'MUY_MALAS': -10,
            'MALAS': -5,
            'NEUTRAS': 0,
            'BUENAS': 5,
            'MUY_BUENAS': 10
        }
        # Modo verboso
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


    # Etiquetas de puntuación
    score_labels = {
        90: '(5/5 MUY BUENO)',
        75: '(4/5 BUENO)',
        25: '(3/5 NEUTRO)',
        10: '(2/5 MALO)',
        0: '(1/5 MUY MALO)'
    }

    def score(self, file_dir):
        # Calcular la puntuación de un archivo
        new_lexamas, final_score, lexemas_used = self.lexical_analyzer(file_dir)
        # Aplicar ajuste a la puntuación final
        final_score = round((final_score + 10) * 5, 2)

        for cut_point in sorted(self.score_labels.keys(), reverse=True):
            if final_score >= cut_point:
                print(f"'{file_dir}': {final_score} {self.score_labels[cut_point]}")
                print(str(new_lexamas) + ' lexemas a NEUTRO')

                if self.verbose:
                    # Verificar saludo
                    self.verify_greeting(lexemas_used)
                    # Imprimir lista de lexemas usados si verbose es True
                    self.list_lexemas(lexemas_used)

                return final_score


    def lexical_analyzer(self, file_dir):
        # Diccionario para rastrear los lexemas utilizados y sus tokens correspondientes
        lexemas_used = {}

        # Abrir el archivo especificado en modo de lectura con codificación UTF-8
        with open(file_dir, 'r', encoding='utf-8') as input_file:
            try:

                # Tokenizar el contenido del archivo
                tokenized_text = self.tokenizer(input_file.read())
                partial_score = 0
                non_neutral_lexemas = 1
                new_lexamas = 0

                # Iterar a través de los lexemas tokenizados
                for lexemas in tokenized_text:
                    if lexemas in self.tokens.hash_table:
                        partial_score += self.tokens_score[self.tokens.hash_table[lexemas]]
                        if self.tokens_score[self.tokens.hash_table[lexemas]] != 0:
                            non_neutral_lexemas += 1
                    else:
                        self.tokens.add(lexemas, 'NEUTRAS')
                        new_lexamas = new_lexamas + 1

                    # Registrar el lexema y su token correspondiente en el diccionario
                    lexemas_used[lexemas] = self.tokens.hash_table[lexemas]

                # Devolver el número de nuevos lexemas, la puntuación parcial promedio y los lexemas utilizados
                return (new_lexamas, partial_score / non_neutral_lexemas, lexemas_used)
            except FileNotFoundError:
                print(f"Error: Fichero '{file_dir}' no encotrado.")
            except IOError as e:
                print(f"Error de E/S '{file_dir}': {e}")
            except Exception as e:
                print(f"Error inesperado: {e}")


    # Signos de puntuación en español
    punctuation_signs_spanish = '¡!¿?".,;:()[]{}<>-—–"«»“”‘’'

    # Tokenizar el texto
    def tokenizer(self, text):
        processed_words = []
        for word in text.split():
            clean_word = word.strip(self.punctuation_signs_spanish)
            clean_word = clean_word.lower()
            processed_words.append(clean_word)
        return processed_words


    # Verificar si hay un saludo en los lexemas usados
    def verify_greeting(self, lexemas_used):
        greeting = False
        for lexema, token in lexemas_used.items():
            if lexema == 'hola' or lexema == 'buenos' or lexema == 'buenas' or lexema == 'tardes' or lexema == 'dias' or lexema == 'noches':
                greeting = True
                break
        print('Saludo detectado\n' if greeting else 'Saludo no detectado\n')


    # Listar los lexemas usados por categoría
    def list_lexemas(self, lexemas_used):
        print('Lexemas usados:')
        for token1 in self.tokens_score.keys():
            print(token1)
            for lexema, token2 in lexemas_used.items():
                if token1 == token2:
                    print(lexema, end=', ')
