from app.core.database import SessionLocal
from app.models.academico import Carrera, Laboratorio, Asignatura
from app.models.calidad import UsuarioSGC, DocumentoMatriz, DocumentoRevision, EstadoRevisionEnum
from datetime import date

def poblar_bd():
    db = SessionLocal()
    try:
        # 1. Crear Carreras 
        carrera1 = Carrera(clave="IME", nombre="Ingeniería Mecánica Eléctrica")
        carrera2 = Carrera(clave="ITSE", nombre="Ingeniería en Telecomunicaciones, Sistemas y Electrónica")
        db.add_all([carrera1, carrera2])
        db.commit()

        # 2. Crear Laboratorios
        lab_maq = Laboratorio(codigo="L-ME", nombre="Laboratorio de Máquinas Eléctricas", ubicacion="Nave 1")
        lab_mic = Laboratorio(codigo="L-MIC", nombre="Laboratorio de Microcontroladores", ubicacion="Edificio A")
        db.add_all([lab_maq, lab_mic])
        db.commit()

        # 3. Crear Asignaturas (6to Semestre)
        asig_maq = Asignatura(id_carrera=carrera1.id_carrera, clave="ME-06", nombre="Máquinas Eléctricas", semestre=6)
        asig_mic = Asignatura(id_carrera=carrera2.id_carrera, clave="MIC-06", nombre="Microcontroladores", semestre=6)
        db.add_all([asig_maq, asig_mic])
        db.commit()

        # 4. Crear Usuario SGC (Aprobador)
        jefe_lab = UsuarioSGC(
            nombre_completo="Ing. Coordinador SGC",
            email="coordinador@sgc.unam.mx",
            password_hash="hashed_dummy",
            rol="Coordinador_Calidad"
        )
        db.add(jefe_lab)
        db.commit()

        # 5. Crear Documento ISO 9001
        doc_matriz = DocumentoMatriz(
            codigo_formato="FO-LAB-MIC-01",
            titulo="Manual Operativo y Rúbricas de Microcontroladores",
            id_laboratorio=lab_mic.id_laboratorio,
            id_asignatura=asig_mic.id_asignatura
        )
        db.add(doc_matriz)
        db.commit()

        # 6. Crear Revisión Vigente (Aprobada)
        doc_rev = DocumentoRevision(
            id_documento=doc_matriz.id_documento,
            numero_revision=2,
            estado=EstadoRevisionEnum.Aprobado_Vigente,
            id_aprobo=jefe_lab.id_usuario,
            fecha_emision=date(2026, 1, 15),
            fecha_vigencia=date(2026, 8, 10),
            resumen_modificaciones="Actualización de prácticas para arquitectura AVR y PIC.",
            hash_sha256="8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",
            ruta_almacenamiento_minio="formatos-sgc/FO-LAB-MIC-01_Rev2.pdf"
        )
        db.add(doc_rev)
        db.commit()

        print("¡Datos semilla insertados correctamente!")
    except Exception as e:
        print(f"Error insertando datos: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    poblar_bd()