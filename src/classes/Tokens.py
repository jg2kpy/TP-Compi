class Tokens:
    token_dir = ''  # Directorio de tokens
    hash_table = {}  # TO DO: Hacer un hash table

    def from_text(self, token_name, text):
        # Agregar lexemas a la tabla hash desde un texto
        for lexema in text:
            self.hash_table[lexema] = token_name

    def add(self, lexema, token_name):
        # Agregar un lexema a la tabla hash y actualizar el archivo correspondiente
        self.hash_table[lexema] = token_name
        self._to_file(token_name, f'{self.token_dir}{token_name}.txt')

    def _to_file(self, token_name, token_file):
        # Guardar los lexemas en el archivo correspondiente
        with open(token_file, 'w', encoding='utf-8') as file:
            for lexema, token in self.hash_table.items():
                if token == token_name:
                    file.write(lexema + '\n')
