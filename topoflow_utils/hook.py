"""Routines used by WMT hooks for TopoFlow components."""
import string
import yaml

import numpy as np


choices_map = {
    'Yes': 1,
    'No': 0
}
units_map = {
    'meters': 'm^2',
    'kilometers': 'km^2'
}


def lowercase_choice(choice):
    """Formats a string for consumption by TopoFlow.

    Parameters
    ----------
    choice : str
      A parameter choice from WMT.

    """
    return string.join(choice.split(), '_').lower()


def get_dtype(parameter_value):
    """Get the TopoFlow data type of a parameter.

    Parameters
    ----------
    parameter_value : object
      An object, a scalar.

    """
    try:
        float(parameter_value)
    except ValueError:
        return 'string'
    else:
        return 'float'


def assign_parameters(env, file_list):
    """Assign values for input parameters in a TopoFlow component.

    A subset of TopoFlow input parameters can take a scalar value, or,
    through an uploaded file, a time series, a grid, or a grid
    sequence. This function assigns such parameters a scalar value, or
    the name of a file, based on the user's selection in WMT.

    Parameters
    ----------
    env : dict
      A dict of component parameter values from WMT.
    file_list : list
      A list of file names used by the component.

    """
    terminator = '_ptype'
    for key in env.copy().iterkeys():
        if key.endswith(terminator):
            key_root, sep, end = key.partition(terminator)
            # if env[key] == 'Scalar':
            #     env[key_root] = env[key_root + '_scalar']
            # else:
            if env[key] != 'Scalar':
                env[key_root] = env[key_root + '_file']
                file_list.append(key_root)
            env[key_root + '_dtype'] = get_dtype(env[key_root])


def load_rti(name):
    """Load a RiverTools RTI file.
    
    Parameters
    ----------
    name : string
        Name of the RTI file.
    
    Returns
    -------
    dict
        Key-value pairs given in the RTI file.
    """
    lines = []
    with open(name, 'r') as fp:
        for line in fp:
            if ';' in line:
                line = line[:line.find(';')]
            if ':' in line:
                lines.append(line)

    return yaml.load(os.linesep.join(lines))


def scalar_to_rtg_file(name, env):
    """Convert a scalar value to an RiverTools RTG file.
    
    Parameters
    ----------
    name : string
        Name of the variable to convert to a grid.
    env : dict
        Mapping of keys to values for the parameter file environment.
    """
    env[name + '_ptype'] = 'Grid'
    env[name + '_dtype'] = 'string'
    file_name = env['case_prefix'] + '_{name}.rtg'.format(name=name)

    rti = load_rti(env['site_prefix'] + '.rti')
    shape = (rti['Number of rows'], rti['Number of columns'])
    byte_order = rti['Byte order']
    if byte_order == 'MSB':
        dtype = '>f4'
    else:
        dtype = '<f4'
    grid = np.full(shape, env[name], dtype=dtype)
    grid.tofile(file_name)

    env[name] = env[name + '_file'] = file_name
