import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CRLF remover.')
    parser.add_argument('-f', '--filename', help='List of files to test with', required=True)

    args = parser.parse_args()

    filename_input = args.filename
    filename_output = 'singleline_' + filename_input

    with open(filename_output, "w", newline='') as file_out:
        with open(filename_input) as file_in:
            line_count = 1
            for line in file_in:
                line_ = line.strip("\n")
                # print('Line count: {}'.format(line_count), end='\r')
                print('line: {}'.format(line_))
                line_count += 1
                file_out.write('{} '.format(line_))
