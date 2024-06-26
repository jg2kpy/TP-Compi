import classes.MNLPTK as mnlptk_class
import matplotlib.pyplot as plt

# Número de ejemplos a procesar
examples = 6
# Directorio donde se encuentran los tokens
tokens_dir = './tokens/'
# Directorio donde se encuentran los archivos de ejemplos
examples_dir = '../examples/'

def main(verbose=True):
    mnlptk = mnlptk_class.MNLPTK(tokens_dir, verbose)
    scores = []

    for i in range(examples):
        print(f'Ejecutando ejemplo {i}')
        atc_file = f'{examples_dir}ATC_{i}.txt'
        exp_file = f'{examples_dir}EXP_{i}.txt'
        atc_score = mnlptk.score(atc_file, 'ATC')
        exp_score = mnlptk.score(exp_file, 'EXP')
        avg_score = round((atc_score + exp_score) / 2)
        scores.append(avg_score)
        # Imprimir la puntuación general promedio
        for cut_point in sorted(mnlptk.score_labels.keys(), reverse=True):
            if avg_score > cut_point:
                print(f'Puntuación general: {avg_score} {mnlptk.score_labels[cut_point]}\n')
                break
        print(f'Fin de ejemplo {i}\n')

    # Mensaje informativo
    print('Para cambiar un lexema de su token, mueva el lexema en el fichero correspondiente y vuelva a ejecutar el programa.')

    return scores

def plot_scores(scores):
    # Crear un gráfico de barras
    plt.figure(figsize=(10, 5))
    plt.bar(range(len(scores)), scores, color='blue')
    plt.xlabel('Ejemplos')
    plt.ylabel('Puntuación General Promedio')
    plt.title('Comparación de Puntuaciones Generales Promedio por Ejemplo')
    plt.xticks(range(len(scores)), [f'Ejemplo {i}' for i in range(len(scores))])
    plt.show()

# Ejecutar la función principal si el script se ejecuta directamente
if __name__ == "__main__":
    scores = main()
    plot_scores(scores)
