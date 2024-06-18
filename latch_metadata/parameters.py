
from dataclasses import dataclass
import typing
import typing_extensions

from flytekit.core.annotation import FlyteAnnotation

from latch.types.metadata import NextflowParameter
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir

# Import these into your `__init__.py` file:
#
# from .parameters import generated_parameters

generated_parameters = {
    'input': NextflowParameter(
        type=str,
        default=None,
        section_title='Input/output options',
        description='URI/path to an [SDRF](https://github.com/bigbio/proteomics-metadata-standard/tree/master/annotated-projects) file **OR** globbing pattern for URIs/paths of mzML or Thermo RAW files',
    ),
    'outdir': NextflowParameter(
        type=typing.Optional[typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})]],
        default=None,
        section_title=None,
        description='The output directory where the results will be saved.',
    ),
    'email': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Email address for completion summary.',
    ),
    'root_folder': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Main parameters (SDRF)',
        description='Root folder in which the spectrum files specified in the SDRF are searched',
    ),
    'local_input_type': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Overwrite the file type/extension of the filename as specified in the SDRF',
    ),
    'expdesign': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Main parameters (spectra files)',
        description="A tab-separated experimental design file in OpenMS' own format (TODO link). All input files need to be present as a row with exactly the same names. If no design is given, unrelated, unfractionated runs are assumed.",
    ),
    'database': NextflowParameter(
        type=str,
        default=None,
        section_title='Protein database',
        description='The `fasta` protein database used during database search.',
    ),
    'add_decoys': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Generate and append decoys to the given protein database',
    ),
    'decoy_affix': NextflowParameter(
        type=typing.Optional[str],
        default='DECOY_',
        section_title=None,
        description='Pre- or suffix of decoy proteins in their accession',
    ),
    'affix_type': NextflowParameter(
        type=typing.Optional[str],
        default='prefix',
        section_title=None,
        description='Location of the decoy marker string in the fasta accession. Before (prefix) or after (suffix)',
    ),
    'openms_peakpicking': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Spectrum preprocessing',
        description='Activate OpenMS-internal peak picking',
    ),
    'peakpicking_inmemory': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Perform peakpicking in memory',
    ),
    'peakpicking_ms_levels': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Which MS levels to pick as comma separated list. Leave empty for auto-detection.',
    ),
    'search_engines': NextflowParameter(
        type=typing.Optional[str],
        default='comet',
        section_title='Database search',
        description='A comma separated list of search engines. Valid: comet, msgf',
    ),
    'enzyme': NextflowParameter(
        type=typing.Optional[str],
        default='Trypsin',
        section_title=None,
        description="The enzyme to be used for in-silico digestion, in 'OpenMS format'",
    ),
    'num_enzyme_termini': NextflowParameter(
        type=typing.Optional[str],
        default='fully',
        section_title=None,
        description='Specify the amount of termini matching the enzyme cutting rules for a peptide to be considered. Valid values are `fully` (default), `semi`, or `none`',
    ),
    'allowed_missed_cleavages': NextflowParameter(
        type=typing.Optional[int],
        default=2,
        section_title=None,
        description='Specify the maximum number of allowed missed enzyme cleavages in a peptide. The parameter is not applied if `unspecific cleavage` is specified as enzyme.',
    ),
    'precursor_mass_tolerance': NextflowParameter(
        type=typing.Optional[int],
        default=5,
        section_title=None,
        description='Precursor mass tolerance used for database search. For High-Resolution instruments a precursor mass tolerance value of 5 ppm is recommended (i.e. 5). See also [`--precursor_mass_tolerance_unit`](#--precursor_mass_tolerance_unit).',
    ),
    'precursor_mass_tolerance_unit': NextflowParameter(
        type=typing.Optional[str],
        default='ppm',
        section_title=None,
        description="Precursor mass tolerance unit used for database search. Possible values are 'ppm' (default) and 'Da'.",
    ),
    'fragment_mass_tolerance': NextflowParameter(
        type=typing.Optional[float],
        default=0.03,
        section_title=None,
        description='Fragment mass tolerance used for database search. The default of 0.03 Da is for high-resolution instruments.',
    ),
    'fragment_mass_tolerance_unit': NextflowParameter(
        type=typing.Optional[str],
        default='Da',
        section_title=None,
        description="Fragment mass tolerance unit used for database search. Possible values are 'ppm' (default) and 'Da'.",
    ),
    'fixed_mods': NextflowParameter(
        type=typing.Optional[str],
        default='Carbamidomethyl (C)',
        section_title=None,
        description='A comma-separated list of fixed modifications with their Unimod name to be searched during database search',
    ),
    'variable_mods': NextflowParameter(
        type=typing.Optional[str],
        default='Oxidation (M)',
        section_title=None,
        description='A comma-separated list of variable modifications with their Unimod name to be searched during database search',
    ),
    'isotope_error_range': NextflowParameter(
        type=typing.Optional[str],
        default='0,1',
        section_title=None,
        description="Comma-separated range of integers with allowed isotope peak errors for precursor tolerance (MS-GF+ parameter '-ti'). E.g. -1,2",
    ),
    'instrument': NextflowParameter(
        type=typing.Optional[str],
        default='high_res',
        section_title=None,
        description="Type of instrument that generated the data. 'low_res' or 'high_res' (default; refers to LCQ and LTQ instruments)",
    ),
    'protocol': NextflowParameter(
        type=typing.Optional[str],
        default='automatic',
        section_title=None,
        description='MSGF only: Labeling or enrichment protocol used, if any. Default: automatic',
    ),
    'min_precursor_charge': NextflowParameter(
        type=typing.Optional[int],
        default=2,
        section_title=None,
        description="Minimum precursor ion charge. Omit the '+'",
    ),
    'max_precursor_charge': NextflowParameter(
        type=typing.Optional[int],
        default=4,
        section_title=None,
        description="Maximum precursor ion charge. Omit the '+'",
    ),
    'min_peptide_length': NextflowParameter(
        type=typing.Optional[int],
        default=6,
        section_title=None,
        description='Minimum peptide length to consider (works with MSGF and in newer Comet versions)',
    ),
    'max_peptide_length': NextflowParameter(
        type=typing.Optional[int],
        default=40,
        section_title=None,
        description='Maximum peptide length to consider (works with MSGF and in newer Comet versions)',
    ),
    'num_hits': NextflowParameter(
        type=typing.Optional[int],
        default=1,
        section_title=None,
        description='Specify the maximum number of top peptide candidates per spectrum to be reported by the search engine. Default: 1',
    ),
    'max_mods': NextflowParameter(
        type=typing.Optional[int],
        default=3,
        section_title=None,
        description='Maximum number of modifications per peptide. If this value is large, the search may take very long.',
    ),
    'db_debug': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description="Debug level when running the database search. Logs become more verbose and at '>5' temporary files are kept.",
    ),
    'enable_mod_localization': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Modification localization',
        description='Turn the mechanism on.',
    ),
    'mod_localization': NextflowParameter(
        type=typing.Optional[str],
        default='Phospho (S),Phospho (T),Phospho (Y)',
        section_title=None,
        description='Which variable modifications to use for scoring their localization.',
    ),
    'allow_unmatched': NextflowParameter(
        type=typing.Optional[str],
        default='false',
        section_title='Peptide re-indexing',
        description='Do not fail if there are some unmatched peptides. Only activate as last resort, if you know that the rest of your settings are fine!',
    ),
    'IL_equivalent': NextflowParameter(
        type=typing.Optional[str],
        default='true',
        section_title=None,
        description='Should isoleucine and leucine be treated interchangeably when mapping search engine hits to the database? Default: true',
    ),
    'posterior_probabilities': NextflowParameter(
        type=typing.Optional[str],
        default='percolator',
        section_title='PSM re-scoring (general)',
        description="How to calculate posterior probabilities for PSMs:\n\n* 'percolator' = Re-score based on PSM-feature-based SVM and transform distance\n    to hyperplane for posteriors\n* 'fit_distributions' = Fit positive and negative distributions to scores\n    (similar to PeptideProphet)",
    ),
    'psm_pep_fdr_cutoff': NextflowParameter(
        type=typing.Optional[float],
        default=0.1,
        section_title=None,
        description='FDR cutoff on PSM level (or potential peptide level; see Percolator options) before going into feature finding, map alignment and inference.',
    ),
    'pp_debug': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description="Debug level when running the re-scoring. Logs become more verbose and at '>5' temporary files are kept.",
    ),
    'FDR_level': NextflowParameter(
        type=typing.Optional[str],
        default='peptide-level-fdrs',
        section_title='PSM re-scoring (Percolator)',
        description="Calculate FDR on PSM ('psm-level-fdrs') or peptide level ('peptide-level-fdrs')?",
    ),
    'train_FDR': NextflowParameter(
        type=typing.Optional[float],
        default=0.05,
        section_title=None,
        description='The FDR cutoff to be used during training of the SVM.',
    ),
    'test_FDR': NextflowParameter(
        type=typing.Optional[float],
        default=0.05,
        section_title=None,
        description='The FDR cutoff to be used during testing of the SVM.',
    ),
    'subset_max_train': NextflowParameter(
        type=typing.Optional[int],
        default=300000,
        section_title=None,
        description='Only train an SVM on a subset of PSMs, and use the resulting score vector to evaluate the other PSMs. Recommended when analyzing huge numbers (>1 million) of PSMs. When set to 0, all PSMs are used for training as normal. This is a runtime vs. discriminability tradeoff. Default: 300,000',
    ),
    'description_correct_features': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description='Use additional features whose values are learnt by correct entries. See help text. Default: 0 = none',
    ),
    'outlier_handling': NextflowParameter(
        type=typing.Optional[str],
        default='none',
        section_title='PSM re-scoring (distribution fitting)',
        description='How to handle outliers during fitting:\n\n* ignore_iqr_outliers (default): ignore outliers outside of `3*IQR` from Q1/Q3 for fitting\n* set_iqr_to_closest_valid: set IQR-based outliers to the last valid value for fitting\n* ignore_extreme_percentiles: ignore everything outside 99th and 1st percentile (also removes equal values like potential censored max values in XTandem)\n* none: do nothing',
    ),
    'consensusid_algorithm': NextflowParameter(
        type=typing.Optional[str],
        default='best',
        section_title='Consensus ID',
        description='How to combine the probabilities from the single search engines: best, combine using a sequence similarity-matrix (PEPMatrix), combine using shared ion count of peptides (PEPIons). See help for further info.',
    ),
    'consensusid_considered_top_hits': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description='Only use the top N hits per search engine and spectrum for combination. Default: 0 = all',
    ),
    'min_consensus_support': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description='A threshold for the ratio of occurence/similarity scores of a peptide in other runs, to be reported. See help.',
    ),
    'protein_inference': NextflowParameter(
        type=typing.Optional[str],
        default='aggregation',
        section_title='Protein inference ',
        description="The inference method to use. 'aggregation' (default) or 'bayesian'.",
    ),
    'protein_level_fdr_cutoff': NextflowParameter(
        type=typing.Optional[float],
        default=0.05,
        section_title=None,
        description='The experiment-wide protein (group)-level FDR cutoff. Default: 0.05',
    ),
    'protein_quant': NextflowParameter(
        type=typing.Optional[str],
        default='unique_peptides',
        section_title='Protein Quantification',
        description="Quantify proteins based on:\n\n* 'unique_peptides' = use peptides mapping to single proteins or a group of indistinguishable proteins (according to the set of experimentally identified peptides)\n* 'strictly_unique_peptides' = use peptides mapping to a unique single protein only\n* 'shared_peptides' = use shared peptides, too, but only greedily for its best group (by inference score)",
    ),
    'quantification_method': NextflowParameter(
        type=typing.Optional[str],
        default='feature_intensity',
        section_title=None,
        description="Choose between feature-based quantification based on integrated MS1 signals ('feature_intensity'; default) or spectral counting of PSMs ('spectral_counting'). **WARNING:** 'spectral_counting' is not compatible with our MSstats step yet. MSstats will therefore be disabled automatically with that choice.",
    ),
    'mass_recalibration': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description="Recalibrates masses based on precursor mass deviations to correct for instrument biases. (default: 'false')",
    ),
    'transfer_ids': NextflowParameter(
        type=typing.Optional[str],
        default='false',
        section_title=None,
        description="Tries a targeted requantification in files where an ID is missing, based on aggregate properties (i.e. RT) of the features in other aligned files (e.g. 'mean' of RT). (**WARNING:** increased memory consumption and runtime). 'false' turns this feature off. (default: 'false')",
    ),
    'targeted_only': NextflowParameter(
        type=typing.Optional[bool],
        default=True,
        section_title=None,
        description="Only looks for quantifiable features at locations with an identified spectrum. Set to false to include unidentified features so they can be linked and matched to identified ones (= match between runs). (default: 'true')",
    ),
    'inf_quant_debug': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description="Debug level when running the re-scoring. Logs become more verbose and at '>666' potentially very large temporary files are kept.",
    ),
    'skip_post_msstats': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Statistical post-processing',
        description='Skip MSstats for statistical post-processing?',
    ),
    'ref_condition': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Instead of all pairwise contrasts (default), uses the given condition name/number (corresponding to your experimental design) as a reference and creates pairwise contrasts against it. (TODO not yet fully implemented)',
    ),
    'contrasts': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description="Allows full control over contrasts by specifying a set of contrasts in a semicolon seperated list of R-compatible contrasts with the condition names/numbers as variables (e.g. `1-2;1-3;2-3`). Overwrites '--ref_condition' (TODO not yet fully implemented)",
    ),
    'enable_qc': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Quality control',
        description="Enable generation of quality control report by PTXQC? default: 'false' since it is still unstable",
    ),
    'ptxqc_report_layout': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Specify a yaml file for the report layout (see PTXQC documentation) (TODO not yet fully implemented)',
    ),
}

