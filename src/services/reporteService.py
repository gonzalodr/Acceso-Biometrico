import re
import csv

from models.reporte     import Reporte
from data.reporteData   import ReporteData
from PySide6.QtCore     import *
from fpdf               import FPDF
from docx               import Document


class ReporteServices:
    def __init__(self):
        self.reporteData = ReporteData()
        
    def insertarReporte(self, reporte: Reporte):
        reporte.fecha_generacion = QDate.currentDate().toString("yyyy-MM-dd")
        return self.reporteData.create_reporte(reporte)
    
    def modificarReporte(self, reporte: Reporte):
        return self.reporteData.update_reporte(reporte)
        
    def eliminarReporte(self, id):
        return self.reporteData.delete_reporte(id)

    def obtenerListaReporte(self, pagina=1, tam_pagina=10, ordenar_por="id", tipo_orden="ASC", busqueda=None):
        return self.reporteData.list_reportes(pagina, tam_pagina, ordenar_por, tipo_orden, busqueda)

    def obtenerReportePorId(self, id):
        return self.reporteData.get_reporte_by_id(id)
    
    def obtenerTodoReporte(self):
        return self.reporteData.obtener_todo_reportes()
    
    def obtener_datos_en_lotes(self, limit=500, **filtros):
        offset = 0
        while True:
            resultado = self.reporteData.obtener_datos_para_reporte(limit=limit, offset=offset, **filtros)
            if not resultado['success']:
                break
            
            lote = resultado['reporte']
            if not lote:
                break

            yield lote
            offset += limit

    def generar_reporte_pdf_por_lotes(self, filename="reporte.pdf", limit=100, **filtros):
        
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=10)
        
        for lote in self.obtener_datos_en_lotes(limit=limit, **filtros):
            pdf.add_page()
            for empleado in lote:
                pdf.cell(200, 10, txt=f"{empleado['nombre']} {empleado['apellidos']} - {empleado['cedula']}", ln=True)
                if 'departamento' in empleado:
                    pdf.cell(200, 10, txt=f"Departamento: {empleado['departamento'].nombre}", ln=True)
                if 'rol' in empleado:
                    pdf.cell(200, 10, txt=f"Rol: {empleado['rol'].nombre}", ln=True)
                if 'justificacion' in empleado:
                    j = empleado['justificacion']
                    pdf.cell(200, 10, txt=f"Justificación: {j.fecha} - {j.motivo} - {j.descripcion}", ln=True)
                if 'asistencia' in empleado:
                    a = empleado['asistencia']
                    pdf.cell(200, 10, txt=f"Asistencia: {a.fecha} - {a.estado_asistencia}", ln=True)
                if 'permisos' in empleado:
                    p = empleado['permisos']
                    pdf.cell(200, 10, txt=f"Permiso: {p.fecha_inicio} a {p.fecha_fin} - {p.tipo}", ln=True)
                pdf.ln(5)

        pdf.output(filename)

    def generar_reporte_docx_por_lotes(self, filename="reporte.docx", limit=100, **filtros):
        doc = Document()
        doc.add_heading("Reporte de Empleados", 0)

        for lote in self.obtener_datos_en_lotes(limit=limit, **filtros):
            for empleado in lote:
                doc.add_heading(f"{empleado['nombre']} {empleado['apellidos']} - {empleado['cedula']}", level=1)
                if 'departamento' in empleado:
                    doc.add_paragraph(f"Departamento: {empleado['departamento'].nombre}")
                if 'rol' in empleado:
                    doc.add_paragraph(f"Rol: {empleado['rol'].nombre}")
                if 'justificacion' in empleado:
                    j = empleado['justificacion']
                    doc.add_paragraph(f"Justificación: {j.fecha} - {j.motivo} - {j.descripcion}")
                if 'asistencia' in empleado:
                    a = empleado['asistencia']
                    doc.add_paragraph(f"Asistencia: {a.fecha} - {a.estado_asistencia}")
                if 'permisos' in empleado:
                    p = empleado['permisos']
                    doc.add_paragraph(f"Permiso: {p.fecha_inicio} a {p.fecha_fin} - {p.tipo}")
                doc.add_paragraph("")

        doc.save(filename)
        
    def generar_reporte_csv_por_lotes(self, filename="reporte.csv", limit=100, **filtros):
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                'Nombre', 'Apellidos', 'Cédula', 
                'Departamento', 'Rol',
                'Justificación', 'Asistencia', 'Permiso'
            ])

            for lote in self.obtener_datos_en_lotes(limit=limit, **filtros):
                for empleado in lote:
                    justificacion   = f"{empleado['justificacion'].fecha} - {empleado['justificacion'].motivo} - {empleado['justificacion'].descripcion}" if 'justificacion' in empleado else ''
                    asistencia      = f"{empleado['asistencia'].fecha} - {empleado['asistencia'].estado_asistencia}" if 'asistencia' in empleado else ''
                    permiso         = f"{empleado['permisos'].fecha_inicio} a {empleado['permisos'].fecha_fin} - {empleado['permisos'].tipo}" if 'permisos' in empleado else ''
                    departamento    = empleado['departamento'].nombre if 'departamento' in empleado else ''
                    rol             = empleado['rol'].nombre if 'rol' in empleado else ''
                    
                    writer.writerow([
                        empleado['nombre'],
                        empleado['apellidos'],
                        empleado['cedula'],
                        departamento,
                        rol,
                        justificacion,
                        asistencia,
                        permiso
                    ])