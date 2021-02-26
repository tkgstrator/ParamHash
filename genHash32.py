import zlib

with open("params-filter-nodup.txt", mode="r") as f:
    with open("param.csv", mode="w") as w:
        for line in f:
            param = line.strip()
            hash = format(zlib.crc32(param.encode("ascii")) & 0xFFFFFFFF, "x")
            param = param.split(".")
            w.write(f"{hash},{param[0]}\n")
