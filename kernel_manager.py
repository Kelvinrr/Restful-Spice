from collections import OrderedDict
import glob
import os
import re


def create_kernel_listing(available_missions):
    """
    Take a dict of available missions that include a "root" key that identifies
    the root PATH to a given mission kernel directory and generate the
    lookup table of available metakernels.

    Parameters
    ----------
    available_missions : dict
                         With top level keys being the body and second level
                         keys being the mission

    """
    year_re = re.compile('(\d{4})')
    version_re = re.compile('v[0-9]+')

    meta_kernels = {}
    for body, missions in available_missions.items():
        has_year = False
        meta_kernels[body] = {}
        for mission, root in missions.items():

            # Build the PATHs
            spice_root = root["root"]
            meta_root =  os.path.join(spice_root, 'extras/mk')
            files = glob.glob(meta_root + '/*.tm')
            # Grab the metas in descending order
            meta = OrderedDict([])
            for f in files:
                year = year_re.findall(f)
                if year:
                    has_year = True
                    base = os.path.basename(f)
                    meta.setdefault(year[0], []).append(base)
                else:
                    base = os.path.basename(f)
                    meta.setdefault('all', []).append(base)

            for k, v in meta.items():
                sorted_meta = sorted(v, key=lambda x: re.search('v[0-9]+', x).group(), reverse=True)
                meta[k] = [os.path.join(meta_root, i) for i in sorted_meta]

            meta_kernels[body][mission] = meta
    return meta_kernels
