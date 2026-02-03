import os

def create_init_files(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        init_file = os.path.join(dirpath, '__init__.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write('')
            print(f"Created {init_file}")

if __name__ == "__main__":
    create_init_files('src')
