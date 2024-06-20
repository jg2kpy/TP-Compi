from classes.MNLPTK import MNLPTK
import PySimpleGUI as sg
import os

tokens_dir = './tokens/'
examples_dir = '../examples/'

def main(verbose=False):
    mnlptk = MNLPTK(tokens_dir, verbose)

    layout = [
        [sg.Text('Archivo ATC:'), sg.InputText(key='-ATC-', size=(40, 1)), sg.FileBrowse(file_types=(("Text Files", "*.txt"),))],
        [sg.Text('Archivo EXP:'), sg.InputText(key='-EXP-', size=(40, 1)), sg.FileBrowse(file_types=(("Text Files", "*.txt"),))],
        [sg.Button('Procesar'), sg.Button('Salir')],
        [sg.Output(size=(80, 20), key='-OUTPUT-')]
    ]

    window = sg.Window('MNLPTK Processor', layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Salir':
            break
        if event == 'Procesar':
            atc_file = values['-ATC-']
            exp_file = values['-EXP-']

            if os.path.exists(atc_file) and os.path.exists(exp_file):
                atc_score = mnlptk.score(atc_file)
                exp_score = mnlptk.score(exp_file)
                average_score = (atc_score + exp_score) / 2
                print(f'Puntuación general: {average_score}\n')
            else:
                print('Por favor, seleccione archivos válidos.')

    window.close()

if __name__ == "__main__":
    main()
