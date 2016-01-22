"""Routines used by WMT hooks for TopoFlow components."""
import string


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
            if env[key] == 'Scalar':
                env[key_root] = env[key_root + '_scalar']
            else:
                env[key_root] = env[key_root + '_file']
                file_list.append(key_root)
            env[key_root + '_dtype'] = get_dtype(env[key_root])
