from cleanTools import *
from config import *
import xlrd


def loadDataSet(fileName: str):
    """
    加载数据集
    :param fileName:
    :return:
    """
    workBook = xlrd.open_workbook(fileName)
    table = workBook.sheets()[0]
    nrows = table.nrows  # 行数

    provinceMap = {}  # 省
    cityMap = {}  # 市
    areaMap = {}  # 区

    provinceToAreaMap = {}  # 省对应区
    cityToAreaMap = {}  # 市对应区

    provinceName = ''
    cityName = ''
    for i in range(2, nrows):
        rowValues = table.row_values(i)

        if rowValues[1][-4:] == '0000':
            provinceName = rowValues[0]
            provinceToAreaMap[rowValues[0]] = {}
        else:
            provinceToAreaMap[provinceName][rowValues[0]] = rowValues[1]

        if rowValues[1][-2:] == '00' and rowValues[1][-4:] != '0000':
            cityName = rowValues[0]
            cityToAreaMap[rowValues[0]] = {}
        else:
            if rowValues[1][-4:] != '0000':
                cityToAreaMap[cityName][rowValues[0]] = rowValues[1]

        if rowValues[1][-4:] == '0000':
            provinceMap[rowValues[0]] = rowValues[1]
        elif rowValues[1][-2:] == '00':
            cityMap[rowValues[0]] = rowValues[1]
        else:
            areaMap[rowValues[0]] = rowValues[1]

    return provinceMap, cityMap, areaMap, provinceToAreaMap, cityToAreaMap


class StringToCode:
    """
    将输入字符串转为准确adcode
    """

    def __init__(self, string, lookahead):
        # 删除全角半角空格
        self.string = inputNormalize(string)
        # 对于省的例外描述清理
        self.string = suffixClean(string)
        # 省市区字典
        self.provinceMap, self.cityMap, self.areaMap, self.provinceToAreaMap, self.cityToAreaMap = loadDataSet(filePath)
        # 一次查看字符串的长度
        self.lookahead = lookahead

        self.adcodeDic = {
            "省": '',
            "市": '',
            "区": ''
        }

    def fullTextExtract(self):
        # 起始位置
        i = 0
        provinceName = ''
        cityName = ''
        while i < len(self.string):

            for length in range(1, self.lookahead + 1):
                if i + length > len(self.string):
                    break

                word = self.string[i:i+length]

                for province in self.provinceMap:
                    provinceC = suffixClean(province)
                    if word == provinceC:
                        self.adcodeDic["省"] = self.provinceMap[province]
                        provinceName = province
                        break

                for city in self.cityMap:
                    if word == city:
                        self.adcodeDic["市"] = self.cityMap[city]
                        cityName = city
                        break

                if provinceName and cityName:
                    for area in self.cityToAreaMap[cityName]:
                        if word == area:
                            self.adcodeDic["区"] = self.cityToAreaMap[cityName][area]
                            break
                elif provinceName:
                    for area in self.provinceToAreaMap[provinceName]:
                        if word == area:
                            self.adcodeDic["区"] = self.provinceToAreaMap[provinceName][area]
                            break
                elif cityName:
                    for area in self.cityToAreaMap[cityName]:
                        if word == area:
                            self.adcodeDic["区"] = self.cityToAreaMap[cityName][area]
                            break
                else:
                    for area in self.areaMap:
                        if word == area:
                            self.adcodeDic["区"] = self.areaMap[area]
                            break
            i += 1

        return self.adcodeDic

    def getAdcode(self):
        mapDic = self.fullTextExtract()
        maxAdcode = max(mapDic.values())
        return maxAdcode


if __name__ == "__main__":
    header = StringToCode('北京市东城区  固安县', 7)
    print(header.fullTextExtract())
    print(header.getAdcode())

