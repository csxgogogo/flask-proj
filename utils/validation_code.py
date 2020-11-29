#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import random

from PIL import Image, ImageDraw, ImageFont, ImageFilter

RANDOM_NUMBERS = ''.join(map(str, range(10)))
RANDOM_CHARS = ''.join(RANDOM_NUMBERS)
BASE_PATH = os.path.dirname(os.path.dirname(__file__))


def create_validation_code(size=(82, 30),
                           chars=RANDOM_CHARS,
                           mode="RGB",
                           bg_color=(255, 255, 255),
                           fg_color=(0, 217, 146),
                           font_size=20,
                           font_type=BASE_PATH + "/static/fonts/Arial.ttf",
                           length=4,
                           draw_points=True,
                           point_chance=2,
                           draw_lines=True,
                           line_num=2):
    """
    size: 图片的大小，格式（宽，高）
    chars: 允许的字符集合，格式字符串
    mode: 图片模式，默认为RGB
    bg_color: 背景颜色，默认为白色
    fg_color: 前景色，验证码字符颜色
    font_size: 验证码字体大小
    font_type: 验证码字体，默认为 fonts/Arial.ttf
    length: 验证码字符个数
    draw_points: 是否画干扰点
    point_chance: 干扰点出现的概率，大小范围[0, 50]
    draw_lines: 是否画干扰线
    line_num: 干扰线条数，仅当draw_lines=True时有效
    """

    width, height = size
    # 创建图形
    img = Image.new(mode, size, bg_color)
    # 创建画笔
    draw = ImageDraw.Draw(img)

    def get_chars():
        """生成给定长度的字符串，返回列表格式"""
        return random.sample(chars, length)

    def create_points():
        """绘制干扰点"""
        # 大小限制在[0, 50]
        chance = min(50, max(0, int(point_chance)))
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 50)
                if tmp > 50 - chance:
                    draw.point((w, h), fill=fg_color)

    def create_strs():
        """绘制验证码字符"""
        c_chars = get_chars()
        strs = '%s' % ''.join(c_chars)
        font = ImageFont.truetype(font_type, font_size)
        font_width, font_height = font.getsize(strs)
        draw.text(((width - font_width) / 5, (height - font_height) / 4),
                  strs, font=font, fill=fg_color)
        return strs

    def create_lines():
        """绘制干扰线"""
        for i in range(line_num):
            begin = (random.randint(0, size[0]), random.randint(0, size[1]))
            end = (random.randint(0, size[0]), random.randint(0, size[1]))
            draw.line([begin, end], fill=fg_color)

    if draw_lines:
        create_lines()
    if draw_points:
        create_points()
    strs = create_strs()
    # 图形扭曲参数
    params = [
        1 - float(random.randint(1, 4)) / 100,
        0,
        0,
        0,
        1 - float(random.randint(1, 10)) / 100,
        float(random.randint(1, 3)) / 500,
        0.002,
        float(random.randint(1, 3)) / 500
    ]
    img = img.transform(size, Image.PERSPECTIVE, params)
    # 滤镜，边界加强（阈值更大）
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, strs
