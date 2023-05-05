#!/usr/bin/env python3
import os
import sys
import argparse
import time
import threading

# Configuración de colores
COLOR_NC = '\033[0m'
COLOR_YELLOW = '\033[1;33m'
COLOR_CYAN = '\033[1;36m'
COLOR_MAGENTA = '\033[1;35m'
COLOR_RED = '\033[1;31m'

# Palabras clave a buscar
keywords = ['password', 'pass', 'passwd']

# Configuración de colores
COLOR_NC = '\033[0m'
COLOR_YELLOW = '\033[1;33m'
COLOR_CYAN = '\033[1;36m'
COLOR_MAGENTA = '\033[1;35m'
COLOR_RED = '\033[1;31m'

# Función para imprimir el banner
def print_banner():
    print(COLOR_MAGENTA)
    print(' __                  __   ___       __   __      ') 
    print('|__) |  | |    |    /__` |__   /\  |__) /  ` |__|') 
    print('|__) \__/ |___ |___ .__/ |___ /~~\ |  \ \__, |  |')
    print(COLOR_NC)

# Función para buscar las palabras clave en un archivo
def search_file(file_path):
    try:
        for keyword in keywords:
            with open(file_path, 'r') as file:
                for num, line in enumerate(file, 1):
                    if keyword in line.lower():
                        print(f'{COLOR_YELLOW}[+] Se ha encontrado la palabra "{keyword}"{COLOR_NC} en el archivo {COLOR_CYAN}"{file_path}"{COLOR_NC} en la línea {COLOR_RED}{num}{COLOR_NC}')
    except Exception as e:
        pass

# Función para buscar en un directorio
def search_directory(search_dir, exclude_dirs=[]):
    for entry in os.scandir(search_dir):
        if entry.is_file():
            search_file(entry.path)
        elif entry.is_dir():
            if entry.path not in exclude_dirs:
                search_directory(entry.path, exclude_dirs)

# Función para mostrar barra de progreso
def show_progress_bar():
    for i in range(1, 4):
        time.sleep(1)
        print(COLOR_CYAN + '.' * i + COLOR_NC, end='', flush=True)

# Función para procesar los argumentos del usuario
def process_args():
    parser = argparse.ArgumentParser(description='Búsqueda de palabras clave en archivos')
    parser.add_argument('--keywords', nargs='+', default=keywords, help='Palabras clave a buscar')
    parser.add_argument('--search-in', nargs='+', required=True, help='Directorios donde buscar')
    parser.add_argument('--exclude-dirs', nargs='+', default=[], help='Directorios a excluir de la búsqueda')
    args = parser.parse_args()
    return args

# Función principal
def main():
    # Procesar argumentos
    args = process_args()

    # Asignar palabras clave
    global keywords
    keywords = args.keywords

    # Buscar palabras clave en los directorios especificados
    for search_dir in args.search_in:
        print(COLOR_CYAN + f'Buscando en: {search_dir}' + COLOR_NC)
        search_directory(search_dir, args.exclude_dirs)

if __name__ == '__main__':
    # Imprimir banner
    print_banner()

    # Mostrar barra de progreso
    print('Iniciando BullSearcher...')
    progress_thread = threading.Thread(target=show_progress_bar)
    progress_thread.start()
    progress_thread.join()
    print('\n')

    # Ejecutar programa
    try:
        main()
    except KeyboardInterrupt:
        print('\n' + COLOR_RED + 'Programa interrumpido por el usuario' + COLOR_NC)
        sys.exit(1)

