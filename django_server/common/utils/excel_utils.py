from xlrd.sheet import Sheet


class ExcelUtil:

    @classmethod
    def get_row_values(cls, sheet: Sheet, row_index: int, col_start: int, col_end: int, del_crlf=True):
        values = sheet.row_values(row_index, col_start, col_end)
        data = []
        for value in values:
            data.append(cls.format_value(value, del_crlf))
        return data

    @classmethod
    def format_value(cls, value, del_crlf=True):
        if isinstance(value, str):
            value = value.strip()
            if del_crlf:
                value = value.replace("\n", "")
        if isinstance(value, float):
            if int(value * 100) % 100 == 0:
                value = int(value)
            else:
                value = round(value, 2)
        return value

    @classmethod
    def get_value(cls, sheet: Sheet, row_index: int, col_index: int, del_crlf=True):
        """
        获取数据
        :param sheet: sheet页
        :param row_index: 行数下标
        :param col_index: 列数下标
        :param del_crlf: 删除换行符
        """
        value = sheet.cell_value(row_index, col_index)
        if value is None:
            return None
        if isinstance(value, str):
            value.strip()
            if del_crlf:
                value.replace("\n", "")
        return value

    @classmethod
    def get_merge_data(cls, sheet: Sheet, row_index: int, col_index: int):
        """
        获取合并数据
        :param sheet: sheet页
        :param merge_cell_list: 合并列表
        :param row_index: 行数下标
        :param col_index: 列数下标
        """
        merge_cell_list = sheet.merged_cells
        if merge_cell_list is None or len(merge_cell_list) == 0:
            return sheet.cell_value(row_index, col_index)
        cell_value = None
        for (min_row, max_row, min_col, max_col) in merge_cell_list:
            if min_row <= row_index < max_row:
                if min_col <= col_index < max_col:
                    cell_value = cls.get_value(sheet, min_row, min_col)
                    break
                else:
                    cell_value = cls.get_value(sheet, row_index, col_index)
            else:
                cell_value = cls.get_value(sheet, row_index, col_index)
        return cell_value
