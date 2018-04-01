if __name__ == '__main__':
    import numpy as np
    from MMFinder import MMFinder as mmf

    d = 1
    o = 1
    i = 1
    u = 1

    # === (0) load dataset ===
    mypop2 = mmf('genotypes.txt')

    # === (1) create init population ===
    mypop2.make_population(marker_on='all_one', popsize=100)
    mypop2.set_coefficients(w_d=d, w_o=o, w_i=i, w_u=u)
    max_sc = mypop2.max_distinguishable_pairs()
    sc, sv = mypop2.scoring()

    print('N of pairs: %d' % mypop2.total_pairs)
    print('N of Distinguishable pairs: %f' % mypop2.MaxDistN)

    print('------')
    print(max_sc)
    print(0, mypop2.best_score, np.sum(mypop2.best_chrom, axis=1), np.max(sv[0]))

    # === (2) repeat selection & crossing & mutation ===
    for rep in range(0,100):

        mypop2.selection()
        mypop2.recombination()
        mypop2.mutation(r_mutation=0.5)

        sc, sv = mypop2.scoring()

        print(rep+1, mypop2.best_score, np.sum(mypop2.best_chrom, axis=1), np.max(sv[0]))

    best_chrom = mypop2.best_chrom
    print(best_chrom)
