class Guest:
    def __init__(self, passport, name, country):
        self._passport = passport
        self._name = name
        self._country = country
        self._blacklistedReason = []

    @property
    def passport(self):
        return self._passport

    @property
    def name(self):
        return self._name

    @property
    def country(self):
        return self._country

    def isBlacklisted(self):
        return bool(self._blacklistedReason)

    def blacklist(self, dateReported, reason):
        self._blacklistedReason.append([dateReported, reason])

    def __str__(self):
        result = f"Passport Number: {self._passport}\nName: {self._name}\nCountry: {self._country}\n"

        if self.isBlacklisted():
            for reason in self._blacklistedReason:
                result += f"<< Blacklisted on {reason[0]}, {reason[1]} >>\n"
        return result
