# -*- coding: utf-8 -*-
try:
    import xlwt
except:
    raise ImportWarning("xlwt not installed")
import datetime


__all__ = ('XlsUtil', )


class XlsUtil(object):
    header_style = xlwt.XFStyle()
    header_style.alignment.horz = xlwt.Formatting.Alignment.HORZ_CENTER
    header_style.alignment.vert = xlwt.Formatting.Alignment.VERT_CENTER

    def __init__(self, output_file):
        self.output_file = output_file
        self.book = xlwt.Workbook()

    def save(self):
        self.book.save(self.output_file)

    def add_sheet(self, sheet_name, fields, records):
        """
        新建一个表单
        :param sheet_name: 表单名
        :param fields: 表头
        :param records: 表内容

        表头支持单行和多行表头。其中多行为N维数据
        表头和表内容支持合并单元格, 详情见write_row
        """
        sheet = self.book.add_sheet(sheet_name)
        r_index = 0

        # 处理表头, 支持多行表头
        if isinstance(fields[0], (tuple, list)):
            fields_list = fields
        else:
            fields_list = [fields]

        for fields in fields_list:
            self.write_row(sheet, r_index, fields, self.header_style)
            r_index += 1

        for r in records:
            self.write_row(sheet, r_index, r)
            r_index += 1

    @classmethod
    def write_row(cls, sheet, r_index, r_data, style=xlwt.Style.default_style):
        """
        写入一行数据
        :param sheet: 表单
        :param r_index: 行数(从0开始)
        :param r_data: 行数据

        行数据支持合并单元格, 格式如下:
        [(value, width, height), value]
        width/height表示单元格的宽高, 不填默认为1
        """
        i = 0
        for d in r_data:
            if isinstance(d, (tuple, list)) and len(d) == 3:
                val, width, height = d
            else:
                val, width, height = d, 1, 1

            if val is None:
                i += 1
                continue

            sheet.write_merge(
                r_index,
                r_index + height - 1,
                i,
                i + width - 1,
                cls.convert_value(val),
                style
            )

            i += width

    @staticmethod
    def convert_value(v):
        if isinstance(v, bool):
            v = '是' if v else '否'
        elif isinstance(v, datetime.datetime) or isinstance(v, datetime.date):
            v = v.strftime('%Y-%m-%d')
        return v
