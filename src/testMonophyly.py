import pandas as pd
import tskit as tsk

ts = tsk.load("../../data/sim/IM_m0_T1_chr1_1e4.trees")

def testMonophyly(tree, pop_by_node) :
    pops = pd.DataFrame(columns=['nodes'])

    for node in tree.leaves(tree.root):
        current_pop = pop_by_node.loc(node)['pop']
        if current_pop != 2 :
            if (current_pop not in pops.index):
                pops.loc[current_pop] = [[]]
            pops.at[current_pop, 'nodes'].append(node)
    
    pops['mrca'] = pops['nodes'].apply(lambda x: tree.mrca(*x))
    pops['toplevelChildren'] = pops['mrca'].apply(lambda x: list(tree.leaves(x)))
    return (pops['nodes'] == pops['toplevelChildren']).all()