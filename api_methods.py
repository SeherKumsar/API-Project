import requests
import datetime
from pandas import DataFrame

def return_api_result(url, params):
    r = requests.get(url,
                     params=params)

    if r.status_code != 200:
        raise requests.exceptions.HTTPError(r.reason, r.url)

    else:
        return r.json()

def closes_approach(date_min='now', date_max='+60', dist_min=None, dist_max='0.05', h_min=None, h_max=None,
                   v_inf_min=None, v_inf_max=None, v_rel_min=None, v_rel_max=None, orbit_class=None, pha=False,
                   nea=False, comet=False, nea_comet=False, neo=False, kind=None, spk=None, des=None,
                   body='Earth', sort='date', limit=None, fullname=False, return_df=False):
    r"""
    Provides data for currently known close-approach data for all asteroids and comets in NASA's Jet Propulsion
    Laboratory's (JPL) Small-Body Database.

    Parameters
    ----------
    date_min : str, datetime, default 'now'
        Excludes data earlier than the given date. Defaults to 'now', representing the current date, but can also be
        a string representing a date in 'YYYY-MM-DD' format or 'YYYY-MM-DDThh:mm:ss' format or a datetime object.
    date_max :'str, datetime, 'now', default '+60'
        Excludes data later than the given date. Defaults to '+60', representing 60 days after the :code:`date_min`
        parameter. Accepts a string of '+D' where D represents the number of days or a string representing a date in
        'YYYY-MM-DD' format or 'YYYY-MM-DDThh:mm:ss' format or a datetime object. 'now' is also an acceptable value
        and will exclude date later than the current date.
    dist_min : str, float, int, default None
        Excludes data with an approach distance less than the given value (if provided). The default unit is AU
        (astronomical units), and LD (lunar distance) is also available. For example, '0.05' or 0.05 would return
        AU units whereas '0.05LD' would return LD units.
    dist_max : str, float int, default None
        Excludes data with an approach distance greater than the given value (if specified). The default unit is AU
        (astronomical units), and LD (lunar distance) is also available. For example, '0.05' would return AU units
        whereas '0.05LD' would return LD units.
    h_min : float, int, default None
        Exclude data from objects with H-values less than the given value.
    h_max : float, int, default None
        Exclude data from objects with H-values greater than the given value.
    v_inf_min : float, int, default None
        Exclude data with V-infinity less than this positive value in km/s
    v_inf_max : float, int, default None
        Exclude data with V-infinity greater than this positive value in km/s
    v_rel_min : float, int, default None
        Exclude data with V-relative less than this positive value in km/s
    v_rel_max : float, int, default None
        Exclude data with V-relative greater than this positive value in km/s
    orbit_class : str
        Limits data to specified orbit-class
    pha : bool, default False
        If True, limits the resulting data to only PHA objects
    nea : bool, default False
        If True, limits the returned data to only NEA objects
    comet : bool, default False
        If True, limits the returned data to comet objects only
    nea_comet : bool, default False
        If True, limits the returned data to NEA comet objects only
    neo : bool, default False
        If True, limits the returned data to only NEO objects
    kind : str, {'a', 'an', 'au', 'c', 'cn', 'cu', 'n', 'u'}, default None
        Filters returned data to specified type of object. Available options include 'a'=asteroid,
        'an'=numbered-asteroids, 'au'=unnumbered-asteroids, 'c'=comets, 'cn'=numbered-comets, 'cu'=unnumbered-comets,
        'n'=numbered-objects, and 'u'=unnumbered-objects
    spk : str, int, default None
        Return data only for the matching SPK-ID.
    des : str, default None
        Filters data to objects matching the given destination.
    body : str, default "Earth"
        Filters data to close-approaches of the specified body. 'ALL' or '*' returns all close-approaches to the
        available bodies.
    sort : str, {'date', 'dist', 'dist-min', 'v-inf', 'v-rel', 'h', 'object'}
        Sorts the returned data by the specified field. Defaults to 'date' ascending. To sort by descending, add a '-'
        in front of the sort value, for example, '-date'.
    limit : int, default None
        Limit data to the first number of results specified by the parameter. Must be greater than 0.
    fullname : bool, default False
        Includes the full-format object name/designation
    return_df : bool, default False
        If True, returns the 'data' field of the returned JSON data as a pandas DataFrame with column names extracted
        from the 'fields' key of the returned JSON.

    Raises
    ------
    ValueError
        Raised if :code:`h_min` is greater than :code:`h_max`
    ValueError
        Raised if :code:`v_inf_min` parameter is greater than :code:`v_inf_max`
    ValueError
        Raised if :code:`v_rel_min` parameter is greater than :code:`v_rel_max`
    ValueError
        Raised if :code:`limit` parameter is 0 or less.
    TypeError
        Raised if :code:`limit` parameter is not an integer (if specified)
    TypeError
        Raised if :code:`pha` is not boolean (True or False)
    TypeError
        Raised if :code:`nea` is not boolean (True or False)
    TypeError
        Raised if :code:`comet` is not boolean (True or False)
    TypeError
        Raised if :code:`neo` is not boolean (True or False)
    TypeError
        Raised if :code:`fullname` is not boolean (True or False)
    HTTPError
        Raised if the returned status code of the resulting data is not 200 (success)

    Returns
    -------
    dict
        Dictionary object representing the returned JSON data from the API.

    Examples
    --------
    # Get all close-approach object data in the year 2019 with a maximum approach distance of 0.01AU.
    >>> close_approach(date_min='2019-01-01', date_max='2019-12-31', dist_max=0.01)
    # Get close-approach data for asteroid 433 Eros within 0.2AU from the years 1900 to 2100.
    >>> close_approach(des='433', date_min='1900-01-01', date_max='2100-01-01', dist_max=0.2)
    # Return close-approach data from the beginning of 2000 to the beginning of 2020 as a pandas DataFrame.
    >>> close_approach(date_min='2000-01-01', date_max='2020-01-01', return_df=True)

    Notes
    -----
    Each close-approach record is a list containing the following fields in the corresponding order:

    * des - primary designation of the asteroid or comet (e.g., 443, 2000 SG344)
    * orbit_id - orbit ID
    * jd - time of close-approach (JD Ephemeris Time)
    * cd - time of close-approeach (formatted calendar date/time)
    * dist - nominal approach distance (au)
    * dist_min - minimum (3-sigma) approach distance (au)
    * dist_max - maximum (3-sigma) approach distance (au)
    * v_rel - velocity relative to the approach body at close approach (km/s)
    * v_inf - velocity relative to a massless body (km/s)
    * t_sigma_f - 3-sigma uncertainty in the time of close-approach (formatted in days, hours, and minutes;
        days are not included if zero; example “13:02” is 13 hours 2 minutes; example “2_09:08” is 2 days 9 hours 8
        minutes)
    * body - name of the close-approach body (e.g., Earth)
        * only output if the body query parameters is set to ALL
    * h - absolute magnitude H (mag)
    * fullname - formatted full-name/designation of the asteroid or comet
        * optional - only output if requested with the appropriate query flag
        * formatted with leading spaces for column alignment in monospaced font tables

    """
    url = 'https://ssd-api.jpl.nasa.gov/cad.api'

    if date_min != 'now':
        if not isinstance(date_min, (str, datetime.datetime)):
            raise TypeError("date parameter must be a string representing a date in YYYY-MM-DD or YYYY-MM-DDThh:mm:ss "
                            "format, 'now' for the current date, or a datetime object.")

        if isinstance(date_min, datetime.datetime):
            date_min = date_min.strftime('%Y-%m-%dT%H:%M:%S')

    if isinstance(date_max, datetime.datetime):
        date_max = date_max.strftime('%Y-%m-%dT%H:%M:%S')

    if h_min is not None and h_max is not None:
        if h_min > h_max:
            raise ValueError('h_min parameter must be less than h_max')

    if v_inf_min is not None and v_inf_max is not None:
        if v_inf_min > v_inf_max:
            raise ValueError('v_inf_min parameter must be less than v_inf_max')

    if v_rel_min is not None and v_rel_max is not None:
        if v_rel_min > v_rel_max:
            raise ValueError('v_rel_min parameter must be less than v_rel_max')

    if limit is not None:
        if not isinstance(limit, int):
            raise TypeError('limit parameter must be an integer (if specified)')

        elif limit <= 0:
            raise ValueError('limit parameter must be greater than 0')

    if not isinstance(pha, bool):
        raise TypeError('pha parameter must be boolean (True or False)')

    if not isinstance(nea, bool):
        raise TypeError('nea parameter must be boolean (True or False)')

    if not isinstance(comet, bool):
        raise TypeError('comet parameter must be boolean (True or False)')

    if not isinstance(nea_comet, bool):
        raise TypeError('nea_comet parameter must be boolean (True or False)')

    if not isinstance(neo, bool):
        raise TypeError('neo parameter must be boolean (True or False)')

    if not isinstance(fullname, bool):
        raise TypeError('fullname parameter must be boolean (True or False)')

    params = {
        'date-min': date_min,
        'date-max': date_max,
        'dist-min': dist_min,
        'dist-max': dist_max,
        'h-min': h_min,
        'h-max': h_max,
        'v-inf-min': v_inf_min,
        'v-inf-max': v_inf_max,
        'v-rel-min': v_rel_min,
        'v-rel-max': v_rel_max,
        'class': orbit_class,
        'pha': pha,
        'nea': nea,
        'comet': comet,
        'nea-comet': nea_comet,
        'neo': neo,
        'kind': kind,
        'spk': spk,
        'des': des,
        'body': body,
        'sort': sort,
        'limit': limit,
        'fullname': fullname
    }

    r = return_api_result(url=url, params=params)

    if return_df:
        r = DataFrame(r['data'], columns=r['fields'])

    return r