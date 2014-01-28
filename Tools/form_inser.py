
def main():
    rem = "%s = _form.cleaned_data['%s'], \n"
    sho = "<tr>\n    <td>{{ exam_lbl.%s }}:</td>\n    <td>{{ exam.%s }}</td>\n</tr>\n"
    lines = open('file.txt')
    out = open("form.txt", "w")
    keys = open("keys.txt", "w")
    for line in lines:
        key = line.split("=")[0]
        key = key.replace(" ", "")
        out.write(rem %(key, key))
        keys.write(sho %(key, key))
    out.close()
    keys.close()


if __name__ == '__main__':
    main()


