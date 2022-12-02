
from docxtpl import DocxTemplate


def execDoc(source, target, context):
    tpl = DocxTemplate(source)
    tpl.render(context=context)
    tpl.save(target)
