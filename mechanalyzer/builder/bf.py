""" build the dictionaries of the product branching fractions
"""

from mechanalyzer.calculator import bf
# probably more useful to turn this into a class


def bf_tp_dct(modeltype, ped_df, hoten_df, bf_threshold, rxn='', savefile=False, fne=None):
    """ Build a branching fractions dictionary as a
        function of temeprature and pressure
        containing the BFs of each product of the PES

        :param modeltype: model used for P(E1) calculations
        :type modeltype: str
        :param ped_df: dataframe[P][T] with the Series of energy distrib [en: prob(en)]
        :type ped_df: dataframe(series(float))
        :param hoten_df: hot branching fractions for hotspecies
        :type hoten_df: df[P][T]:df[allspecies][energies]}
        :param reac: label of original reactants producing hot species - only for file save
        :type hotreac: str
        :param fne: branching fractions at T,P for each product
            for the selected hotspecies
        :type fne: dataframe of series df[P][T]:series[species],
            dataframe(series(float)) (same as bf_tp_df)
        :return bf_tp_dct: branching fractions at T,P for each product
            for the selected hotspecies
        :rtype: dct{species: {pressure: (array(T), array(BF))}}
    """

    if modeltype == 'fne':
        bf_tp_df = fne
    else:
        bf_tp_df = bf.bf_tp_df_full(ped_df, hoten_df)

    bf_tp_dct_species = bf.bf_tp_df_todct(
        bf_tp_df, bf_threshold, model=modeltype, rxn=rxn, savefile=savefile)
    _bf_tp_dct = bf_tp_dct_species

    return _bf_tp_dct


def merge_bf_ktp(bf_ktp_dct, ktp_dct, frag_reacs, otherprod, hotsp_dct):
    """ derive k' = bf*k and rename final ktp dictionary appropriately

        :param bf_tp_dct: branching fractions at T,P for each product
            for the selected hotspecies
        :type: dct{species: {pressure: (array(T), array(BF))}}
        :param ktp_dct: rates of the original reaction A=>B to split in A=>Pi
            with Pi = species in bf_ktp_dct (B decomposes to Pi)
        :type ktp_dct: dictionary {P: (T, k)}
        :param frag_reacs: reactant fragments ['A','B']
        :type frag_reacs: tuple/list(str)
        :param otherprod: remaining product(s)
        :type otherprod: tuple(str)
        :param hotsp_dct: dictionary of hotspecies and
            corresponding fragments (if bimol)
        :type hotsp_dct: {species_unimol: [species_unimol],
                          species_bimol: [frag1, frag2], ...}
        :return rxn_ktp_dct: ktp dct of final rate constants for channels
        :rtype: {rxn: {P: (T, k)}}
    """

    ktp_dct_model_i = bf.merge_bf_rates(bf_ktp_dct, ktp_dct)
    ktp_dct_model_i_new = rename_ktp_dct(
        ktp_dct_model_i, frag_reacs, otherprod, hotsp_dct)
    rxn_ktp_dct = ktp_dct_model_i_new

    return rxn_ktp_dct


def rename_ktp_dct(ktp_dct, frag_reacs, otherprod, hotsp_dct):
    """ rename ktp dictionary with appropriate names for prompt dissociation.
        ktp_dct.keys(): sp
        renamed_ktp_dct.keys(): rctname=>sp
        if sp is the original product, the reaction is reversible =

        :param rxn_ktp_dct: ktp dct of final rate constants for channels
        :type rxn_ktp_dct: {sp: {P: (T, k)}}
        :param frag_reacs: reactant fragments ['A','B']
        :type frag_reacs: tuple/list(str)
        :param otherprod: remaining product(s)
        :type otherprod: tuple
        :return rename_ktp_dct: dct with new keys
        :rtype: {rxn_name: {P: (T, k)}}
    """

    renamed_ktp_dct = {}
    for spc in ktp_dct.keys():
        frag_prods = hotsp_dct[spc] + otherprod
        print(hotsp_dct[spc], otherprod, frag_prods)
        newkey = (frag_reacs, frag_prods, (None,))
        renamed_ktp_dct[newkey] = ktp_dct[spc]

    return renamed_ktp_dct
