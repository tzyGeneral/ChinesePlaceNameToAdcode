# coding=utf-8
import unicodedata
import re


def inputNormalize(string: str) -> str:
    # 全角转半角
    string = unicodedata.normalize('NFKC', string)
    # 保留汉字，字母，数字，逗号，句号
    string = re.sub(r'[^(\u4e00-\u9fa5a-zA-Z0-9)]', '', string)
    return string


def suffixClean(string: str) -> str:
    # 清理省的描述
    string = string.replace('壮族自治区', '')
    string = string.replace('回族自治区', '')
    string = string.replace('维吾尔自治区', '')
    string = string.replace('自治区', '')
    string = string.replace('特别行政区', '')
    return string

