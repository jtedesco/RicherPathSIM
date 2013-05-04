import os

__author__ = 'jontedesco'

showPublications = True
showScore = False

firstPubsTemplate = '\\textbf{%d} & \\textbf{%s} & \\textbf{%s} & \\textbf{%s} ' + ('& \\textbf{%s}' if showScore else '') + ' \\\\\n'
firstNoPubsTemplate = '\\textbf{%d} & \\textbf{%s} & \\textbf{%s} ' + ('& \\textbf{%s}' if showScore else '') + ' \\\\\n'
middlePubsTemplate = '%d & %s & %s & %s ' + ('& %s' if showScore else '') + ' \\\\\n'
middleNoPubsTemplate = '%d & %s & %s & ' + ('& %s' if showScore else '') + ' \\\\\n'

for filename in os.listdir('.'):
    if 'PathSim' not in filename and 'NeighborSim' not in filename and 'ShapeSim' not in filename:
        continue
    measure = 'PathSim' if 'PathSim' in filename else 'NeighborSim'
    content = open(filename).read()
    latexContent = ""
    rank = 0
    for line in content.split('\n'):
        if line.startswith('Most Similar'):
            rank = 0
            latexContent += '\hline\n\end{tabular}\n\n'
            latexContent += '\\begin{tabular}{|c|c|c|c|c|}\n\hline\nRank & Author & Citations \\footnotemark[1] ' \
                            + ('& Publications \\footnotemark[1]' if showPublications else '')\
                            + ('& %s Score' % measure if showScore else '') + '\\\\\n\hline\n'
        elif line.startswith('+='):
            continue
        elif 'Author' in line:
            continue
        elif line.startswith('| '):
            rank += 1
            tokens = line[1:].split('|')
            author = tokens[0].strip()
            score = tokens[1].strip()
            citations = tokens[2].strip()
            publications = tokens[3].strip()
            if rank == 1:
                if showPublications:
                    latexContent += firstPubsTemplate % tuple(
                        [rank, author, citations, publications] + ([score] if showScore else []))
                else:
                    latexContent += firstNoPubsTemplate % tuple([rank, author, citations] + ([score] if showScore else []))
            else:
                if showPublications:
                    latexContent += middlePubsTemplate % tuple([rank, author, citations, publications] + ([score] if showScore else []))
                else:
                    latexContent += middleNoPubsTemplate % tuple([rank, author, citations] + ([score] if showScore else []))
    with open(os.path.join('latex', filename), 'w') as outputFile:
        outputFile.write(latexContent)
