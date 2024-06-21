import PySimpleGUI as sg
import os
from classes.MNLPTK import MNLPTK

tokens_dir = './tokens/'
examples_dir = '../examples/'

def main(verbose=False):
    mnlptk = MNLPTK(tokens_dir, verbose)

    layout = [
        [sg.Text('Archivo ATC:'), sg.InputText(key='-ATC-', size=(40, 1)), sg.FileBrowse(file_types=(("Text Files", "*.txt"), ))],
        [sg.Text('Archivo EXP:'), sg.InputText(key='-EXP-', size=(40, 1)), sg.FileBrowse(file_types=(("Text Files", "*.txt"), ))],
        [sg.Button('Procesar'), sg.Button('Limpiar'), sg.Button('Salir')],
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
        if event == 'Procesar':
            atc_file = values['-ATC-']
            exp_file = values['-EXP-']

            if os.path.exists(atc_file) and os.path.exists(exp_file):
                window['-PROGRESS-'].update(visible=True)
                window['-OUTPUT-'].update('')
                window.refresh()

                atc_score = mnlptk.score(atc_file)
                window['-PROGRESS-'].update(50)
                window.refresh()

                exp_score = mnlptk.score(exp_file)
                window['-PROGRESS-'].update(100)
                window.refresh()

                average_score = (atc_score + exp_score) / 2

                print(f'Puntuación ATC: {atc_score}')
                print(f'Puntuación EXP: {exp_score}')
                print(f'Puntuación general: {average_score}\n')

                window['-PROGRESS-'].update(0, visible=False)
            else:
                sg.popup_error('Por favor, seleccione archivos válidos.')

    window.close()

if __name__ == "__main__":
    main()
