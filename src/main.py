import classes.MNLPTK as mnlptk_class

# Número de ejemplos a procesar
examples = 6
# Directorio donde se encuentran los tokens
tokens_dir = './tokens/'
# Directorio donde se encuentran los archivos de ejemplos
examples_dir = '../examples/'

def main(verbose=False):
    # Crear una instancia de la clase MNLPTK
    mnlptk = mnlptk_class.MNLPTK(tokens_dir, verbose)
    for i in range(examples):
        # Generar nombres de archivos para ATC y EXP
        atc_file = f'{examples_dir}ATC_{i}.txt'
        exp_file = f'{examples_dir}EXP_{i}.txt'
        # Obtener las puntuaciones de los archivos
        atc_score = mnlptk.score(atc_file)
        exp_score = mnlptk.score(exp_file)
        # Imprimir la puntuación general promedio
        print(f'Puntuación general: {str((atc_score + exp_score) / 2)} \n')

    # Mensaje informativo
    print('Para cambiar un lexema de su token, mueva el lexema en el fichero correspondiente y vuelva a ejecutar el programa.')

# Ejecutar la función principal si el script se ejecuta directamente
if __name__ == "__main__":
    main()
