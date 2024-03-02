import random


class VerificationCodeGenerator:
    def generate_otp(self, length: int = 6) -> str:
        otp = ""
        for _ in range(length):
            num = random.randint(1, 9)
            otp += str(num)
        return otp
