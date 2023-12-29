import base64
from io import BytesIO
from matplotlib import pyplot as plt
import requests
import datetime
from pandas import DataFrame
from IPython.display import Image, display

# from config.config import NASA_API_KEY


def return_api_result(url, params):
    """
    URL ve parametrelerle bir HTTP GET isteği yapar ve API'nin yanıtını işler.
    :param url: API URL'si
    :param params: API isteği için parametreler
    """
    r = requests.get(url, params=params) # HTTP GET isteği

    if r.status_code != 200: # HTTP 200 OK yanıtı değilse
        raise requests.exceptions.HTTPError(r.reason, r.url) # Hatayı fırlat
    else: # HTTP 200 OK yanıtı ise
        return r.json() # JSON verilerini döndür


def get_apod_image(api_key, date=None):
    """
    NASA'nın Astronomy Picture of the Day (APOD) API kullanarak bir resim alır ve görüntüler.
    
    Parameters:
    - api_key (str): NASA API anahtarı.
    - date (str): İsteğe bağlı, görüntü tarihi. 'YYYY-MM-DD' formatında olmalıdır.
    
    """
    endpoint = 'https://api.nasa.gov/planetary/apod'

    # API isteği için parametreleri ayarla
    params = {'api_key': api_key}
    if date:
        params['date'] = date

    # API'den veriyi al
    api_result = return_api_result(url=endpoint, params=params)

    # API'den dönen JSON verisini yazdır
    print(api_result)

    # API'den dönen veriyi kontrol et
    if 'url' in api_result:
        image_url = api_result['url']

        # Resmi görüntüle
        image = Image(url=image_url)
        display(image)

        return image
    else:
        return None  # Hata durumunda None döndür
    

def closes_approach(date_min='now', date_max='+60', dist_min=None, dist_max='0.05', h_min=None, h_max=None,
                   v_inf_min=None, v_inf_max=None, v_rel_min=None, v_rel_max=None, orbit_class=None, pha=False,
                   nea=False, comet=False, nea_comet=False, neo=False, kind=None, spk=None, des=None,
                   body='Earth', sort='date', limit=None, fullname=False, return_df=False):
    r"""
    NASA'nın Jet Propulsion Laboratory'nin (JPL) Small-Body Database'deki tüm asteroid ve kuyruklu yıldızlar için
    bilinen yaklaşan geçiş verilerini sağlar.
    
    Parameters
    ----------
    date_min : str, datetime, default 'now'
        Belirtilen tarihten önceki verileri hariç tutar. Varsayılan olarak 'now', yani mevcut tarihi temsil eder, ancak
        aynı zamanda 'YYYY-MM-DD' formatında bir tarih veya 'YYYY-MM-DDThh:mm:ss' formatında bir tarih/saat veya bir
        datetime nesnesi de olabilir.
    date_max :'str, datetime, 'now', default '+60'
        Belirtilen tarihten sonraki verileri hariç tutar. Varsayılan olarak '+60', :code:`tarih_min` parametresinden 60
        gün sonrasını temsil eder. '+D' biçiminde bir dize kabul eder, burada D gün sayısını temsil eder veya 'YYYY-MM-DD'
        formatında bir tarih veya 'YYYY-MM-DDThh:mm:ss' formatında bir tarih/saat veya bir datetime nesnesi olabilir.
        'now' da kabul edilen bir değerdir ve mevcut tarihten sonraki verileri hariç tutar.

    dist_min : str, float, int, default None
        Belirtilen değerden küçük olan yaklaşım mesafesi verilerini hariç tutar (varsa). Varsayılan birim AU (astronomik birim) olup,
        LD (lunar mesafe) de mevcuttur. Örneğin, '0.05' veya 0.05 AU birimleri döndürecektir, '0.05LD' LD birimlerini döndürür.
    dist_max : str, float int, default None
        Belirtilen değerden büyük olan yaklaşım mesafesi verilerini hariç tutar (varsa). Varsayılan birim AU (astronomik birim) olup,
        LD (lunar mesafe) de mevcuttur. Örneğin, '0.05' AU birimlerini döndürecektir, '0.05LD' LD birimlerini döndürür.

    h_min : float, int, default None
        H değeri belirtilen değerden küçük olan nesnelerin verilerini hariç tutar.
    h_max : float, int, default None
        H değeri belirtilen değerden büyük olan nesnelerin verilerini hariç tutar.

    v_inf_min : float, int, default None
        Bu pozitif değerden küçük olan V-sonsuzluk değeri olan verileri hariç tutar (km/s).
    v_inf_max : float, int, default None
        Bu pozitif değerden büyük olan V-sonsuzluk değeri olan verileri hariç tutar (km/s).

    v_rel_min : float, int, default None
        Bu pozitif değerden küçük olan V-relatif değeri olan verileri hariç tutar (km/s).
    v_rel_max : float, int, default None
        Bu pozitif değerden büyük olan V-relatif değeri olan verileri hariç tutar (km/s).

    orbit_class : str
        Verileri belirtilen yörünge(orbit) sınıfına sınırlar.

    pha : bool, default False
        True ise, sonuç verilerini sadece PHA nesnelerine sınırlar.

    nea : bool, default False
        True ise, dönen verileri sadece NEA nesnelerine sınırlar.

    comet : bool, default False
        True ise, dönen verileri sadece kuyruklu yıldız nesnelerine sınırlar.

    nea_comet : bool, default False
        True ise, dönen verileri sadece NEA kuyruklu yıldız nesnelerine sınırlar.

    neo : bool, default False
        True ise, dönen verileri sadece NEO nesnelerine sınırlar.

    kind : str, {'a', 'an', 'au', 'c', 'cn', 'cu', 'n', 'u'}, default None
        Geri dönen verileri belirtilen nesne türüne filtreler. Kullanılabilir seçenekler arasında 'a'=asteroid,
        'an'=numaralandırılmış-asteroidler, 'au'=numaralandırılmamış-asteroidler, 'c'=kuyruklu yıldızlar, 'cn'=numaralandırılmış-kuyruklu yıldızlar,
        'cu'=numaralandırılmamış-kuyruklu yıldızlar, 'n'=numaralandırılmış nesneler ve 'u'=numaralandırılmamış nesneler bulunur.
        
    spk : str, int, default None
        Yalnızca eşleşen SPK-ID için veri döndürür.

    des : str, default None
        Verileri verilen hedeflere eşleşen nesnelerle filtreler.

    body : str, default "Earth"
        Belirtilen cismin yaklaşan geçişlerine filtre uygular. 'ALL' veya '*' tüm mevcut cisimlere yapılan
        yaklaşan geçişleri döndürür.

    sort : str, {'date', 'dist', 'dist-min', 'v-inf', 'v-rel', 'h', 'object'}
        Geri dönen verileri belirtilen alana göre sıralar. Varsayılan olarak 'date' artan olarak sıralanır.
        Azalan olarak sıralamak için, sıralama değerinin önüne '-' ekleyin, örneğin, '-date'.

    limit : int, default None
        Parametre tarafından belirtilen sonuç sayısına göre verileri sınırlar. 0'dan büyük olmalıdır.

    fullname : bool, default False
        Tam biçimli nesne adını/tanımını içerir

    return_df : bool, default False
        True ise, JSON verilerinin 'data' alanını pandas DataFrame olarak döndürür, sütun adlarını
        JSON verilerinin 'fields' anahtarından çıkarır.

    

    Returns
    -------
    dict
        API'den dönen JSON verilerini temsil eden sözlük nesnesi.

    Examples
    --------
    # 2019 yılında tüm yaklaşan nesne verilerini, maksimum yaklaşım mesafesi 0.01AU ile alın.
    >>> close_approach(date_min='2019-01-01', date_max='2019-12-31', dist_max=0.01)
    # Asteroid 433 Eros için 1900 ila 2100 yılları arasındaki 0.2AU'den az olan yaklaşan geçiş verilerini alın.
    >>> close_approach(des='433', date_min='1900-01-01', date_max='2100-01-01', dist_max=0.2)
    # 2000'in başından 2020'nin başına kadar olan yaklaşan geçiş verilerini pandas DataFrame olarak döndürün.
    >>> close_approach(date_min='2000-01-01', date_max='2020-01-01', return_df=True)

    Notes
    -----
    Her yaklaşan geçiş kaydı, aşağıdaki sırayla gelen alanları içeren bir listedir:

    * des - asteroid veya kuyruklu yıldızın birincil adlandırması (örneğin, 443, 2000 SG344)
    * orbit_id - orbit ID
    * jd - yaklaşan geçişin zamanı (JD Ephemeris Time)
    * cd - yaklaşan geçişin zamanı (formatted calendar date/time)
    * dist - nominal yaklaşım mesafesi (au)
    * dist_min - minimum (3-sigma) yaklaşım mesafesi (au)
    * dist_max - maksimum (3-sigma) yaklaşım mesafesi (au)
    * v_rel - yaklaşık geçişte hedefe göre göre hız (km/s)
    * v_inf -  kütlesiz gövdeye göre hız (km/s)
    * t_sigma_f - yaklaşan geçişin zamanındaki 3 sigma belirsizliği (gün, saat ve dakika olarak biçimlendirilmiş;
        sıfırsa günler dahil değildir; örnek "13:02" 13 saat 2 dakika; örnek "2_09:08" 2 gün 9 saat 8 dakika)
    * body - body - yaklaşan geçiş gövdesinin adı (örneğin, Earth)
        * yalnızca body sorgu parametreleri ALL olarak ayarlandığında çıktı verilir
    * h - mutlak büyüklük H (mag)
    * fullname - asteroid veya kuyruklu yıldızın biçimlendirilmiş tam adı/tanımı
        * optional - uygun flag query ile istendiğinde verilir
        * monospace font tablolarındaki sütun hizalaması için önde boşluklarla biçimlendirilmiştir
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