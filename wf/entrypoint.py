from dataclasses import dataclass
from enum import Enum
import os
import subprocess
import requests
import shutil
from pathlib import Path
import typing
import typing_extensions

from latch.resources.workflow import workflow
from latch.resources.tasks import nextflow_runtime_task, custom_task
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir
from latch.ldata.path import LPath
from latch_cli.nextflow.workflow import get_flag
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.utils import urljoins
from latch.types import metadata
from flytekit.core.annotation import FlyteAnnotation

from latch_cli.services.register.utils import import_module_by_path

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_gib": 100,
        }
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]






@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(pvc_name: str, input: str, outdir: typing.Optional[typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})]], email: typing.Optional[str], root_folder: typing.Optional[str], local_input_type: typing.Optional[str], expdesign: typing.Optional[str], database: str, add_decoys: typing.Optional[bool], openms_peakpicking: typing.Optional[bool], peakpicking_inmemory: typing.Optional[bool], peakpicking_ms_levels: typing.Optional[str], db_debug: typing.Optional[int], enable_mod_localization: typing.Optional[bool], pp_debug: typing.Optional[int], description_correct_features: typing.Optional[int], consensusid_considered_top_hits: typing.Optional[int], min_consensus_support: typing.Optional[int], mass_recalibration: typing.Optional[bool], inf_quant_debug: typing.Optional[int], skip_post_msstats: typing.Optional[bool], ref_condition: typing.Optional[str], contrasts: typing.Optional[str], enable_qc: typing.Optional[bool], ptxqc_report_layout: typing.Optional[str], decoy_affix: typing.Optional[str], affix_type: typing.Optional[str], search_engines: typing.Optional[str], enzyme: typing.Optional[str], num_enzyme_termini: typing.Optional[str], allowed_missed_cleavages: typing.Optional[int], precursor_mass_tolerance: typing.Optional[int], precursor_mass_tolerance_unit: typing.Optional[str], fragment_mass_tolerance: typing.Optional[float], fragment_mass_tolerance_unit: typing.Optional[str], fixed_mods: typing.Optional[str], variable_mods: typing.Optional[str], isotope_error_range: typing.Optional[str], instrument: typing.Optional[str], protocol: typing.Optional[str], min_precursor_charge: typing.Optional[int], max_precursor_charge: typing.Optional[int], min_peptide_length: typing.Optional[int], max_peptide_length: typing.Optional[int], num_hits: typing.Optional[int], max_mods: typing.Optional[int], mod_localization: typing.Optional[str], allow_unmatched: typing.Optional[str], IL_equivalent: typing.Optional[str], posterior_probabilities: typing.Optional[str], psm_pep_fdr_cutoff: typing.Optional[float], FDR_level: typing.Optional[str], train_FDR: typing.Optional[float], test_FDR: typing.Optional[float], subset_max_train: typing.Optional[int], outlier_handling: typing.Optional[str], consensusid_algorithm: typing.Optional[str], protein_inference: typing.Optional[str], protein_level_fdr_cutoff: typing.Optional[float], protein_quant: typing.Optional[str], quantification_method: typing.Optional[str], transfer_ids: typing.Optional[str], targeted_only: typing.Optional[bool]) -> None:
    try:
        shared_dir = Path("/nf-workdir")



        ignore_list = [
            "latch",
            ".latch",
            "nextflow",
            ".nextflow",
            "work",
            "results",
            "miniconda",
            "anaconda3",
            "mambaforge",
        ]

        shutil.copytree(
            Path("/root"),
            shared_dir,
            ignore=lambda src, names: ignore_list,
            ignore_dangling_symlinks=True,
            dirs_exist_ok=True,
        )

        cmd = [
            "/root/nextflow",
            "run",
            str(shared_dir / "main.nf"),
            "-work-dir",
            str(shared_dir),
            "-profile",
            "docker",
            "-c",
            "latch.config",
                *get_flag('input', input),
                *get_flag('outdir', outdir),
                *get_flag('email', email),
                *get_flag('root_folder', root_folder),
                *get_flag('local_input_type', local_input_type),
                *get_flag('expdesign', expdesign),
                *get_flag('database', database),
                *get_flag('add_decoys', add_decoys),
                *get_flag('decoy_affix', decoy_affix),
                *get_flag('affix_type', affix_type),
                *get_flag('openms_peakpicking', openms_peakpicking),
                *get_flag('peakpicking_inmemory', peakpicking_inmemory),
                *get_flag('peakpicking_ms_levels', peakpicking_ms_levels),
                *get_flag('search_engines', search_engines),
                *get_flag('enzyme', enzyme),
                *get_flag('num_enzyme_termini', num_enzyme_termini),
                *get_flag('allowed_missed_cleavages', allowed_missed_cleavages),
                *get_flag('precursor_mass_tolerance', precursor_mass_tolerance),
                *get_flag('precursor_mass_tolerance_unit', precursor_mass_tolerance_unit),
                *get_flag('fragment_mass_tolerance', fragment_mass_tolerance),
                *get_flag('fragment_mass_tolerance_unit', fragment_mass_tolerance_unit),
                *get_flag('fixed_mods', fixed_mods),
                *get_flag('variable_mods', variable_mods),
                *get_flag('isotope_error_range', isotope_error_range),
                *get_flag('instrument', instrument),
                *get_flag('protocol', protocol),
                *get_flag('min_precursor_charge', min_precursor_charge),
                *get_flag('max_precursor_charge', max_precursor_charge),
                *get_flag('min_peptide_length', min_peptide_length),
                *get_flag('max_peptide_length', max_peptide_length),
                *get_flag('num_hits', num_hits),
                *get_flag('max_mods', max_mods),
                *get_flag('db_debug', db_debug),
                *get_flag('enable_mod_localization', enable_mod_localization),
                *get_flag('mod_localization', mod_localization),
                *get_flag('allow_unmatched', allow_unmatched),
                *get_flag('IL_equivalent', IL_equivalent),
                *get_flag('posterior_probabilities', posterior_probabilities),
                *get_flag('psm_pep_fdr_cutoff', psm_pep_fdr_cutoff),
                *get_flag('pp_debug', pp_debug),
                *get_flag('FDR_level', FDR_level),
                *get_flag('train_FDR', train_FDR),
                *get_flag('test_FDR', test_FDR),
                *get_flag('subset_max_train', subset_max_train),
                *get_flag('description_correct_features', description_correct_features),
                *get_flag('outlier_handling', outlier_handling),
                *get_flag('consensusid_algorithm', consensusid_algorithm),
                *get_flag('consensusid_considered_top_hits', consensusid_considered_top_hits),
                *get_flag('min_consensus_support', min_consensus_support),
                *get_flag('protein_inference', protein_inference),
                *get_flag('protein_level_fdr_cutoff', protein_level_fdr_cutoff),
                *get_flag('protein_quant', protein_quant),
                *get_flag('quantification_method', quantification_method),
                *get_flag('mass_recalibration', mass_recalibration),
                *get_flag('transfer_ids', transfer_ids),
                *get_flag('targeted_only', targeted_only),
                *get_flag('inf_quant_debug', inf_quant_debug),
                *get_flag('skip_post_msstats', skip_post_msstats),
                *get_flag('ref_condition', ref_condition),
                *get_flag('contrasts', contrasts),
                *get_flag('enable_qc', enable_qc),
                *get_flag('ptxqc_report_layout', ptxqc_report_layout)
        ]

        print("Launching Nextflow Runtime")
        print(' '.join(cmd))
        print(flush=True)

        env = {
            **os.environ,
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms2048M -Xmx8G -XX:ActiveProcessorCount=4",
            "K8S_STORAGE_CLAIM_NAME": pvc_name,
            "NXF_DISABLE_CHECK_LATEST": "true",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(urljoins("latch:///your_log_dir/nf_nf_core_proteomicslfq", name, "nextflow.log"))
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)



@workflow(metadata._nextflow_metadata)
def nf_nf_core_proteomicslfq(input: str, outdir: typing.Optional[typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})]], email: typing.Optional[str], root_folder: typing.Optional[str], local_input_type: typing.Optional[str], expdesign: typing.Optional[str], database: str, add_decoys: typing.Optional[bool], openms_peakpicking: typing.Optional[bool], peakpicking_inmemory: typing.Optional[bool], peakpicking_ms_levels: typing.Optional[str], db_debug: typing.Optional[int], enable_mod_localization: typing.Optional[bool], pp_debug: typing.Optional[int], description_correct_features: typing.Optional[int], consensusid_considered_top_hits: typing.Optional[int], min_consensus_support: typing.Optional[int], mass_recalibration: typing.Optional[bool], inf_quant_debug: typing.Optional[int], skip_post_msstats: typing.Optional[bool], ref_condition: typing.Optional[str], contrasts: typing.Optional[str], enable_qc: typing.Optional[bool], ptxqc_report_layout: typing.Optional[str], decoy_affix: typing.Optional[str] = 'DECOY_', affix_type: typing.Optional[str] = 'prefix', search_engines: typing.Optional[str] = 'comet', enzyme: typing.Optional[str] = 'Trypsin', num_enzyme_termini: typing.Optional[str] = 'fully', allowed_missed_cleavages: typing.Optional[int] = 2, precursor_mass_tolerance: typing.Optional[int] = 5, precursor_mass_tolerance_unit: typing.Optional[str] = 'ppm', fragment_mass_tolerance: typing.Optional[float] = 0.03, fragment_mass_tolerance_unit: typing.Optional[str] = 'Da', fixed_mods: typing.Optional[str] = 'Carbamidomethyl (C)', variable_mods: typing.Optional[str] = 'Oxidation (M)', isotope_error_range: typing.Optional[str] = '0,1', instrument: typing.Optional[str] = 'high_res', protocol: typing.Optional[str] = 'automatic', min_precursor_charge: typing.Optional[int] = 2, max_precursor_charge: typing.Optional[int] = 4, min_peptide_length: typing.Optional[int] = 6, max_peptide_length: typing.Optional[int] = 40, num_hits: typing.Optional[int] = 1, max_mods: typing.Optional[int] = 3, mod_localization: typing.Optional[str] = 'Phospho (S),Phospho (T),Phospho (Y)', allow_unmatched: typing.Optional[str] = 'false', IL_equivalent: typing.Optional[str] = 'true', posterior_probabilities: typing.Optional[str] = 'percolator', psm_pep_fdr_cutoff: typing.Optional[float] = 0.1, FDR_level: typing.Optional[str] = 'peptide-level-fdrs', train_FDR: typing.Optional[float] = 0.05, test_FDR: typing.Optional[float] = 0.05, subset_max_train: typing.Optional[int] = 300000, outlier_handling: typing.Optional[str] = 'none', consensusid_algorithm: typing.Optional[str] = 'best', protein_inference: typing.Optional[str] = 'aggregation', protein_level_fdr_cutoff: typing.Optional[float] = 0.05, protein_quant: typing.Optional[str] = 'unique_peptides', quantification_method: typing.Optional[str] = 'feature_intensity', transfer_ids: typing.Optional[str] = 'false', targeted_only: typing.Optional[bool] = True) -> None:
    """
    nf-core/proteomicslfq

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(pvc_name=pvc_name, input=input, outdir=outdir, email=email, root_folder=root_folder, local_input_type=local_input_type, expdesign=expdesign, database=database, add_decoys=add_decoys, decoy_affix=decoy_affix, affix_type=affix_type, openms_peakpicking=openms_peakpicking, peakpicking_inmemory=peakpicking_inmemory, peakpicking_ms_levels=peakpicking_ms_levels, search_engines=search_engines, enzyme=enzyme, num_enzyme_termini=num_enzyme_termini, allowed_missed_cleavages=allowed_missed_cleavages, precursor_mass_tolerance=precursor_mass_tolerance, precursor_mass_tolerance_unit=precursor_mass_tolerance_unit, fragment_mass_tolerance=fragment_mass_tolerance, fragment_mass_tolerance_unit=fragment_mass_tolerance_unit, fixed_mods=fixed_mods, variable_mods=variable_mods, isotope_error_range=isotope_error_range, instrument=instrument, protocol=protocol, min_precursor_charge=min_precursor_charge, max_precursor_charge=max_precursor_charge, min_peptide_length=min_peptide_length, max_peptide_length=max_peptide_length, num_hits=num_hits, max_mods=max_mods, db_debug=db_debug, enable_mod_localization=enable_mod_localization, mod_localization=mod_localization, allow_unmatched=allow_unmatched, IL_equivalent=IL_equivalent, posterior_probabilities=posterior_probabilities, psm_pep_fdr_cutoff=psm_pep_fdr_cutoff, pp_debug=pp_debug, FDR_level=FDR_level, train_FDR=train_FDR, test_FDR=test_FDR, subset_max_train=subset_max_train, description_correct_features=description_correct_features, outlier_handling=outlier_handling, consensusid_algorithm=consensusid_algorithm, consensusid_considered_top_hits=consensusid_considered_top_hits, min_consensus_support=min_consensus_support, protein_inference=protein_inference, protein_level_fdr_cutoff=protein_level_fdr_cutoff, protein_quant=protein_quant, quantification_method=quantification_method, mass_recalibration=mass_recalibration, transfer_ids=transfer_ids, targeted_only=targeted_only, inf_quant_debug=inf_quant_debug, skip_post_msstats=skip_post_msstats, ref_condition=ref_condition, contrasts=contrasts, enable_qc=enable_qc, ptxqc_report_layout=ptxqc_report_layout)

