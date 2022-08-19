import os

import matplotlib.pyplot as plt
import numpy as np
import pytest
from loguru import logger

import utils
from pathlib import Path

base_path = Path(__file__).parent
file_name = base_path / "data/MGISEQ2000_PCR-free_NA12878_1_V100003043_L01_1.fq"


def test_readfile():
    logger.info("file_name={}".format(file_name))
    data = utils.read_file(file_name, [0, 5])
    logger.info("data={},".format(len(data)))


# def test_draw():
#     data = utils.read_file(file_name, [0, 5])

#     plt.rcParams['font.sans-serif'] = ['SimHei']  #如果title是中文，matplotlib会乱码，这时需要加上下面这段代码
#     plt.title("quality score graph", fontsize=20)

#     x = np.array([x for x in range(150)])
#     y = np.array(data[0])
#     plt.plot(x, y, color='r', lw=2)

#     plt.xlabel("位点", fontsize=16)
#     plt.ylabel("质量值", fontsize=16)
#     plt.show()

#     # =========================================
#     logger.info("画图成功")


def test_draw2():
    logger.info("pwd={}".format(os.path.abspath('.')))
    # =========================================
    data = utils.read_file(file_name, [0, 10])

    plt.figure(figsize=(10, 5))
    x_nums = [x for x in range(150)]
    for y_data in data:
        x = np.array(x_nums)
        y = np.array(y_data)
        plt.plot(x, y, 'g', lw=0.5)

    # =========================================

    # =========================================
    # x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    # y = np.array([13, 25, 17, 36, 21, 16, 10, 15])
    # plt.bar(x, y, 0.2, alpha=0.5, color='r')
    plt.savefig(base_path / 'test_draw2.png', dpi=500)


def test_draw3():
    x = np.arange(0, 100)
    fig = plt.figure()
    ax1 = fig.add_subplot(221)
    ax1.plot(x, x)
    ax2 = fig.add_subplot(222)
    ax2.plot(x, -x)
    ax3 = fig.add_subplot(223)
    ax3.plot(x, x**2)
    ax4 = fig.add_subplot(224)
    ax4.plot(x, np.log(x))
    plt.savefig(base_path / 'test_draw3.png', dpi=500)


def test_draw4():
    plt.figure(figsize=(6, 6.5))
    for i in range(4):
        ax = plt.subplot(221 + i)
        alpha = 0.98 / 4 * i + 0.01
        ax.set_title('%.3f' % alpha)
        t1 = np.arange(0.0, 1.0, 0.01)
        for n in [1, 2, 3, 4]:
            plt.plot(t1, t1**n, label="n=%d" % n)
        leg = plt.legend(loc='best', ncol=4, mode="expand", shadow=True)
        leg.get_frame().set_alpha(alpha)

    plt.savefig(base_path / 'test_draw4.png', dpi=500)


def test_draw5():
    plt.figure(figsize=(6, 6.5))

    plt.rcParams['font.family'] = 'FangSong'  # 设置字体为仿宋
    plt.rcParams['font.size'] = 10  # 设置字体的大小为10
    plt.rcParams['axes.unicode_minus'] = False  # 显示正、负的问题

    # 第一个子图
    ax1 = plt.subplot(221)
    ax1.plot([1, 3, 5, 7], [2, 4, 6, 8], 'c--o', markerfacecolor='r', label='legend1')
    plt.twinx()  # 设置双坐标轴
    ax1.plot([1, 3, 5, 7], [3, 5, 7, 9], 'r-..', markerfacecolor='b', label='legend2')

    ax1.set_title('标题', fontproperties='SimHei', fontsize=20, color='c')  # 为子图添加标题，fontproperties是设置标题的字体，fontsize是设置标题字体的大小，color是设置标题字体的颜色
    ax1.set_xlabel('x轴')  # 为x轴添加标签
    ax1.set_ylabel('y轴')  # 为y轴添加标签
    ax1.legend(loc='upper left')  # 设置图表图例在左上角
    ax1.grid(True)  # 绘制网格
    # 第二个子图
    ax2 = plt.subplot(222)
    ax2.bar([1, 2, 3, 4], [3, 4, 5, 6], color='c')
    ax2.set_title('标题')  # 为子图添加标题
    ax2.set_xlabel('x轴')  # 为x轴添加标签
    ax2.set_ylabel('y轴')  # 为y轴添加标签
    # 第三个子图
    ax3 = plt.subplot(223)
    ax3.scatter([1, 4, 8, 2], [4, 6, 3, 8], color='r')
    ax3.set_title('标题')  # 为子图添加标题
    ax3.set_xlabel('x轴')  # 为x轴添加标签
    ax3.set_ylabel('y轴')  # 为y轴添加标签
    plt.tight_layout()  # 自动调整各子图间距
    plt.savefig(base_path / 'test_draw5.png', dpi=500)


if __name__ == "__main__":
    pytest.main(["-s", __file__])
