import os

def list_files(startpath, output_file):
    with open(output_file, 'w') as f:
        for root, dirs, files in os.walk(startpath):
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * (level)
            f.write('{}{}/\n'.format(indent, os.path.basename(root)))
            subindent = ' ' * 4 * (level + 1)
            for file in files:
                f.write('{}{}\n'.format(subindent, file))

if __name__ == "__main__":
    startpath = os.path.dirname(os.path.abspath(__file__))  # este obtendrá la ruta del directorio actual del script
    output_filename = "project_structure.txt"
    list_files(startpath, output_filename)
    print(f"Estructura guardada en {output_filename}")
