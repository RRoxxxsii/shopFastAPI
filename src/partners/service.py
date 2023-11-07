
class TINValidation:

    @staticmethod
    def _validate_tin_length_ten(tin: str) -> bool:
        total = sum(map(int, tin[:8]))
        modulo = total % 11
        lowest_position_inn = tin % 10
        lowest_position_modulo = modulo % 10
        return lowest_position_modulo == lowest_position_inn

    @staticmethod
    def _validate_tin_length_twelve(tin: str):
        coefficients = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
        coefficients2 = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
        total = sum([coefficients[i] * tin[i] for i in range(len(coefficients))])
        total2 = sum([coefficients2[i] * tin[i] for i in range(len(coefficients2))])
        modulo = total % 11
        modulo2 = total2 % 11
        check_sum = modulo % 10
        check_sum2 = modulo2 % 10
        return check_sum == tin[-2] and check_sum2 == tin[-1]

    @staticmethod
    def validate_tin(tin: str) -> bool:
        if len(tin) == 10:
            return TINValidation._validate_tin_length_ten(tin)
        if len(tin) == 12:
            return TINValidation._validate_tin_length_twelve(tin)
        return False


class TRRCValidation:

    @staticmethod
    def validate_trrc(trrc: str):
        return trrc == 0 or len(trrc) == 9       # Individual Entrepreneurs do not have TRRC
