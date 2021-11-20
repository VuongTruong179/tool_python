import sys
import subprocess
import json
import os

def runCMD(command):
    response = []
    try:
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        response = p.stdout.readlines()
        retval = p.wait()
    except Exception as ex:
        writeError(str(ex))
        print("Oops!", str(ex), "occurred.")
    return response


def writeError(error):
    ROOT_DIR = os.path.abspath(os.pardir)
    writeFile('./error.txt', error)


def writeFile(filePath, content):
    try:
        print("Write Fie: " + filePath)
        file = open(filePath, 'a', encoding='utf-8')
        file.write(content + "\n")
        file.close()
    except Exception as ex:
        print("Oops!", str(ex), "occurred.")


def readFile(filePath):
    listContent = []
    try:
        file = open(filePath, 'r')
        listContent = file.readlines()
        # while True:
        #     # Get next line from file
        #     line = file.readline()
        #
        #     # if line is empty
        #     # end of file is reached
        #     if not line:
        #         break
        #     listContent.append(line.strip())
        file.close()
    except Exception as ex:
        print("Oops!", str(ex), "occurred.")
    return listContent


def readFileJson(filePath):
    dictJson = {}
    try:
        open(filePath)
    except IOError:
        saveFileJson(filePath, dictJson)
    try:
        with open(filePath, encoding="utf8") as file:
            data = json.load(file)
            jtopy = json.dumps(data)
            dictJson = json.loads(jtopy)
            file.close()
        return dictJson
    except Exception as ex:
        print("Oops!", str(ex), "occurred.")
        return dictJson



def saveFileJson(filePath, data):
    try:
        with open(filePath, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            file.close()
    except Exception as ex:
        print("Oops!", str(ex), "occurred.")
