
from docxtpl import DocxTemplate


def exec_docx(source, target, context):
    tpl = DocxTemplate(source)
    tpl.render(context=context)
    tpl.save(target)
