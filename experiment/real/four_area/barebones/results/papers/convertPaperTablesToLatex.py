import os

__author__ = 'jontedesco'

# Construct the dictionary of number of citations for each paper
paperCitationFile = open('../../data/paperCitationCounts')
citationCounts = {}
for line in paperCitationFile:
    index = line.find(': ')
    count, title = line[:index], line[index+2:]
    title = title.strip().replace(' ', '')
    citationCounts[title] = int(count)

for filename in os.listdir('.'):
    if 'PathSim' in filename or 'NeighborSim' in filename:
        content = open(filename).read()
        latexContent = ""

        titleBuffer = ""
        score = 0

        for line in content.split('\n'):
            if line.startswith('Most Similar'):
                rank = 0
                latexContent += '\hline\n\end{tabular}\n\n'
                latexContent += '\\begin{tabular}{|c|c|c|c|}\n\hline\nRank & Paper & Citation Count & Score\\\\\n\hline\n'
            elif 'Paper' in line:
                continue
            elif line.startswith('| '):
                tokens = line[1:].split('|')
                titleBuffer += ' ' + tokens[0].strip()
                if len(tokens[1].strip()) > 0: score = float(tokens[1].strip())
            elif line.startswith('+-') and len(titleBuffer) > 0:
                rank += 1
                strippedTitle = titleBuffer.strip().replace(' ','')
                title = titleBuffer.strip()
                latexContent += '%d & %s & %s & %s \\\\\n' % (rank, title, citationCounts[strippedTitle], score)
                titleBuffer = ""
                score = 0
        with open(os.path.join('latex', filename), 'w') as outputFile:
            outputFile.write(latexContent)
