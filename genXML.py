import os
import sys
import xml.etree.ElementTree as et  # XMLを扱う
import subprocess
import shlex  # バイナリ実行

paramdict = {}
xmlp = et.XMLParser(encoding="utf-8")


def encrypt():
    for file in os.listdir("build"):
        base, ext = os.path.splitext(file)
        if ext in [".xml"]:
            xml = et.parse(f"build/{file}", parser=xmlp)

            for element in xml.iter():
                try:
                    value = element.attrib["Name"]
                    key = filter(lambda x: x == value, paramdict.items())
                    value = paramdict.get(key)
                    if value == None:
                        continue
                    element.attrib["Name"] = value
                except KeyError:
                    continue
                except TypeError:
                    continue
            xml.write(f"build/{file}", encoding="shift_jis")
            command = f"convert batch build/{file}"
            devnull = open("log.txt", "w")
            subprocess.Popen(shlex.split(command), stdout=devnull, stderr=devnull)
            while True:
                try:
                    os.rename(f"build/{file}.byml", f"build/{base}")
                    break
                except FileNotFoundError:
                    continue
                except PermissionError:
                    continue


def decrypt():
    for file in os.listdir("source"):
        base, ext = os.path.splitext(file)
        if ext in [".bprm", ".byml", ".byaml"]:
            command = f"convert batch source/{file}"
            devnull = open("log.txt", "w")
            subprocess.Popen(shlex.split(command), stdout=devnull, stderr=devnull)
            xml = et.parse(f"source/{file}.xml", parser=xmlp)

            for element in xml.iter():
                try:
                    hash = element.attrib["Name"]
                    value = paramdict.get(hash)
                    if value == None:
                        continue
                    element.attrib["Name"] = value
                except KeyError:
                    continue
                except TypeError:
                    continue
            xml.write(f"build/{file}.xml", encoding="shift_jis")


if __name__ == "__main__":
    # 出力用ディレクトリ作成
    if not "build" in os.listdir():
        os.mkdir("build")
    if not "source" in os.listdir():
        os.mkdir("source")
    with open("param.csv", mode="r") as f:
        for line in f:
            line = line.split(",")
            paramdict[line[0]] = line[1].strip()

    print("1: Decrypt BPRM, BYML, BYAML in SOURCE FOLDER")
    print("2: Encrypt XML in BUILD FOLDER")
    while True:
        try:
            type = input()
            if type == "1":
                decrypt()
                break
            if type == "2":
                encrypt()
                break
        except KeyboardInterrupt:
            print("\nBye!")
            sys.exit(1)
