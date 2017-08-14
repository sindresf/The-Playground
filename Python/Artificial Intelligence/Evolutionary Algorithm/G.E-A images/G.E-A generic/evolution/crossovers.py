#methods for performing crossover
def split_mid(gene1,gene2):#TODO actually make this
    return gene1[0:2] + gene2[3:5]

def split_most_fit(amount,most_fit_gene,other_gene):
    return most_fit_gene[0:amount] + other_gene[amount:5]