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
    atc_scores = []
    exp_scores = []

    for i in range(examples):
        print(f'Ejecutando ejemplo {i}')
        atc_file = f'{examples_dir}ATC_{i}.txt'
        exp_file = f'{examples_dir}EXP_{i}.txt'
        atc_score = mnlptk.score(atc_file, 'ATC')
        exp_score = mnlptk.score(exp_file, 'EXP')
        avg_score = round((atc_score + exp_score) / 2)
        scores.append(avg_score)
        atc_scores.append(atc_score)
        exp_scores.append(exp_score)
        # Imprimir la puntuación general promedio
        for cut_point in sorted(mnlptk.score_labels.keys(), reverse=True):
            if avg_score > cut_point:
                print(f'Puntuación general: {avg_score} {mnlptk.score_labels[cut_point]}\n')
                break
        print(f'Fin de ejemplo {i}\n')

    # Mensaje informativo
    print('Para cambiar un lexema de su token, mueva el lexema en el fichero correspondiente y vuelva a ejecutar el programa.')

    return atc_scores, exp_scores, scores

def plot_scores(atc_scores, exp_scores, scores):
    # Crear un gráfico de barras para ATC y EXP por separado
    plt.figure(figsize=(15, 10))

    # Subplot 1: Puntuaciones ATC y EXP
    plt.subplot(2, 1, 1)
    bar_width = 0.35
    index = range(len(atc_scores))

    plt.bar(index, atc_scores, bar_width, label='ATC', color='blue')
    plt.bar([i + bar_width for i in index], exp_scores, bar_width, label='EXP', color='black')

    plt.xlabel('Ejemplos')
    plt.ylabel('Puntuación')
    plt.title('Puntuaciones ATC y EXP')
    plt.xticks([i + bar_width / 2 for i in index], [f'Ejemplo {i}' for i in index])
    plt.legend()

    # Subplot 2: Puntuación General Promedio
    plt.subplot(2, 1, 2)
    plt.bar(range(len(scores)), scores, color='purple')
    plt.xlabel('Ejemplos')
    plt.ylabel('Puntuación General Promedio')
    plt.title('Puntuaciones Generales')
    plt.xticks(range(len(scores)), [f'Ejemplo {i}' for i in range(len(scores))])

    plt.tight_layout()
    plt.show()

# Ejecutar la función principal si el script se ejecuta directamente
if __name__ == "__main__":
    atc_scores, exp_scores, scores = main()
    plot_scores(atc_scores, exp_scores, scores)
