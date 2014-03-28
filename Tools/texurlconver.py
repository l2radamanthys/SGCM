
data = open('urls.txt', 'r').readlines()
out = open('urls-out.txt', 'w')
for line in data:
    line = line.replace("\\", "\\backslash")
    line = line.replace("%", "\\%")
    line = line.replace("_", "\\_")
    out.write(line)
out.close()
