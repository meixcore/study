import os

folder_name = "Управление_файлами"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

current_directory = os.getcwd()
print("Текущая директория:", current_directory)

os.chdir(f'{current_directory}\\Управление_файлами')

with open('file1.txt', 'w', encoding='utf-8') as file:
    file.write('123')

with open('file2.txt', 'w', encoding='utf-8') as f:
    f.write('321')

files_and_dirs = os.listdir('.')
print("Файлы и директории:", files_and_dirs)

os.remove('file2.txt')

if not os.path.exists(folder_name):
    os.makedirs(folder_name)

os.rename('file1.txt', os.path.join('Управление_файлами', 'file1.txt'))

os.chdir(f'{current_directory}')

def delete_directory_if_exists(path):
    if os.path.exists(path):
        contents = os.listdir(path)

        if contents:
            for item in contents:
                item_path = os.path.join(path, item)

                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    delete_directory_if_exists(item_path)

        os.rmdir(path)
        print(f"Удалена директория: {path}")
    else:
        print("Такой директории не существует.")

delete_directory_if_exists(folder_name)