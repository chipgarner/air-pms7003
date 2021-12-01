import aqi


class AqiConverter:
    def concentratrion_to_aqi(self, pollutant, concentration):
        if '2.5' in pollutant:
            pollutant = aqi.POLLUTANT_PM25
        elif '10' in pollutant:
            pollutant = aqi.POLLUTANT_PM10

        try:
            intermediate_air_quality = aqi.to_iaqi(pollutant, concentration, aqi.ALGO_EPA)
        except IndexError:
            intermediate_air_quality = 999

        if intermediate_air_quality is not None:
            intermediate_air_quality = int(intermediate_air_quality)
        return intermediate_air_quality
