import os
import random

from PIL import Image, ImageDraw, ImageFont, ImageFilter

RANDOM_NUMS = ''.join(map(str, range(10)))
RANDOM_CHARS = ''.join(RANDOM_NUMS)
base_path = os.path.dirname(os.path.dirname(__file__))


def create_validation_code(size=(82, 30),
                           char=RANDOM_CHARS,
                           mode='RGB',
                           bg_color=(255, 255, 255),
                           fg_color=(0, 217, 146),
                           font_type=base_path + '/static/fonts/Arial.ttf',
                           font_size=20,
                           length=4,
                           draw_points=True,
                           point_chance=2,
                           draw_lines=True,
                           line_num=2):
    """
    :param size:图片的大小尺寸 width height
    :param char:允许的字符集合，格式字符串
    :param mode:图片模式 默认RGB
    :param bg_color:背景颜色  默认白色
    :param fg_color:验证码颜色
    :param font_type:验证码字体  默认为Arial.aff
    :param font_size:验证码字体大小
    :param length:验证码数字个数 默认4个
    :param draw_points:是否绘制干扰点
    :param point_chance:干扰点出现的概率
    :param draw_lines:是否绘制干扰线
    :param line_num:干扰线条数 当draw_lines为Ture时有效
    :return:验证码图片和验证码
    """

    width, height = size
    # 创建图形
    img = Image.new(mode=mode, size=size, color=bg_color)
    # 创建画笔
    draw = ImageDraw.Draw(img)

    def get_chars():
        """生成指定长度的字符串"""
        return random.sample(char, length)

    def create_points():
        """绘制干扰点 大小在0-50"""
        chance = min(50, max(0, int(point_chance)))
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 50)
                if tmp > 50 - chance:
                    draw.point((w, h), fill=fg_color)

    def create_str():
        """绘制验证码字符"""
        code_str = get_chars()
        code_str = '%s' % ''.join(code_str)
        print(font_type)
        font = ImageFont.truetype(font_type, font_size)
        font_width, font_height = font.getsize(code_str)
        draw.text(((width - font_width) / 5, (height - font_width) / 4),
                  code_str, font=font, fill=fg_color)
        return code_str

    def create_lines():
        """绘制干扰线"""
        for i in range(line_num):
            begin = (random.randint(0, size[0]), random.randint(0, size[1]))
            end = (random.randint(0, size[0]), random.randint(0, size[1]))
            draw.line((begin, end), fill=fg_color)

    if draw_lines:
        create_lines()
    if draw_points:
        create_points()
    code_str = create_str()
    # 图形扭曲参数
    params = [
        1 - float(random.randint(1, 4) / 100),
        0, 0, 0, 1 - float(random.randint(1, 10) / 100, ),
        float(random.randint(1, 3) / 500),
        0.002,
        float(random.randint(1, 3) / 500)
    ]
    img = img.transform(size, Image.PERSPECTIVE, params)
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, code_str


if __name__ == '__main__':
    img, code_str = create_validation_code()
