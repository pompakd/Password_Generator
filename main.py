import argparse
import os.path
import secrets
import string


def get_command_args():
    parser = argparse.ArgumentParser(prog='Password (de)generator',
                                    description='Generate strong (or not) passwords')
    parser.add_argument('-s', '--strength', help='choose a strength: \
                        pin(only digits), week(only letters),\
                        medium(letters + digits, default), \
                        strong(letter + digits + special characters)', default='medium')
    parser.add_argument('-l', '--length', type=int, help ='By default 15', default=15)
    parser.add_argument('-f', '--filename', help='Choose a file to save password')
    parser.add_argument('-n', '--number', type=int, help='Number password to generate, default is 1',
                        default=1)

    return parser.parse_args()
    

class PassGenerator():
    
    def __init__(self, strength, length, number, filename):
        self.passwords = []
        self.strength = strength
        self.length = length
        self.filename = filename
        self.number = number

    def _generate_pass(self):
        random = secrets.SystemRandom()

        match self.strength.lower():
            case 'pin':
                self.pass_dict = string.digits
            case 'low':
                self.pass_dict = string.ascii_letters
            case 'medium':
                self.pass_dict = string.ascii_letters + string.digits
            case 'strong':
                self.pass_dict = string.ascii_letters + string.digits + string.punctuation
            case _:
                raise ValueError('Available arguments: pin, low, medium, strong')

   
        for pass_unit in range(self.number):
            password = ''.join(random.choice(self.pass_dict) for i in range(self.length))
            self.passwords.append(password) 
    
    @staticmethod
    def write_to_file(data, filename):
        if os.path.exists(filename):
            file_choice = input(f'{filename} already exists, want to rewrite it? [y]n: ')
            if file_choice.lower() not in ['', 'y', 'yes']:
                exit('Interrupted')
        
        try:
            with open(filename, 'w') as f:
                f.write('\n'.join(data))
                f.write('\n')
            print('Done!')
        except Exception as e:
            raise(f'{e}\n\
                 Something went wrong\n\
                 Check your file permissions.')

    def run_generator(self):
        self._generate_pass()

        if self.filename:
            self.write_to_file(self.passwords, self.filename)
        else:
            for password in self.passwords:
                print(password)


def main():
    args = get_command_args()
    pass_gen = PassGenerator(args.strength, args.length, args.number, args.filename)
    pass_gen.run_generator()


if __name__ == '__main__':
    main()


