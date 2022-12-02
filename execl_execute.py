import xlrd
from xlsxtpl.writerx import BookWriter


def write_excel(source, target, payloads):
    """
    操作模板写excel
    :param source:
    :param target:
    :param payloads:
    :return:
    """
    book_writer = BookWriter(source)
    book_writer.set_jinja_globals(dir=dir, getattr=getattr)
    for payload in payloads:
        book_writer.render_sheet(payload)
    book_writer.save(target)


def get_sheet(source):
    xlsx = xlrd.open_workbook(source)
    return xlsx.sheets()
