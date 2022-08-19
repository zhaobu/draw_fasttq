#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统计fastq文件中的质量分数分布
"""
__author__ = 'liwei'

from asyncore import read
from cmath import inf
import os
import matplotlib.pyplot as plt
import munch
import numpy as np
import yaml
from Bio import SeqIO
from loguru import logger


class Config:

    def __init__(self, file) -> None:
        self.file = file
        self.raw_data = {}
        # open方法打开直接读出来
        with open(file, 'r', encoding='utf-8') as f:
            # 用load方法转字典
            self.raw_data = yaml.load(f.read(), Loader=yaml.FullLoader)
        self.check()

    def check(self):
        logger.info("配置文件内容为:{}".format(self.raw_data))
        raw_data = self.raw_data
        if not os.path.exists(raw_data['fastq_file']):
            raise ValueError("fastq_file 文件不存在:{}".format(raw_data['fastq_file']))
        if raw_data['result'] == "":
            raise ValueError("result 文件不存在:{}".format(raw_data['result']))
        if len(raw_data["read_line"]) < 1:
            raise ValueError("read_line 配置错误:{}".format(raw_data['read_line']))
        if raw_data["title_name"] == "":
            raise ValueError("title_name 配置错误:{}".format(raw_data['title_name']))
        if raw_data["x_name"] == "":
            raise ValueError("x_name 配置错误:{}".format(raw_data['x_name']))
        if raw_data["y_name"] == "":
            raise ValueError("y_name 配置错误:{}".format(raw_data['y_name']))
        # 字典转对象
        self.data = munch.DefaultMunch.fromDict(raw_data)


class ReadData:

    def __init__(self, read_start: int, read_end: int, data: list) -> None:
        self.read_start = read_start
        self.read_end = read_end
        self.data = data


class FastqData:

    def __init__(self, conf_name) -> None:
        conf = Config(conf_name)
        self.conf = conf.data
        logger.info("配置文件加载成功,conf={}".format(self.conf))
        self.decode_read_data()

    def decode_read_data(self):
        with open(self.conf.fastq_file) as handle:
            record = SeqIO.parse(handle, "fastq")
            index = 0
            logger.info("line information")
            # [[0, 100], [1000, 1100]]
            read_line = self.conf.read_line
            self.read_data = [ReadData(info[0], info[1], []) for info in read_line]

            # 计算要读取到的最大位置
            read_max = read_line[0][1]
            for info in read_line:
                if info[1] > read_max:
                    read_max = info[1]

            for line in record:
                for idx, read_info in enumerate(read_line):
                    read_start, read_end = read_info[0], read_info[1]
                    if index >= read_start and index < read_end:
                        once_more = True
                        phred_nums = line.letter_annotations['phred_quality']
                        # cur_data = munch.Munch(index=index, id=line.id, seq=line.seq, phred_nums=phred_nums)
                        self.read_data[idx].data.append(phred_nums)
                        # p_nums = [10**(qi / (-10.0)) for qi in phred_nums]
                        # logger.info("index={},id={},seq={},phred_nums={},p_nums={}".format(index, line.id, line.seq, phred_nums, p_nums))
                        # logger.info("len(phred_nums)={}".format(len(phred_nums)))
                index += 1
                if index >= read_max:
                    break


class Show:

    def __init__(self, fastq: FastqData) -> None:
        self.read_data = fastq.read_data
        self.conf = fastq.conf
        logger.info("读取到的fastq文件的数据长度为:{}".format(len(self.read_data)))

    def draw_once(self, read_data: ReadData):
        prefix = "{}-{}".format(read_data.read_start, read_data.read_end)
        plt.figure(figsize=(20, 15))

        rows, cols = 2, 1
        # 画所有reads
        self.draw_all_reads(read_data, prefix, rows, cols, 1)

        # plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0, hspace=0.3)
        # 画统计图
        self.draw_statistics(read_data, prefix, rows, cols, 2)

        plt.tight_layout()  # 自动调整各子图间距
        # 保存结果
        # 判断文件是否存在
        result_path = "./result/{}".format(str.split(self.conf.fastq_file, '/')[-1])
        if not os.path.exists(result_path):
            os.mkdir(result_path)
        plt.savefig("{}/{}-{}".format(result_path, prefix, self.conf.result), dpi=500)

    def draw(self):
        for read_data in self.read_data:
            self.draw_once(read_data)

    def draw_statistics(self, read_data: ReadData, prefix: str, rows: int, cols: int, index: int):
        logger.info("开始画统计图")

        ax = plt.subplot(rows, cols, index)
        # 汉字字体，优先使用楷体，找不到则使用黑体
        # plt.rcParams['font.sans-serif'] = ['Kaitt', 'SimHei']
        # 正常显示负号
        # plt.rcParams['axes.unicode_minus'] = False

        x_pos = [x for x in range(150)]
        # 按列求平均值
        arrary = np.array(read_data.data)
        average = np.average(arrary, axis=0)
        ax.plot(x_pos, average, label='average')

        # 按列求最小值
        minimum = np.amin(arrary, axis=0)
        ax.plot(x_pos, minimum, label='minimum')

        # 按列求最大值
        maximum = np.amax(arrary, axis=0)
        ax.plot(x_pos, maximum, label='maximum')

        ddof = 0
        ddof_str = "求的是总体方差和总体标准差"
        prestr = "overall "
        if self.conf.ddof:
            ddof_str = "求的是样本方差和样本标准差"
            ddof = 1
            prestr = "sample "
        logger.info("conf.ddof={},{}".format(self.conf.ddof, ddof_str))

        # 求每一列的方差
        variance = np.var(arrary, axis=0, ddof=ddof)
        ax.plot(x_pos, variance, label=prestr + 'variance')

        # 求每一列的标准差
        standard_deviation = np.std(arrary, axis=0, ddof=ddof)
        ax.plot(x_pos, standard_deviation, label=prestr + 'standard deviation')

        # 先画图后再设置标题,label等
        title_name = "{} {} {}".format(prefix, "statistics", self.conf.title_name)
        title_name = "{}\nfastq file:{}".format(title_name, str.split(self.conf.fastq_file, '/')[-1])
        ax.set_title(title_name, fontsize=20)
        ax.set_xlabel(self.conf.x_name, fontsize=16)
        ax.set_ylabel(self.conf.y_name, fontsize=16)
        ax.legend(fontsize=16, loc="best")  # 设置图表图例在右上角
        plt.tight_layout()

    def draw_all_reads(self, read_data: ReadData, prefix: str, rows: int, cols: int, index: int):
        logger.info("开始画子图所有reads,总数为{}".format(len(read_data.data)))
        ax = plt.subplot(rows, cols, index)
        # 汉字字体，优先使用楷体，找不到则使用黑体
        # plt.rcParams['font.sans-serif'] = ['Kaitt', 'SimHei']
        # 正常显示负号
        # plt.rcParams['axes.unicode_minus'] = False

        x_pos = [x for x in range(150)]

        for info in read_data.data:
            x = x_pos
            y = info
            # x = np.array(x_pos)
            # y = np.array(info)
            # logger.info("len={},{}".format(len(info), info))
            ax.plot(x, y, color='g', lw=0.5)

        # 先画图后再设置标题,label等
        title_name = "{} {} {}".format(prefix, "all reads", self.conf.title_name)
        title_name = "{}\nfastq file:{}".format(title_name, str.split(self.conf.fastq_file, '/')[-1])
        ax.set_title(title_name, fontsize=20)
        ax.set_xlabel(self.conf.x_name, fontsize=16)
        ax.set_ylabel(self.conf.y_name, fontsize=16)
        plt.tight_layout()


def main():
    try:
        fastq_data = FastqData("conf.yml")
        show = Show(fastq_data)
    except Exception as e:
        logger.error("fastq文件数据读取错误:{}".format(e))
    else:
        show.draw()
        logger.debug('执行结束...')


if __name__ == "__main__":
    main()
