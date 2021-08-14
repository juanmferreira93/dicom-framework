CHAR_MAPPING = {
    "00": "NUL",
    "01": "SOH",
    "02": "STX",
    "03": "ETX",
    "04": "EOT",
    "05": "ENQ",
    "06": "ACK",
    "07": "BEL",
    "08": "BS",
    "09": "HT",
    "0a": "LF",
    "0b": "VT",
    "0c": "FF",
    "0d": "CR",
    "0e": "SO",
    "0f": "SI",
    "10": "DLE",
    "11": "DC1",
    "12": "DC2",
    "13": "DC3",
    "14": "DC4",
    "15": "NAK",
    "16": "CYN",
    "17": "ETB",
    "18": "CAN",
    "19": "EM",
    "1a": "SUB",
    "1b": "ESC",
    "1c": "FS",
    "1d": "GS",
    "1e": "RS",
    "1f": "US",
    "127": "DEL",
}

NULL_MAPPING = {
    "00": "",
    "01": "",
    "02": "",
    "03": "",
    "04": "",
    "05": "",
    "06": "",
    "07": "",
    "08": "",
    "09": "",
    "0a": "",
    "0b": "",
    "0c": "",
    "0d": "",
    "0e": "",
    "0f": "",
    "10": "",
    "11": "",
    "12": "",
    "13": "",
    "14": "",
    "15": "",
    "16": "",
    "17": "",
    "18": "",
    "19": "",
    "1a": "",
    "1b": "",
    "1c": "",
    "1d": "",
    "1e": "",
    "1f": "",
    "127": "",
}


def decode(string, mapping="CHAR"):
    encoding = "utf-8"
    errors = "replace"

    try:
        if mapping == "CHAR":
            mapper = CHAR_MAPPING
        elif mapping == "NULL":
            mapper = NULL_MAPPING

        return (
            string.decode(encoding, errors)
            .replace("\x00", mapper["00"])
            .replace("\x01", mapper["01"])
            .replace("\x02", mapper["02"])
            .replace("\x03", mapper["03"])
            .replace("\x04", mapper["04"])
            .replace("\x05", mapper["05"])
            .replace("\x06", mapper["06"])
            .replace("\x07", mapper["07"])
            .replace("\x08", mapper["08"])
            .replace("\x09", mapper["09"])
            .replace("\x0a", mapper["0a"])
            .replace("\x0b", mapper["0b"])
            .replace("\x0c", mapper["0c"])
            .replace("\x0d", mapper["0d"])
            .replace("\x0e", mapper["0e"])
            .replace("\x0f", mapper["0f"])
            .replace("\x10", mapper["10"])
            .replace("\x11", mapper["11"])
            .replace("\x12", mapper["12"])
            .replace("\x13", mapper["13"])
            .replace("\x14", mapper["14"])
            .replace("\x15", mapper["15"])
            .replace("\x16", mapper["16"])
            .replace("\x17", mapper["17"])
            .replace("\x18", mapper["18"])
            .replace("\x19", mapper["19"])
            .replace("\x1a", mapper["1a"])
            .replace("\x1b", mapper["1b"])
            .replace("\x1c", mapper["1c"])
            .replace("\x1d", mapper["1d"])
            .replace("\x1e", mapper["1e"])
            .replace("\x1f", mapper["1f"])
            .replace("\x7f", mapper["127"])
        )
    except:
        return str(string)
