import sense.AqiConverter as Converter

converter = Converter.AqiConverter()


def test_convert_pm25():

    result = converter.concentration_to_aqi('2.5 ug/m3', 12)

    assert result == 50

    result = converter.concentration_to_aqi('2.5 ug/m3', 13)

    assert result == 53

    result = converter.concentration_to_aqi('2.5 ug/m3', 35)

    assert result == 99


def test_convert_pm10():

    result = converter.concentration_to_aqi('10 ug/m3', 12)

    assert result == 11

    result = converter.concentration_to_aqi('10 ug/m3', 155)

    assert result == 101

    result = converter.concentration_to_aqi('10 ug/m3', 604)

    assert result == 500


def test_out_of_range():

    result = converter.concentration_to_aqi('2.5 ug/m3', 501)

    assert result == 999


def test_bad_pollutant_returns_None():

    result = converter.concentration_to_aqi('Not ug/m3', 501)

    assert result is None
