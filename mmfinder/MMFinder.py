class MMFinder():

    # === Starting 'MMFinder' ===
    def __init__(self, input_data, Delimiter='\t', HeaderLineNo=-1, IndexCol=0, random_seed=None):
        import pandas as pd
        import numpy as np
        import scipy.special as ss

        # --- Loading dataset ---
        dataset = pd.read_csv(input_data, sep=Delimiter, header=HeaderLineNo, index_col=IndexCol)
        dataset.index.name = 'MarkerID'

        # --- Getting information ---
        self.df           = dataset
        self.N_indviduals = len(dataset.columns)
        self.N_markers    = len(dataset)
        self.total_pairs  = ss.comb(self.N_indviduals, 2)
        self.best_score   = 0
        self.best_chrom   = []

        # Information of markers
        culc_freq = lambda x: pd.value_counts(x)/len(x)
        gt_freqs = self.df.apply(culc_freq, axis=1).fillna(0)

        # number of genotype "A"
        if 'A' in gt_freqs:
            self.gt_A_freq = np.array(gt_freqs['A'])
        else:
            self.gt_A_freq = np.zeros(self.N_markers)
        # number of genotype "B"
        if 'B' in gt_freqs:
            self.gt_B_freq = np.array(gt_freqs['B'])
        else:
            self.gt_B_freq = np.zeros(self.N_markers)
        # number of genotype "-(missing data)"
        if '-' in gt_freqs:
            self.gt_UN_freq = np.array(gt_freqs['-'])
        else:
            self.gt_UN_freq = np.zeros(self.N_markers)

        # --- Culculating theoretical number of markers ---
        for m in range(self.N_markers):
            if self.N_indviduals <= 2**m:
                self.theorical_marker_num = m
                break
            self.theorical_marker_num = self.N_markers

        # --- Culculating Max number of distinguishable pairs ---
        self.MaxDistN = self.max_distinguishable_pairs()

        # --- Setting random-seed ---
        np.random.seed(random_seed)

        # --- Print out ---
        print('=== Dataset ===')
        print(input_data)
        print('- %d individuals' % self.N_indviduals)
        print('- %d markers' % self.N_markers)
        print('===============')

    def set_coefficients(self, w_d=1, w_o=1, w_i=1, w_u=1):
        self.w_d = w_d
        self.w_o = w_o
        self.w_i = w_i
        self.w_u = w_u

    # === Initial population ===
    def make_population(self,  popsize=10, marker_on='minimum', turn_on_N=5):
        import numpy as np

        # --- Preparing population ---
        self.chrompop = []
        for i in range(popsize):
            # --- Create chromosome ---
            chrom_fwk = [0] * self.N_markers
            chrom_idx = [j for j in range(self.N_markers)]

            # --- Conditon branch by "marker_on"---
            if marker_on == 'minimum':
                choiced_idx = np.random.choice(chrom_idx, size=self.theorical_marker_num, replace=False)
            elif marker_on == 'one':
                choiced_idx = np.random.choice(chrom_idx, size=1, replace=False)
            elif marker_on == 'two':
                choiced_idx = np.random.choice(chrom_idx, size=2, replace=False)
            elif marker_on == 'three':
                choiced_idx = np.random.choice(chrom_idx, size=3, replace=False)
            elif marker_on == 'arbitrarily':
                choiced_idx = np.random.choice(chrom_idx, size=turn_on_N, replace=False)
            elif marker_on == 'all_one':
                choiced_idx = chrom_idx
            else:
                choiced_N = np.random.randint(1, self.N_markers+1, size=1)
                choiced_idx = np.random.choice(chrom_idx, size=choiced_N, replace=False)

            # --- Change status of markers on chromosome: 0 => 1  ---
            for k in choiced_idx:
                chrom_fwk[k] = 1

            # --- Add chromosome to population ---
            self.chrompop.append(chrom_fwk)

        return self.chrompop

    # === Selection ===
    def selection(self, selective_pressure=1.0):
        import numpy as np

        # --- Selection ---
        curpop_size = len(self.chrompop)
        newpop_size = int(curpop_size * selective_pressure)
        pop_idx = [i for i in range(curpop_size)]

        scores, _ = self.scoring()
        prob = scores/np.sum(scores)
        selected_idx = np.random.choice(pop_idx, size=newpop_size, replace=True, p=prob)
        self.chrompop = np.array(self.chrompop)[selected_idx].tolist()

    # === Recombination ===
    def recombination(self, prob=[0.50, 0.45, 0.05]):
        import numpy as np
        import copy

        # --- Parents ---
        mathers = copy.deepcopy(self.chrompop)
        fathers = copy.deepcopy(self.chrompop)
        np.random.shuffle(mathers)
        np.random.shuffle(fathers)

        # --- Recombination ---
        chrom_position = [i for i in range(self.N_markers)]
        newpop = []
        for m, f in zip(mathers, fathers):
            num = np.random.choice([0,1,2], p=prob)
            pos = np.random.choice(chrom_position, size=num)
            if len(pos) == 1:
                new_chrom = m[:pos[0]] + f[pos[0]:]
            elif len(pos) == 2:
                pos = np.sort(pos)
                new_chrom = m[:pos[0]] + f[pos[0]:pos[1]] + m[pos[1]:]
            else:
                new_chrom = m[:]
            newpop.append(new_chrom)

        self.chrompop = newpop

    # === Mutaiton ===
    def mutation(self, r_mutation=0.05):
        import numpy as np

        # --- Mutation ---
        chrom_position = [i for i in range(self.N_markers)]
        newpop = []
        for chrom in self.chrompop:
            if r_mutation > np.random.random():
                pos = np.random.choice(chrom_position)
                if chrom[pos]==1:
                    chrom[pos] = 0
                else:
                    chrom[pos] = 1
            newpop.append(chrom)

        self.chrompop = newpop


    # === Scoring ===
    def scoring(self, chrom=None):
        import numpy as np

        # --- Setting chromosome-array ---
        if chrom:
            arr = np.array(chrom)
        else:
            arr = np.array(self.chrompop)

        # --- each scores ---
        D = self.distinguishable_pairs()
        O = self.on_state_markers()
        I = self.informative_genotypes()
        U = self.missing_genotypes()

        # --- Scoring ---
        if np.max(D) == self.MaxDistN:
            D = [0 if v<self.MaxDistN else v for v in D]
        scores = (self.w_d * D) + (self.w_o * O) + (self.w_i * I) - (self.w_u * U)

        # --- Update best score & chromosome ---
        if self.best_score < np.max(scores):
            self.best_score = np.max(scores)
            self.best_chrom = arr[np.where(scores==self.best_score)]

        return scores, (D, O, I, U)

    # === Culculate frequency of Distinguishable pairs ===
    def distinguishable_pairs(self, chrom=None):
        import numpy as np
        import pandas as pd
        import itertools

        # --- Setting chromosome-array ---
        if chrom:
            arr = np.array(chrom)
        else:
            arr = np.array(self.chrompop)

        # --- Culculation ---
        D_num = [] # List of Num of distinguishable pairs
        for chrom in arr:
            idx = np.nonzero(chrom)  # index of ON-state markers
            if len(idx)==0:
                D_num.append(0)
                next

            GTs = []
            for genes in np.array(self.df).T:
                GTs.append(''.join(genes[idx])) # Strings of ON-state markers
            df_GTs = pd.DataFrame(GTs, columns=['Genotypes'])
            GTs_count = df_GTs.groupby('Genotypes').size()
            GTs_list  = GTs_count.index
            distinguishable = 0 # Num of distinguishable pairs

            for gt0, gt1 in list(itertools.combinations(GTs_list,2)):
                gt0_list = list(gt0)
                gt1_list = list(gt1)
                gt0_ungt_idx = [k for k, v in enumerate(gt0_list) if v!='A' and v!='B']
                gt1_ungt_idx = [k for k, v in enumerate(gt1_list) if v!='A' and v!='B']
                ungt_idx = list(set(gt0_ungt_idx + gt1_ungt_idx))

                for masked_idx in ungt_idx:
                    gt0_list[masked_idx] = '.'
                    gt1_list[masked_idx] = '.'
                gt0_str = ''.join(gt0_list)
                gt1_str = ''.join(gt1_list)
                if gt0_str != gt1_str:
                    distinguishable += GTs_count[gt0] * GTs_count[gt1]

            D_num.append(distinguishable)

        D = np.array(D_num / self.total_pairs)

        return D

    # === Culculate frequency of ON-state markers ===
    def on_state_markers(self, chrom=None):
        import numpy as np
        import numpy.ma as ma

        # --- Setting chromosome-array ---
        if chrom:
            arr = np.array(chrom)
        else:
            arr = np.array(self.chrompop)

        # --- Turn-off stderr for invalid values ---
        np.seterr(invalid='ignore')
        tmp = ma.masked_invalid(self.theorical_marker_num / np.sum(arr, axis=1))
        O = np.array(ma.fix_invalid(tmp, fill_value=0))

        # --- Turn-on stderr for invalid values ---
        np.seterr(invalid='warn')

        return O

    # === Culculate frequency of Informative genotypes ===
    def informative_genotypes(self, chrom=None):
        import numpy as np
        import numpy.ma as ma

        # --- Setting chromosome-array ---
        if chrom:
            arr = np.array(chrom)
        else:
            arr = np.array(self.chrompop)

        # --- Turn-off stderr for invalid values ---
        np.seterr(invalid='ignore')
        tmp = ma.masked_invalid(np.sum(arr * (self.gt_A_freq + self.gt_B_freq), axis=1) / np.sum(arr, axis=1))
        I = np.array(ma.fix_invalid(tmp, fill_value=0))

        # --- Turn-on stderr for invalid values ---
        np.seterr(invalid='warn')

        return I

    # === Culculate frequency of Uninformative genotypes (missing genotypes) ===
    def missing_genotypes(self, chrom=None):
        import numpy as np
        import numpy.ma as ma

        # --- Setting chromosome-array ---
        if chrom:
            arr = np.array(chrom)
        else:
            arr = np.array(self.chrompop)

        # --- Turn-off stderr for invalid values ---
        np.seterr(invalid='ignore')
        tmp = ma.masked_invalid(np.sum(arr * self.gt_UN_freq, axis=1) / np.sum(arr, axis=1))
        U = np.array(ma.fix_invalid(tmp, fill_value=0))

        # --- Turn-on stderr for invalid values ---
        np.seterr(invalid='warn')

        return U

    # === Max of Distinguishable pairs ==
    def max_distinguishable_pairs(self):
        import numpy as np

        max_d_pais = self.distinguishable_pairs(chrom=[np.ones(self.N_markers)])
        return max_d_pais

    # === Exhaustive Search (!!! Too long time. Not recommend !!!)===
    def exhaustive_search(self):
        li = [[0,1] for i in range(self.N_markers)]
        best_score = 0
        best_chrom = []
        for l in itertools.product(*li):
            print(list(l))
            self.scoring()
