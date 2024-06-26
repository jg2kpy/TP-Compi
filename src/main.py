import PySimpleGUI as sg
import os
import matplotlib.pyplot as plt
from classes.MNLPTK import MNLPTK

tokens_dir = './tokens/'
examples_dir = '../examples/'

def main(verbose=True):
    mnlptk = MNLPTK(tokens_dir, verbose)
    atc_scores = []
    exp_scores = []
    scores = []

    layout = [
        [sg.Text('Archivo ATC:'), sg.InputText(key='-ATC-', size=(40, 1)), sg.FileBrowse(file_types=(("Text Files", "*.txt"),))],
        [sg.Text('Archivo EXP:'), sg.InputText(key='-EXP-', size=(40, 1)), sg.FileBrowse(file_types=(("Text Files", "*.txt"),))],
        [sg.Button('Procesar'), sg.Button('Limpiar'), sg.Button('Generar Gráfico'), sg.Button('Salir')],
        [sg.ProgressBar(100, orientation='h', size=(40, 20), key='-PROGRESS-', visible=False)],
        [sg.Output(size=(80, 20), key='-OUTPUT-')]
    ]

    window = sg.Window('MNLPTK Processor', layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Salir':
            break
        if event == 'Limpiar':
            window['-ATC-'].update('')
            window['-EXP-'].update('')
            window['-OUTPUT-'].update('')
            atc_scores.clear()
            exp_scores.clear()
            scores.clear()
        if event == 'Procesar':
            atc_file = values['-ATC-']
            exp_file = values['-EXP-']

            if os.path.exists(atc_file) and os.path.exists(exp_file):
                window['-PROGRESS-'].update(visible=True)
                window['-OUTPUT-'].update('')
                window.refresh()

                atc_score = mnlptk.score(atc_file, 'ATC')
                window['-PROGRESS-'].update(50)
                window.refresh()

                exp_score = mnlptk.score(exp_file, 'EXP')
                window['-PROGRESS-'].update(100)
                window.refresh()

                avg_score = round((atc_score + exp_score) / 2)
                scores.append(avg_score)
                atc_scores.append(atc_score)
                exp_scores.append(exp_score)

                for cut_point in sorted(mnlptk.score_labels.keys(), reverse=True):
                    if avg_score > cut_point:
                        print(f'Puntuación general: {avg_score} {mnlptk.score_labels[cut_point]}\n')
                        break

                window['-PROGRESS-'].update(0, visible=False)
            else:
                sg.popup_error('Por favor, seleccione archivos válidos.')
        if event == 'Generar Gráfico':
            if scores:
                plot_scores(atc_scores, exp_scores, scores)
            else:
                sg.popup_error('No hay datos para generar el gráfico.')

    window.close()

def plot_scores(atc_scores, exp_scores, scores):
    plt.figure(figsize=(15, 10))

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

    plt.subplot(2, 1, 2)
    plt.bar(range(len(scores)), scores, color='purple')
    plt.xlabel('Ejemplos')
    plt.ylabel('Puntuación General Promedio')
    plt.title('Puntuaciones Generales')
    plt.xticks(range(len(scores)), [f'Ejemplo {i}' for i in range(len(scores))])

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
