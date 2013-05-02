import os

__author__ = 'jontedesco'

firstPubsTemplate = '\\textbf{%d} & \\textbf{%s} & \\textbf{%s} & \\textbf{%s} & \\textbf{%s} \\\\\n'
firstNoPubsTemplate = '\\textbf{%d} & \\textbf{%s} & \\textbf{%s} & \\textbf{%s} \\\\\n'
middlePubsTemplate = '%d & %s & %s & %s & %s \\\\\n'
middleNoPubsTemplate = '%d & %s & %s &  %s \\\\\n'

showPublications = True

for filename in os.listdir('.'):
    if 'PathSim' not in filename and 'NeighborSim' not in filename: continue
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
                            + '& %s Score\\\\\n\hline\n' % measure
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
                    latexContent += firstPubsTemplate % (rank, author, citations, publications, score)
                else:
                    latexContent += firstNoPubsTemplate % (rank, author, citations, score)
            else:
                if showPublications:
                    latexContent += middlePubsTemplate % (rank, author, citations, publications, score)
                else:
                    latexContent += middleNoPubsTemplate % (rank, author, citations, score)
    with open(os.path.join('latex', filename), 'w') as outputFile:
        outputFile.write(latexContent)
