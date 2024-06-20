import classes.MNLPTK as mnlptk_class

examples = 6
tokens_dir = './tokens/'
examples_dir = '../examples/'

def main():
    mnlptk = mnlptk_class.MNLPTK(tokens_dir)
    for i in range(examples):
        atc_file = f'{examples_dir}ATC_{i}.txt'
        exp_file = f'{examples_dir}EXP_{i}.txt'
        mnlptk.score(atc_file)
        mnlptk.score(exp_file)
        print()

    print('Para cambiar un lexema de su token, mueva el lexema en el fichero correspondiente y vuelva a ejecutar el programa.')

if __name__ == "__main__":
    main()
