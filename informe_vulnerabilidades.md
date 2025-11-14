# Informe de Vulnerabilidades - Proyecto Flask BigData

**Fecha de análisis:** 13 de noviembre de 2025  
**Proyecto:** Aplicación Flask para carga de datos CSV  
**Ubicación:** `/home/javier/repos/flask-bigdata-2526/`

---

## Resumen Ejecutivo

Se han identificado **10 vulnerabilidades de seguridad** en el proyecto Flask, de las cuales **3 son críticas** y requieren atención inmediata. El sistema presenta deficiencias significativas en validación de entrada, autenticación y configuración de seguridad.

---

## 🔴 Vulnerabilidades Críticas

### 1. **Sin Validación de Archivos CSV**
- **Ubicación:** `app.py:25`, `app.py:41`
- **Descripción:** Los archivos CSV se procesan directamente sin validación del contenido
- **Riesgo:** Alto - Vulnerable a ataques de injection a través de archivos maliciosos
- **Código afectado:**
  ```python
  df = pd.read_csv(request.files["clientes"])
  df = pd.read_csv(request.files["consumos"])
  ```
- **Impacto:** Potencial ejecución de código arbitrario, corrupción de datos, DoS

### 2. **Conexión MongoDB Insegura**
- **Ubicación:** `app.py:10`
- **Descripción:** Conexión directa a MongoDB sin autenticación visible
- **Riesgo:** Alto - Acceso no autorizado a base de datos
- **Código afectado:**
  ```python
  client = MongoClient("mongodb://server25.fjortega.es:27777/")
  ```
- **Impacto:** Acceso completo a la base de datos, exfiltración de datos

### 3. **Falta de Autenticación/Autorización**
- **Ubicación:** Todo el sistema
- **Descripción:** Sin sistema de autenticación para acceder a funcionalidades
- **Riesgo:** Alto - Cualquier usuario puede acceder y subir archivos
- **Impacto:** Acceso no autorizado, manipulación de datos, uso indebido del sistema

---

## 🟡 Vulnerabilidades Medias

### 4. **Límite de Tamaño Excesivo**
- **Ubicación:** `app.py:6`
- **Descripción:** `MAX_CONTENT_LENGTH = 600MB` es demasiado alto
- **Riesgo:** Medio - Potencial DoS mediante upload de archivos grandes
- **Impacto:** Saturación de recursos, DoS

### 5. **Sin Protección CSRF**
- **Ubicación:** `subida_datos.html:152`
- **Descripción:** Formularios sin tokens CSRF
- **Riesgo:** Medio - Vulnerable a cross-site request forgery
- **Impacto:** Acciones no autorizadas en nombre del usuario

### 6. **Manejo Inadecuado de Errores**
- **Ubicación:** Todo el sistema
- **Descripción:** Errores pueden exponer información interna del sistema
- **Riesgo:** Medio - Divulgación de información sensible
- **Impacto:** Exposición de estructura interna, credenciales, etc.

### 7. **Sin Validación de Datos**
- **Ubicación:** `app.py:30-34`, `app.py:47-51`
- **Descripción:** Datos CSV se insertan directamente sin sanitización
- **Riesgo:** Medio - Riesgo de NoSQL injection
- **Código afectado:**
  ```python
  for record in data:
      record["alumno"] = request.form["alumno"]
      # Sin validación de campos adicionales
  ```

---

## 🟢 Vulnerabilidades Menores

### 8. **Headers de Seguridad Faltantes**
- **Ubicación:** Configuración Flask
- **Descripción:** Sin headers como `X-Content-Type-Options`, `X-Frame-Options`
- **Riesgo:** Bajo - Múltiples vectores de ataque menores
- **Impacto:** XSS, clickjacking, MIME sniffing

### 9. **Sin Rate Limiting**
- **Ubicación:** Configuración de la aplicación
- **Descripción:** Sin límites en frecuencia de uploads
- **Riesgo:** Bajo - Vulnerable a ataques de fuerza bruta
- **Impacto:** DoS, abuso de recursos

### 10. **Configuración de Depuración**
- **Ubicación:** `app.py:64`
- **Descripción:** Modo debug potencialmente habilitado en producción
- **Riesgo:** Bajo - Divulgación de información en caso de error
- **Impacto:** Exposición de información sensible del sistema

---

## Análisis Técnico Detallado

### Validación de Entrada
- **Estado:** ❌ Inexistente
- **Problema:** No se valida tipo, contenido ni estructura de archivos CSV
- **Recomendación:** Implementar validación estricta con bibliotecas especializadas

### Autenticación y Autorización
- **Estado:** ❌ No implementada
- **Problema:** Acceso libre a todas las funcionalidades
- **Recomendación:** Implementar sistema de autenticación robusto

### Configuración de Seguridad
- **Estado:** ⚠️ Deficiente
- **Problema:** Configuraciones por defecto, sin hardening
- **Recomendación:** Aplicar mejores prácticas de configuración Flask

### Base de Datos
- **Estado:** ❌ Insegura
- **Problema:** Conexión sin autenticación, sin validación de datos
- **Recomendación:** Configurar autenticación, validar entradas

---

## Recomendaciones Prioritarias

### 🔥 **Acción Inmediata Requerida**

1. **Implementar validación estricta de archivos**
   - Validar tipo MIME real, no solo extensión
   - Verificar estructura y contenido de CSV
   - Limitar tamaño y número de registros

2. **Configurar autenticación MongoDB**
   - Habilitar authentication en MongoDB
   - Usar variables de entorno para credenciales
   - Implementar conexiones seguras (SSL/TLS)

3. **Añadir sistema de autenticación**
   - Implementar login/logout
   - Control de sesiones
   - Autorización por roles

### 📋 **Acciones a Medio Plazo**

4. **Implementar protección CSRF**
   - Añadir tokens CSRF a formularios
   - Validar tokens en backend

5. **Mejorar manejo de errores**
   - Logging de seguridad
   - Mensajes de error genéricos
   - Monitoreo de excepciones

6. **Configurar headers de seguridad**
   - Content Security Policy
   - X-Frame-Options
   - X-Content-Type-Options

### 🔧 **Mejoras Técnicas**

7. **Optimizar configuraciones**
   - Reducir límite de upload a valores razonables (10-50MB)
   - Configurar rate limiting
   - Deshabilitar debug en producción

8. **Validación y sanitización de datos**
   - Validar estructura de datos antes de inserción
   - Sanitizar entradas del usuario
   - Implementar validación de esquemas

---

## Plan de Mitigación

### Fase 1: Seguridad Crítica (1-2 días)
- [ ] Configurar autenticación MongoDB
- [ ] Implementar validación básica de archivos
- [ ] Añadir autenticación de usuarios

### Fase 2: Protección CSRF (2-3 días)
- [ ] Implementar tokens CSRF
- [ ] Configurar headers de seguridad
- [ ] Mejorar manejo de errores

### Fase 3: Hardening (3-5 días)
- [ ] Optimizar configuraciones
- [ ] Implementar rate limiting
- [ ] Añadir logging de seguridad
- [ ] Pruebas de penetración

---

## Conclusión

El proyecto presenta vulnerabilidades de seguridad **graves** que requieren atención inmediata. La implementación de las recomendaciones de la **Fase 1** es **crítica** antes de cualquier despliegue en producción.

La falta de validación de entrada y autenticación representa un riesgo significativo para la confidencialidad, integridad y disponibilidad del sistema.

---

**Analista:** Sistema de Análisis de Seguridad  
**Contacto:** Para aclaraciones sobre este informe, consulte la documentación técnica del proyecto.