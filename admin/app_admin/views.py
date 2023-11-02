import datetime
from distutils.log import error
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from django.contrib.auth.models import User, Group
from datetime import date
from django.db.models import Q
import requests

@api_view(['GET'])
def getDocente(request, idUsuario = None):
    infoDocente = requests.get("http://127.0.0.1:8001/docente/%s" % idUsuario).json()
    serializer = DocenteSerializer(infoDocente)
    return Response(serializer.data)

# Vista que retorna el docente, dado su id de usuario.
@api_view(['GET'])
def getJefeCarrera(request, idUsuario = None):
    infoJefe = Jefe_Carrera.objects.filter(id_usuario__id = idUsuario).first()
    serializer = JefeCarreraSerializer(infoJefe)
    return Response(serializer.data)

# Vista que retorna el coordinador, dado su id de usuario.
@api_view(['GET'])
def getCoordinador(request, idUsuario = None):
    infoCoordinador = requests.get("http://127.0.0.1:8002/coordinador/%s" % idUsuario).json()
    serializer = CoordinadorSerializer(infoCoordinador)
    return Response(serializer.data)

# Vista que retorna el estudiante, dado su id de usuario.
@api_view(['GET'])
def getIdEstudiante(request, idUsuario = None):
    infoEstudiante = requests.get("http://127.0.0.1:8000/estudiante/%s" % idUsuario).json()
    print(infoEstudiante)
    serializer = EstudianteSerializer(infoEstudiante)
    return Response(serializer.data)

@api_view(['GET'])
def getCalificacionesEstudiante(request, idUsuario = None):
    calificaciones = Calificacion.objects.filter(id_estudiante__id_usuario = idUsuario, id_evaluacion__id_coordinacion__id_semetre__isActual = True).all().order_by('-fecha_entrega')
    serializer = CalificacionSerializer(calificaciones, many = "true")
    return Response(serializer.data)

@api_view(['GET'])
def getDataAsignatura(request, codigo = None, idUsuario = None):

    ## Buscar la coordinacion del curso de teoria con el codigo y id del usuario - verificar que existe seccion del estudiante
    ids_coordinacion = Coordinacion_Estudiante.objects.filter(id_coordinacion__id_asignatura__codigo = codigo, id_coordinacion__id_asignatura__componente = "T", id_estudiante__id_usuario = idUsuario).values_list('id_coordinacion__id',flat=True)
    if ids_coordinacion.count() != 0:

        ## Evaluaciones con calificaciones
        calificaciones = Calificacion.objects.filter(id_evaluacion__id_coordinacion__id_asignatura__codigo = codigo, id_evaluacion__id_coordinacion__id_asignatura__componente = "T", id_estudiante__id_usuario__id = idUsuario).all()
        serializer = CalificacionSerializer(calificaciones, many="true")

        ## Calificaciones con solicitudes segun asignaturas de Teoria del estudiante
        idsCalificacionSolicitudes =  calificaciones.values_list('id',flat=True) ## Obtener ids de las calificaciones existentes
        idsCalificacionesConSolicitudes = [] # Arreglo a devolver
        
        for id in idsCalificacionSolicitudes:
            solicitudes = requests.get("http://127.0.0.1:8003/solicitud_C/%s" % id).json()
            #solicitud = Solicitud_Revision.objects.filter(id_calificacion = id).values_list('id_calificacion', flat=True) # buscar si existe esa calificacion en alguna solicitud
            for solicitud in solicitudes:
                if solicitud["id_calificacion"] == id:
                    idsCalificacionesConSolicitudes.append(solicitud[0]) # Si existe se añade
                    break
        

        ##Evaluaciones sin evaluar
        #Este pendiente, sea de la asignatura y de una seccion en especifico y de teoria
        evaluacionesSinNota = Evaluacion.objects.filter(estado = 'P',id_coordinacion__id_asignatura__codigo = codigo,id_coordinacion = ids_coordinacion[0],id_coordinacion__id_asignatura__componente = "T")
        serializerEvaluaciones = EvaluacionEspecificaSerializer(evaluacionesSinNota, many = 'true')

        ## Informacion correspodiente a los docente de dicho curso
        informacionDocente = Coordinacion_Docente.objects.filter(id_coordinacion__id_asignatura__codigo = codigo, id_coordinacion__id_asignatura__componente = "T", id_coordinacion = ids_coordinacion[0]).all()
        serializerInformacionDocente = DocenteCursoSerializer(informacionDocente, many="true")


        ## Respuesta si existe coordinacion 
        return Response([serializer.data,serializerEvaluaciones.data, idsCalificacionesConSolicitudes, serializerInformacionDocente.data])
    else: ## No existe seccion por lo que no tiene curso de teoria
        return Response([[],[],[],[]])

    

@api_view(['GET'])
def getDataAsignaturaLab(request, codigo = None, idUsuario = None):
    ## Buscar la coordinacion del curso de teoria con el codigo y id del usuario - verificar que existe seccion del estudiante
    ids_coordinacion = Coordinacion_Estudiante.objects.filter(id_coordinacion__id_asignatura__codigo = codigo, id_coordinacion__id_asignatura__componente = "L", id_estudiante__id_usuario = idUsuario).values_list('id_coordinacion__id',flat=True)
    if ids_coordinacion.count() != 0:

        ## Evaluaciones con calificaciones
        calificaciones = Calificacion.objects.filter(id_evaluacion__id_coordinacion__id_asignatura__codigo = codigo, id_evaluacion__id_coordinacion__id_asignatura__componente = "L", id_estudiante__id_usuario__id = idUsuario).all()
        serializer = CalificacionSerializer(calificaciones, many="true")

        ## Calificaciones con solicitudes segun asignaturas de Teoria del estudiante
        idsCalificacionSolicitudes =  calificaciones.values_list('id',flat=True) ## Obtener ids de las calificaciones existentes
        idsCalificacionesConSolicitudes = [] # Arreglo a devolver
        for id in idsCalificacionSolicitudes:
            solicitudes = requests.get("http://127.0.0.1:8003/solicitud_C/%s" % id).json()
            #solicitud = Solicitud_Revision.objects.filter(id_calificacion = id).values_list('id_calificacion', flat=True) # buscar si existe esa calificacion en alguna solicitud
            for solicitud in solicitudes:
                if solicitud["id_calificacion"] == id:
                    idsCalificacionesConSolicitudes.append(solicitud[0]) # Si existe se añade
                    break

        ##Evaluaciones sin evaluar
        #Este pendiente, sea de la asignatura y de una seccion en especifico y de lab
        evaluacionesSinNota = Evaluacion.objects.filter(estado = 'P',id_coordinacion__id_asignatura__codigo = codigo,id_coordinacion = ids_coordinacion[0],id_coordinacion__id_asignatura__componente = "L")
        serializerEvaluaciones = EvaluacionEspecificaSerializer(evaluacionesSinNota, many = 'true')

        ## Informacion correspodiente a los docente de dicho curso
        informacionDocente = Coordinacion_Docente.objects.filter(id_coordinacion__id_asignatura__codigo = codigo, id_coordinacion__id_asignatura__componente = "L", id_coordinacion = ids_coordinacion[0]).all()
        serializerInformacionDocente = DocenteCursoSerializer(informacionDocente, many="true")


        ## Respuesta si existe coordinacion 
        return Response([serializer.data,serializerEvaluaciones.data, idsCalificacionesConSolicitudes, serializerInformacionDocente.data])
    else: ## No existe seccion por lo que no tiene curso de lab
        return Response([[],[],[],[]])

    

# Informacion para la apelacion de un estudiante
@api_view(['GET'])
def getDataSolicitudApelacion(request, idCalificacion = None):
    calificaciones = Calificacion.objects.filter(id = idCalificacion).all()
    serializer = CalificacionSerializer(calificaciones, many = "true")
    return Response(serializer.data)

# Solicitudes de revisión realizadas por un estudiante.
@api_view(['GET', 'PUT' ,'POST'])
def dataSolicitud(request, idUsuario = None, idSolicitud = None):
    if request.method == 'GET':
        #solicitudes = Solicitud_Revision.objects.filter(id_estudiante__id_usuario__id = idUsuario).all().order_by('fecha_creacion')
        estudiante = requests.get("http://127.0.0.1:8000/estudiante/%s" % idUsuario).json()
        estudiante = EstudianteSerializer(estudiante)
        solicitudes = requests.get("http://127.0.0.1:8003/solicitud_E/%s" % estudiante.id).json()
        serializer = SolicitudSerializer(solicitudes, many = "true")
        return Response(serializer.data)
    
    if request.method == 'PUT':
        #solicitud = Solicitud_Revision.objects.filter(id = idSolicitud).first()
        solicitud = requests.get("http://127.0.0.1:8003/solicitud_I/%s" % idSolicitud).json()
        solicitud = OnlySolicitudSerializer(solicitud)
        solicitud_actualizada = OnlySolicitudSerializer(solicitud, data = request.data)
        if solicitud_actualizada.is_valid():
            #solicitud_actualizada.save()
            requests.put("http://127.0.0.1:8003/solicitud/update/%s" % idSolicitud, data= solicitud_actualizada.data)
            return Response(solicitud_actualizada.data)
        return Response(solicitud_actualizada.errors)

    if request.method == 'POST':
        nuevaSolicitud = OnlySolicitudSerializer(data = request.data)
        if nuevaSolicitud.is_valid():
            nuevaSolicitud.save()
            return Response(nuevaSolicitud.data)
        return Response(nuevaSolicitud.errors)

@api_view(['GET'])
def getCursosByEstudiante(request, idUsuario = None):
    cursos = Coordinacion_Estudiante.objects.filter(id_estudiante__id_usuario__id = idUsuario).distinct('id_coordinacion__id_asignatura__codigo')
    serializer = CoordinacionEstudianteSerializer(cursos, many="true")
    return Response(serializer.data)

@api_view(['GET'])
def getCursosByDocente(request, idUsuario = None):
    ## Se cambio de order_by a distinct por bloque de horario para cursos espejo
    cursosDocente = Coordinacion_Docente.objects.filter(id_docente__id_usuario__id = idUsuario, id_coordinacion__isActive = True).distinct('id_coordinacion__bloques_horario')
    serializer = CoordinacionDocenteSerializer(cursosDocente, many="true")
    return Response(serializer.data)

## Obtener informacion para realizar la respuesta a una apelacion
## ID estudiante - ID evaluacion - 
@api_view(['GET'])
def getDataSolicitudRespuesta(request,idEstudiante = None, idEvaluacion = None):
    ## Solicitud segun ID estudiante y ID evaluacion
    #solicitudes = Solicitud_Revision.objects.filter(id_estudiante__id = idEstudiante, id_evaluacion__id = idEvaluacion).all()
    solicitudes = requests.get("http://127.0.0.1:8003/solicitud_EE/%s/%s" % idEstudiante %idEvaluacion).json()
    serializer = SolicitudRespuestaSerializer(solicitudes, many = "true")
    return Response(serializer.data)

## ACtualizacion de calificaciones de una solicitud
@api_view(['GET','PUT'])
def actualizacionCalificacionEstudiante(request, idCalificacion = None):

    if request.method == 'GET':
        calificacion = Calificacion.objects.all()
        calificacions = CalificacionEspecificaSerializer(calificacion, many = "true")
        return Response(calificacions.data)
    
    if request.method == 'PUT':
        ### ID de calificacion a modificar Prueba 2
        calificacion = Calificacion.objects.filter(id = idCalificacion).first()
        calificacion_actualizada = CalificacionEspecificaSerializer(calificacion, data = request.data)
        if calificacion_actualizada.is_valid():
            calificacion_actualizada.save()
            return Response(calificacion_actualizada.data)
        return Response(calificacion_actualizada.errors)
    
# Obtiene los estudiantes que estan inscitos en una coordinacion. 
# Se cargan en la vista de subir calificaciones.
@api_view(['GET'])
def getCalifiacionesEstudiantes(request, idCoordinacion = None):
    calificacionEstudiantes = Coordinacion_Estudiante.objects.filter(id_coordinacion__id = idCoordinacion).all()
    serializer = CoordinacionEstudianteSerializer(calificacionEstudiantes, many="true")
    return Response(serializer.data)    

@api_view(['GET', 'DELETE', 'POST', 'PUT']) ## Mostrar evaluaciones a jefe de carrera
def evaluacionesCoordinacion(request, idEvaluacion = None, idCoordinacion = None):

    # Funcionando.
    if request.method == 'GET':
        evaluacionCoordinacion = Evaluacion.objects.filter(id_coordinacion__id = idCoordinacion).all().order_by('nombre')
        serializer = EvaluacionSerializer(evaluacionCoordinacion, many = "true")
        return Response(serializer.data)
    
    # Funcionando correctamente.
    if request.method == 'DELETE':
        evaluacion = Evaluacion.objects.filter(id = idEvaluacion).first()
        evaluacion.delete()
        return Response(status=status.HTTP_200_OK)

    # Funcionando correctamente.
    if request.method == 'POST':
        evaluacionAgregada = PostEvaluacionSerializer(data = request.data)
        if evaluacionAgregada.is_valid():
            evaluacionAgregada.save()
            return Response(evaluacionAgregada.data)
        return Response(evaluacionAgregada.errors)
    
    # Funcionando correctamente. Modificar una evaluacion.
    if request.method == 'PUT':
        evaluacion = Evaluacion.objects.get(id = idEvaluacion)
        evaluacion_actualizada = EvaluacionEspecificaSerializer(evaluacion, data = request.data)
        if evaluacion_actualizada.is_valid():
            evaluacion_actualizada.save()
            return Response(evaluacion_actualizada.data)
        return Response(evaluacion_actualizada.errors)

@api_view(['GET'])
def getTiposEvaluaciones(request):
    tiposEvaluaciones = Tipo_Evaluacion.objects.all()
    serializer = TipoEvaluacionSerializer(tiposEvaluaciones, many="true")
    return Response(serializer.data)

# Arreglar esta vista para que entregue las coordinaciones con los profesores agrupados (2 o más profesores). ## Solucionado
# Saber que coordinacion quiere visualizar, de aqui sacar el id para ver la tabla Solicitud -> CursoInscrito
@api_view(['GET'])
def getCoordinacionesCoordinador(request, idCoordinador = None):
    coordinacionesCoordinador = Coordinacion_Docente.objects.filter(id_coordinacion__id_asignatura__id_coordinador = idCoordinador)
    idsCoordinacion = Coordinacion_Docente.objects.filter(id_coordinacion__id_asignatura__id_coordinador = idCoordinador).distinct('id_coordinacion__id').values_list('id_coordinacion__id', flat=True)
    #Arreglo donde cada espacio es una seccion de una asignatura
    arregloInformacion = []
    for id in idsCoordinacion:
        coordinacion_docentes = Coordinacion_Docente.objects.filter(id_coordinacion__id = id)
        arregloInformacion.append(DocenteCursoSerializer(coordinacion_docentes, many="true").data)
    #serializer = DocenteCursoSerializer(coordinacionesCoordinador, many="true")
    return Response(arregloInformacion)

@api_view(['GET'])
def getCoordinacionesAsignatura(request, idAsignatura = None):
    coordinacionesAsignatura = Coordinacion_Docente.objects.filter(id_coordinacion__id_asignatura__id = idAsignatura).distinct('id_coordinacion')
    serializer = DocenteCursoSerializer(coordinacionesAsignatura, many = "true")
    return Response(serializer.data)

## LUego de especificar la seccion se recogen las solicitudes de este curso-seccion id para ver la tabla Solicitud -> CursoInscrito
@api_view(['GET'])
def getSolicitudesCurso(request, idCoordinacion = None):
    
    ### ID de cursoInscrito o Coordinacion Seccion
    solicitudesCurso = Solicitud_Revision.objects.filter(id_evaluacion__id_coordinacion = idCoordinacion).all()
    
    serializer = SolicitudesDocenteCursoSerializer(solicitudesCurso, many="true")
    return Response(serializer.data)

## Asignaturas de un jefe de carrera
@api_view(['GET'])
def getAsignaturasJefeCarrera(request, idJefe = None):
    ### ID jefe de carrera, se mostraran sus asignaturas
    planesEstudio = Asignaturas_PlanEstudio.objects.filter(id_planEstudio__id_carrera__id_jefeCarrera = idJefe).distinct('id_asignatura').all()
    
    serializer = PlanesJefeSerializer(planesEstudio, many="true")
    return Response(serializer.data)

## Solicitudes de una asignatura (Jefe de carrera)
@api_view(['GET'])
def getSolicitudesAsignaturaJefeCarrera(request, idAsignatura = None):
    ## ID asignatura seleccionado jefe de carrera
    solicitudes = Solicitud_Revision.objects.filter(id_evaluacion__id_coordinacion__id_asignatura__id = idAsignatura).all()    
    serializer = SolicitudSerializer(solicitudes, many="true")
    ## Coordinaciones disponibles
    coordinaciones = Solicitud_Revision.objects.filter(id_evaluacion__id_coordinacion__id_asignatura__id = idAsignatura).values_list('id_evaluacion__id_coordinacion__coordinacion',flat= True).distinct()
    ## Secciones disponibles
    secciones = Solicitud_Revision.objects.filter(id_evaluacion__id_coordinacion__id_asignatura__id = idAsignatura).values_list('id_evaluacion__id_coordinacion__seccion',flat= True).distinct()
    return Response([serializer.data,coordinaciones,secciones])
    
@api_view(['GET'])
def getAllEvaluaciones(request, idCoordinacion = None):
    evaluacionCoordinacion = Evaluacion.objects.filter(id_coordinacion__id = idCoordinacion).all().order_by('nombre')
    serializer = EvaluacionEspecificaSerializer(evaluacionCoordinacion, many = "true")
    return Response(serializer.data)

@api_view(['GET'])
def getEvaluacionesPorNombre(request, nombreEvaluacion = None, idAsignatura = None):
    evaluaciones = Evaluacion.objects.filter(id_coordinacion__id_asignatura__id = idAsignatura, nombre = nombreEvaluacion).all()
    serializer = EvaluacionEspecificaSerializer(evaluaciones, many = "true")
    return Response(serializer.data)

@api_view(['GET'])
def getRolesUsuarios(request):
    roles = Group.objects.all()
    serializer = RolesSerializers(roles, many = "true")
    return Response(serializer.data)

@api_view(['POST'])
def isRolUser(request):

    if User.objects.filter(username = request.data.get('nombreUsuario'), groups = request.data.get('idRolSeleccionado')).exists():
        usuarioExiste = User.objects.filter(username = request.data.get('nombreUsuario')).first()
        serializer = UsuariosSerializers(usuarioExiste)
        return Response(serializer.data)
    return Response(error)

@api_view(['POST'])
def calificacionesEstudiantes(request):
    calificacion = CalificacionEspecificaSerializer(data = request.data)
    if calificacion.is_valid():
        calificacion.save()
        return Response(calificacion.data)
    return Response(calificacion.errors)

# Obtener los datos de una evaluación en particular. Cambiar el estado de una evaluacion.
@api_view(['GET', 'PUT'])
def crudOneEvaluacion(request, idEvaluacion = None):
    
    if request.method == 'GET':
        test = Evaluacion.objects.filter(id = idEvaluacion).first()
        serializer = PostEvaluacionSerializer(test)
        return Response(serializer.data)

@api_view(['GET'])
def getSolicitudesByIdDocente(request, idDocente):
    solicitudes = Solicitud_Revision.objects.filter(id_docente__id = idDocente).order_by('fecha_creacion')
    serializer = SolicitudSerializer(solicitudes, many="true")
    return Response(serializer.data)

@api_view(['GET'])
def getCalificaionesByDocente(request,  idEvaluacion):
    calificaciones = Calificacion.objects.filter(id_evaluacion__id = idEvaluacion).all().order_by('id_estudiante__rut')
    serializer = CalificacionSerializer(calificaciones, many = "true")
    return Response(serializer.data)

@api_view(['PUT'])
def updateCalificacion(request, idCalificacion):
    calificacion = Calificacion.objects.get(id = idCalificacion)
    calificacion_actualizada = CalificacionEspecificaSerializer(calificacion, data = request.data)
    if calificacion_actualizada.is_valid():
        calificacion_actualizada.save()
        return Response(calificacion_actualizada.data)
    return Response(calificacion_actualizada.errors)

@api_view(['GET','POST'])
def addCambioNota(request, idAsignatura = None):
    
    if request.method == 'GET':
        ## Devolver los cambios
        cambios = Cambio_nota.objects.all()
        serializer = CambioNotaSerializer(cambios, many = "true")
        ## Coordinaciones disponibles
        #coordinaciones = Cambio_nota.objects.values_list('id_calificacion__id_evaluacion__id_coordinacion__coordinacion',flat= True).distinct()
        ## Secciones disponibles
        #secciones = Cambio_nota.objects.values_list('id_calificacion__id_evaluacion__id_coordinacion__seccion',flat= True).distinct()
        #return Response([serializer.data,coordinaciones, secciones])
        return Response(serializer.data)

    if request.method == 'POST':
        CambioAgregado = CambioNotaEspecificaSerializer(data = request.data)
        if CambioAgregado.is_valid():
            CambioAgregado.save()
            return Response(CambioAgregado.data)
        return Response(CambioAgregado.errors)

# obtener los cambios segun una asignatura
@api_view(['GET'])
def getCambioNota_idAsignatura(request,idAsignatura = None):
    
    if request.method == 'GET':
        ## Devolver los cambios 
        cambios = Cambio_nota.objects.filter(id_calificacion__id_evaluacion__id_coordinacion__id_asignatura__id = idAsignatura)
        serializer = CambioNotaSerializer(cambios, many = "true")
        ## Coordinaciones disponibles
        coordinaciones = Cambio_nota.objects.filter(id_calificacion__id_evaluacion__id_coordinacion__id_asignatura__id = idAsignatura).values_list('id_calificacion__id_evaluacion__id_coordinacion__coordinacion',flat= True).distinct()
        ## Secciones disponibles
        secciones = Cambio_nota.objects.filter(id_calificacion__id_evaluacion__id_coordinacion__id_asignatura__id = idAsignatura).values_list('id_calificacion__id_evaluacion__id_coordinacion__seccion',flat= True).distinct()
        return Response([serializer.data,coordinaciones, secciones])

@api_view(['POST'])
def cambioFechaCalificacion(request):
    cambioFecha = CambioFechaSerializer(data = request.data)
    if cambioFecha.is_valid():
        cambioFecha.save()
        return Response(cambioFecha.data)
    return Response(cambioFecha.errors)

@api_view(['POST'])
def addCambioPonderacion(request):
    cambioPonderacion = CambioPonderacionSerializer(data = request.data)
    if cambioPonderacion.is_valid():
        cambioPonderacion.save()
        return Response(cambioPonderacion.data)
    return Response(cambioPonderacion.errors)

@api_view(['GET'])
def getCambiosNota(request, idCoordinador = None):
    cambiosNota = Cambio_nota.objects.filter(id_calificacion__id_evaluacion__id_coordinacion__id_asignatura__id_coordinador__id_usuario = idCoordinador)
    serializer = CambioNotaDashboardSerializer(cambiosNota, many="true")
    return Response(serializer.data)

@api_view(['GET'])
def informacionCoordinacion(request, idCoordinacion = None):
    coordinacion = Coordinacion_Seccion.objects.filter(id = idCoordinacion).all()
    serializer = CoordinacionSeccionSerializer(coordinacion, many = "true")
    return Response(serializer.data)

# Get de los cambios de ponderaciones segun jefe de carrera
@api_view(['GET'])
def getCambioPonderaciones(request, idAsignatura = None):
    cambiosPonderaciones = Cambio_Ponderacion.objects.filter(id_evaluacion__id_coordinacion__id_asignatura__id = idAsignatura)
    serializer = CambioPonderacionesJefe(cambiosPonderaciones, many = "true")
    ## Coordinaciones disponibles
    coordinaciones = Cambio_Ponderacion.objects.filter(id_evaluacion__id_coordinacion__id_asignatura__id = idAsignatura).values_list('id_evaluacion__id_coordinacion__coordinacion',flat= True).distinct()
    ## Secciones disponibles
    secciones = Cambio_Ponderacion.objects.filter(id_evaluacion__id_coordinacion__id_asignatura__id = idAsignatura).values_list('id_evaluacion__id_coordinacion__seccion',flat= True).distinct()
    return Response([serializer.data,coordinaciones,secciones])

# Get cambios de fecha segun jefe de carrera
@api_view(['GET'])
def getCambioFecha(request, idAsignatura = None):
    cambiosPonderaciones = Cambio_Fecha.objects.filter(id_evaluacion__id_coordinacion__id_asignatura__id = idAsignatura)
    serializer = CambioFechaDashboardSerializer(cambiosPonderaciones, many = "true")
    ## Coordinaciones disponibles
    coordinaciones = Cambio_Fecha.objects.filter(id_evaluacion__id_coordinacion__id_asignatura__id = idAsignatura).values_list('id_evaluacion__id_coordinacion__coordinacion',flat= True).distinct()
    ## Secciones disponibles
    secciones = Cambio_Fecha.objects.filter(id_evaluacion__id_coordinacion__id_asignatura__id = idAsignatura).values_list('id_evaluacion__id_coordinacion__seccion',flat= True).distinct()
    return Response([serializer.data,coordinaciones,secciones])


## LUego de especificar la seccion se recogen los cambios de notas de este curso-seccion id para VISTA COORDINADOR
@api_view(['GET'])
def getCambioNotaCurso(request, idCurso = None):
    ### ID de cursoInscrito o Coordinacion Seccion
    cambioNotasCurso = Cambio_nota.objects.filter(id_calificacion__id_evaluacion__id_coordinacion = idCurso).all()
    serializer = CambioNotaDashboardSerializer(cambioNotasCurso, many="true")
    return Response(serializer.data)

@api_view(['GET'])
def getEntregaPendienteEvaluacion(request, idDocente = None):
    evPendientes = Evaluacion.objects.filter(id_docente__id = idDocente, estado = 'P').order_by('fechaEntrega').all()
    serializer = EvaluacionSerializer(evPendientes, many = "true")
    return Response(serializer.data)

#Visualizar para autoridad asignaturas atrasadas y cantidad de atrasos
@api_view(['GET'])
def getAsignaturasAtrasadas(request):
    listaAsignaturas = Asignatura.objects.all()
    fechaActual = date.today()
    listaAsignaturasAtrasadas = []
    numeroAtrasosAsignaturas = []


    for asignatura in listaAsignaturas:
        listaEvaluacionesAsignatura = Evaluacion.objects.filter(id_coordinacion__id_asignatura__nombre = asignatura.nombre, id_coordinacion__id_asignatura__codigo = asignatura.codigo, id_coordinacion__id_asignatura__componente = asignatura.componente)
        atrasos = 0

        #por cada evaluacion de una asignatura
        for evaluacionAsignatura in listaEvaluacionesAsignatura:
            
            #Si la evaluacion esta pendiente de entrega y supera la fecha de entrega que debiese
            if evaluacionAsignatura.estado == 'P' and evaluacionAsignatura.fechaEntrega < fechaActual:
                #se suma 1 evaluacion atrasada
                atrasos += 1
                continue
        if atrasos > 0:
            listaAsignaturasAtrasadas.append(asignatura)
            numeroAtrasosAsignaturas.append(atrasos)
            continue
    
    serializerAsignaturas = AsignaturaSerializer(listaAsignaturasAtrasadas, many = "true")

    return Response([serializerAsignaturas.data,numeroAtrasosAsignaturas])

#Visualizar Secciones de una asignatura con atrasos y su numero
@api_view(['GET'])
def getSeccionesAsignaturaAtrasadas(request, idAsignatura = None):
    fechaActual = date.today()
    listaSecciones = Coordinacion_Seccion.objects.filter(id_asignatura = idAsignatura, isActive = True)
    listaEvaluacionesPendientes = Evaluacion.objects.filter(id_coordinacion__id_asignatura = idAsignatura, estado = 'P')
    listaSeccionesAtrasadas = []
    listaNumeroAtrasos = []

    for seccion in listaSecciones:
        posiblesAtrasos = Evaluacion.objects.filter(id_coordinacion__id_asignatura = idAsignatura, estado = 'P', id_coordinacion__seccion = seccion.seccion, id_coordinacion__coordinacion = seccion.coordinacion)
        atrasos = 0
        for posibleAtraso in posiblesAtrasos:
            if posibleAtraso.fechaEntrega < fechaActual:
                atrasos += 1
                continue
        if atrasos > 0:
            listaSeccionesAtrasadas.append(seccion)
            listaNumeroAtrasos.append(atrasos)
            continue

    serializerSeccionesAtrasadas = CoordinacionSeccionSerializer(listaSeccionesAtrasadas, many = "true")

    return Response([serializerSeccionesAtrasadas.data, listaNumeroAtrasos])


@api_view(['GET'])
def getAllEvaluacionesMail(request):
    evaluaciones = Evaluacion.objects.all()
    serializer = EvaluacionDocenteSerializer(evaluaciones, many="true")
    return Response(serializer.data)

@api_view(['GET'])
def getInfoDashboardCoordinador(request, idUsuario = None):
    numeroAsignaturas = Asignatura.objects.filter(id_coordinador__id_usuario = idUsuario).count()
    evaluacionesPendientes = Evaluacion.objects.filter(estado = 'P', id_coordinacion__id_asignatura__id_coordinador__id_usuario = idUsuario, id_coordinacion__isActive = True).count()
    solicitudesActuales = Solicitud_Revision.objects.filter(id_evaluacion__id_coordinacion__id_asignatura__id_coordinador__id_usuario = idUsuario, id_evaluacion__id_coordinacion__isActive = True).count()
    solicitudesPendientes = Solicitud_Revision.objects.filter(id_evaluacion__id_coordinacion__id_asignatura__id_coordinador__id_usuario = idUsuario, id_evaluacion__id_coordinacion__isActive = True, estado = 'P').count()
    solicitudesAprobadas = Solicitud_Revision.objects.filter(id_evaluacion__id_coordinacion__id_asignatura__id_coordinador__id_usuario = idUsuario, id_evaluacion__id_coordinacion__isActive = True, estado = 'A').count()
    solicitudesRechazadas = Solicitud_Revision.objects.filter(id_evaluacion__id_coordinacion__id_asignatura__id_coordinador__id_usuario = idUsuario, id_evaluacion__id_coordinacion__isActive = True, estado = 'R').count()
    solicitudesRevision = Solicitud_Revision.objects.filter(id_evaluacion__id_coordinacion__id_asignatura__id_coordinador__id_usuario = idUsuario, id_evaluacion__id_coordinacion__isActive = True, estado = 'E').count()

    return Response([numeroAsignaturas, evaluacionesPendientes, solicitudesActuales, solicitudesPendientes, solicitudesAprobadas, solicitudesRechazadas,solicitudesRevision])

@api_view(['GET'])
def getInfoDashboardEstudiante(request, idUsuario = None):
    cursosActuales = Coordinacion_Estudiante.objects.filter(id_estudiante__id_usuario = idUsuario, id_coordinacion__isActive = True).all()
    serializer = CoordinacionEstudianteSerializer(cursosActuales, many = "true")
    
    solTotales = Solicitud_Revision.objects.filter(Q(estado = 'A') | Q(estado = 'R'), id_estudiante__id_usuario = idUsuario, id_evaluacion__id_coordinacion__isActive = True).all().order_by('-fecha_respuesta')
    serializerTwo = SolicitudSerializer(solTotales, many = "true")
    solicitudesRealizadas = Solicitud_Revision.objects.filter(id_estudiante__id_usuario = idUsuario, id_evaluacion__id_coordinacion__isActive = True).count()
    solicitudesPendientes = Solicitud_Revision.objects.filter(id_estudiante__id_usuario = idUsuario, id_evaluacion__id_coordinacion__isActive = True, estado = 'P').count()
    solicitudesAprobadas = Solicitud_Revision.objects.filter(id_estudiante__id_usuario = idUsuario, id_evaluacion__id_coordinacion__isActive = True, estado = 'A').count()
    solicitudesRechazadas = Solicitud_Revision.objects.filter(id_estudiante__id_usuario = idUsuario, id_evaluacion__id_coordinacion__isActive = True, estado = 'R').count()
    solicitudesRevision = Solicitud_Revision.objects.filter(id_estudiante__id_usuario = idUsuario, id_evaluacion__id_coordinacion__isActive = True, estado = 'E').count()

    return Response([serializer.data, solicitudesRevision, solicitudesRealizadas, solicitudesPendientes, solicitudesAprobadas, solicitudesRechazadas, serializerTwo.data])

@api_view(['GET'])
def getInfoDashboardJefeCarrera(request, idUsuario = None):
    estudiantes = requests.get("http://127.0.0.1:8000/estudiante/all").json()
    id_jefe_carrera = Jefe_Carrera.objects.filter(id_usuario = idUsuario).first().id
    id_Carrera = Carrera.objects.filter(id_jefeCarrera = id_jefe_carrera).first().id
    id_plan_estudio = Plan_Estudio.objects.filter(id_carrera = id_Carrera).first().id
    estudiantesEnCarrera = 0
    for estudiante in estudiantes:
        if estudiante["id_planEstudio"] == id_plan_estudio:
            estudiantesenCarrera = estudiantesenCarrera + 1

    #estudiantesEnCarrera = Estudiante.objects.filter(id_planEstudio__id_carrera__id_jefeCarrera__id_usuario = idUsuario).count()
    solicitudesSemestre = Solicitud_Revision.objects.filter(id_estudiante__id_planEstudio__id_carrera__id_jefeCarrera__id_usuario = idUsuario, id_evaluacion__id_coordinacion__isActive = True).count()
    solicitudesPendientes = Solicitud_Revision.objects.filter(id_estudiante__id_planEstudio__id_carrera__id_jefeCarrera__id_usuario = idUsuario, id_evaluacion__id_coordinacion__isActive = True, estado = 'P').count()
    solicitudesAprobadas = Solicitud_Revision.objects.filter(id_estudiante__id_planEstudio__id_carrera__id_jefeCarrera__id_usuario = idUsuario, id_evaluacion__id_coordinacion__isActive = True, estado = 'A').count()
    solicitudesRechazadas = Solicitud_Revision.objects.filter(id_estudiante__id_planEstudio__id_carrera__id_jefeCarrera__id_usuario = idUsuario, id_evaluacion__id_coordinacion__isActive = True, estado = 'R').count()
    notasCambiadas = Cambio_nota.objects.filter(id_calificacion__id_estudiante__id_planEstudio__id_carrera__id_jefeCarrera__id_usuario = idUsuario, id_calificacion__id_evaluacion__id_coordinacion__isActive = True).count()

    return Response([estudiantesEnCarrera, solicitudesSemestre, solicitudesPendientes, solicitudesAprobadas, solicitudesRechazadas, notasCambiadas])
@api_view(['GET'])
def evaluacionesCoordinacionCursosEspejo(request, bloqueHorario = None, idUsuario = None):
    # Funcionando.
    if request.method == 'GET':
        ## Lista con los cursos asociados a ese horario y al id del docente
        cursos = Coordinacion_Docente.objects.filter(id_docente__id_usuario__id = idUsuario, id_coordinacion__bloques_horario = bloqueHorario).values_list('id_coordinacion__id', flat= True)
        ##evaluacionCoordinacion = Evaluacion.objects.filter(id_coordinacion__id = cursos).distinct('nombre').all()
        evaluaciones = []
        ## Significa que existe por lo menos un curso
        if cursos.count() != 0:
            ## Obtenemos los nombres de las evaluaciones de un curso
            ## En teoria si son las mismas evaluaciones para todos los cursos, solo con un curso tendriamos todas las evaluaciones
            ## En caso de ser un curso, se obtiene solo las de ese curso
            nombresEvaluacionCoordinacion = Evaluacion.objects.filter(id_coordinacion__id = cursos[0]).distinct('nombre').values_list('nombre',flat=True)
            for nombre in nombresEvaluacionCoordinacion:
                evaluaciones.append([])
            for id in cursos:
                for index ,nombre in enumerate(nombresEvaluacionCoordinacion):
                    ## Buscamos las evaluaciones por nombre y el id del curso
                    ## evaluaciones = [Evaluaciones 1],[Evaluaciones 2],[...],[...], una evaluacion por cada curso, 
                    ## en el caso de que solo haya un curso solo sera una evaluacion por index
                    evaluacionesPorNombre = Evaluacion.objects.filter(id_coordinacion__id = id, nombre = nombre).all()
                    evaluaciones[index].extend(EvaluacionSerializer(evaluacionesPorNombre, many = "true").data)
        return Response(evaluaciones)


@api_view(['GET']) ## Cambio a bloque horario - antes id, se agrega distinct
def informacionCoordinacionCursoEspejo(request, idUsuario = None ,bloqueHorario = None):
    coordinacion = Coordinacion_Docente.objects.filter(id_coordinacion__bloques_horario = bloqueHorario, id_docente__id_usuario__id = idUsuario).distinct('id_coordinacion__bloques_horario')
    serializerUnico = CoordinacionDocenteCursoEspejoSerializer(coordinacion, many = "true")
    coordinacion = Coordinacion_Docente.objects.filter(id_coordinacion__bloques_horario = bloqueHorario, id_docente__id_usuario__id = idUsuario).all()
    serializer = CoordinacionDocenteCursoEspejoSerializer(coordinacion, many = "true")
    return Response([serializerUnico.data,serializer.data])

# Obtiene los estudiantes que estan inscitos en una coordinacion. 
# Se cargan en la vista de subir calificaciones.
@api_view(['GET'])
def getCalificacionesEstudiantesCursosEspejo(request,bloqueHorario = None, idDocente = None):
    ## Curso en comun de los estudiantes, se asume que un estudiante no puede estar en los dos cursos inscrito
    cursosComun = Coordinacion_Docente.objects.filter(id_coordinacion__bloques_horario = bloqueHorario, id_docente__id = idDocente).values_list('id_coordinacion__id',flat=True)
    arregloEstudiante = []
    for id in cursosComun:
        calificacionEstudiantes = Coordinacion_Estudiante.objects.filter(id_coordinacion = id).distinct('id_estudiante')
        arregloEstudiante.extend(CoordinacionEstudianteSerializer(calificacionEstudiantes, many="true").data)

    return Response(arregloEstudiante)

""" Función para obtener la coordinación (Laboratorio o Teoría) inscrita por un estudiante. 
Útil para visualizar las calificaciones y evaluaciones de un estudiante en el componente opuesto,
es decir, los docentes de Teoría pueden acceder a esta información del componene Laboratorio, y viceversa.
En el caso de que el estudiante esté inscrito en un único componente, la función retorna False.
Mencionar además que se consideran los cursos espejos, ya que la función se utiliza en Docente. """ 
@api_view(['GET'])
def estudiantePertenece(request, bloqueHorario = None, idDocente = None, componente = None, idEstudiante = None):
    asignaturasComun = Coordinacion_Docente.objects.filter(id_coordinacion__bloques_horario = bloqueHorario, id_docente__id = idDocente, id_coordinacion__isActive = True).values_list('id_coordinacion__id_asignatura__codigo', flat=True)
    for codigoAsignatura in asignaturasComun:
        consult = Coordinacion_Estudiante.objects.filter(id_coordinacion__id_asignatura__codigo = codigoAsignatura, id_coordinacion__id_asignatura__componente = componente, id_estudiante__id = idEstudiante, id_coordinacion__isActive = True)
        if consult:
            serializer = CoordinacionEstudianteSerializer(consult, many = "true")
            return Response(serializer.data)

    return Response(False)
    
# Obtener los datos de una evaluación en particular. Cambiar el estado de una evaluacion.
@api_view(['GET', 'PUT'])
def crudOneEvaluacionCursosEspejo(request, bloqueHorario = None, idDocente = None, nombreEvaluacion =None):
    
    if request.method == 'GET':
        ## Curso en comun de las evaluaciones, ademas se busca por el nombre en particular
        cursosComun = Coordinacion_Docente.objects.filter(id_coordinacion__bloques_horario = bloqueHorario, id_docente__id = idDocente).values_list('id_coordinacion__id',flat=True)
        evaluacionesDevolver = []
        #Evaluaciones a poner nota
        for id in cursosComun:
            evaluacionBuscada = Evaluacion.objects.filter(nombre = nombreEvaluacion, id_coordinacion = id)
            evaluacionesDevolver.extend(PostEvaluacionSerializer(evaluacionBuscada, many ="true").data)
        
        return Response(evaluacionesDevolver) 

## Calificiones segun una evaluacion
@api_view(['GET'])
def getCalificacionesByDocenteCursosEspejo(request,bloqueHorario = None, idDocente = None, nombreEvaluacion =None):
    ## Curso en comun de las evaluaciones, ademas se busca por el nombre en particular  
    cursosComun = Coordinacion_Docente.objects.filter(id_coordinacion__bloques_horario = bloqueHorario, id_docente__id = idDocente).values_list('id_coordinacion__id',flat=True)
    calificacionesDevolver = []
    #Calificaciones de estudiantes segun evaluacion y cursos espejo
    for id in cursosComun:
        evaluacionBuscada = Evaluacion.objects.filter(nombre = nombreEvaluacion, id_coordinacion = id).values_list('id',flat=True)
        calificaciones =  Calificacion.objects.filter(id_evaluacion__id = evaluacionBuscada[0]).all().order_by('id_estudiante__rut')
        calificacionesDevolver.extend(CalificacionSerializer(calificaciones, many = "true").data)
    return Response(calificacionesDevolver) 

## secciones de una asignatura
@api_view(['GET'])
def getSeccionesAsignaturaJefeCarrera(request, idAsignatura = None):    
    
    idsCoordinacion = Coordinacion_Docente.objects.filter(id_coordinacion__id_asignatura = idAsignatura).distinct('id_coordinacion__id').values_list('id_coordinacion__id', flat=True)
    #Arreglo donde cada espacio es una seccion de una asignatura
    arregloInformacion = []
    for id in idsCoordinacion:
        coordinacion_docentes = Coordinacion_Docente.objects.filter(id_coordinacion__id = id)
        arregloInformacion.append(DocenteCursoSerializer(coordinacion_docentes, many="true").data)

    return Response(arregloInformacion)

## Solicitudes para el jefe de carrera dash
@api_view(['GET'])
def getSolicitudesDashboardJefeCarrera(request, idJefeCarrera = None):    
    
    idsAsignatura = Asignaturas_PlanEstudio.objects.filter(id_planEstudio__id_carrera__id_jefeCarrera__id_usuario = idJefeCarrera).distinct('id_asignatura').values_list('id_asignatura', flat= True)
    nombreAsignaturas = []
    dataRechazados = []
    dataPendientes = []
    dataAceptados = []
    dataRevision = []
    #SolicitudSerializer
    for id in idsAsignatura:
        nombre = Asignatura.objects.filter(id = id).values_list('nombre',flat= True)
        #nombre = solicitud.values_list('id_evaluacion__id_coordinacion__id_asignatura__nombre')
        # Se agrega nombre de la asignatura
        nombreAsignaturas.extend(nombre)
        # Se cuentan las solicitudes pendientes de esa asignatura
        dataPendientes.append(Solicitud_Revision.objects.filter(id_evaluacion__id_coordinacion__id_asignatura__id = id, estado = 'P').count())
        dataRechazados.append(Solicitud_Revision.objects.filter(id_evaluacion__id_coordinacion__id_asignatura__id = id, estado = 'R').count())
        dataAceptados.append(Solicitud_Revision.objects.filter(id_evaluacion__id_coordinacion__id_asignatura__id = id, estado = 'A').count())
        dataRevision.append(Solicitud_Revision.objects.filter(id_evaluacion__id_coordinacion__id_asignatura__id = id, estado = 'E').count())
    return Response([nombreAsignaturas,dataRechazados,dataPendientes,dataAceptados,dataRevision])

## Solicitudes para el jefe de carrera dash
@api_view(['GET'])
def getCambioNotasDashboardJefeCarrera(request, idJefeCarrera = None):    
    
    idsAsignatura = Asignaturas_PlanEstudio.objects.filter(id_planEstudio__id_carrera__id_jefeCarrera__id_usuario = idJefeCarrera).distinct('id_asignatura').values_list('id_asignatura', flat= True)
    cambios = []
    asignaturas = []
    for id in idsAsignatura:
        cantidad = Cambio_nota.objects.filter(id_calificacion__id_evaluacion__id_coordinacion__id_asignatura__id = id).count()
        if cantidad != 0:
            nombre = Asignatura.objects.filter(id = id).values_list('nombre',flat= True)
            asignaturas.append(nombre[0])
            cambios.append(cantidad)
    return Response([cambios,asignaturas])

@api_view(['GET'])
def getAllCalificacionesByCurso(request, codigoAsig = None):
    calificaciones = Calificacion.objects.filter(id_evaluacion__id_coordinacion__id_asignatura__codigo = codigoAsig).all()
    serializer = CalificacionSerializer(calificaciones, many="true")
    return Response(serializer.data)

##Todas los cambios de nota en un semestre activo de un departamento correspondiente
@api_view(['GET'])
def getInfoDashboardAutoridadSub(request, idAutoridad = None):
    info = []
    ## n cambios notas en semestre
    info.append(Cambio_nota.objects.filter(id_calificacion__id_estudiante__id_planEstudio__id_carrera__id_departamento__id_subdirector__id_usuario = idAutoridad, id_calificacion__id_evaluacion__id_coordinacion__isActive = True).count())
    ## n cambios notas a azules
    info.append(Cambio_nota.objects.filter(id_calificacion__id_estudiante__id_planEstudio__id_carrera__id_departamento__id_subdirector__id_usuario = idAutoridad, id_calificacion__id_evaluacion__id_coordinacion__isActive = True, anterior_nota__lt = 4, actual_nota__gte = 4).count())
    ## n cambios notas a rojos
    info.append(Cambio_nota.objects.filter(id_calificacion__id_estudiante__id_planEstudio__id_carrera__id_departamento__id_subdirector__id_usuario = idAutoridad, id_calificacion__id_evaluacion__id_coordinacion__isActive = True, anterior_nota__gte = 4, actual_nota__lt = 4).count())
    
    ##obtengo asignaturas correspondientes autoridad
    relacionAsignaturaPlanEstudio = Asignaturas_PlanEstudio.objects.filter(id_planEstudio__id_carrera__id_departamento__id_subdirector__id_usuario = idAutoridad)
    asignaturas = Asignatura.objects.all()
    asignaturasAutoridad = []
    for relacion in relacionAsignaturaPlanEstudio:
        for asignatura in asignaturas:
            if relacion.id_asignatura.id == asignatura.id:
                asignaturasAutoridad.append(asignatura)
                continue
    
    ##n cambios en ponderaciones
    nCambiosPonderaciones = 0
    for asignatura in asignaturasAutoridad:
        nCambiosPonderaciones += Cambio_Ponderacion.objects.filter(id_evaluacion__id_coordinacion__isActive = True, id_evaluacion__id_coordinacion__id_asignatura = asignatura.id).count()
    
    info.append(nCambiosPonderaciones)

    #n cambio fechas
    nCambiosFecha = 0
    for asignatura in asignaturasAutoridad:
        nCambiosFecha += Cambio_Fecha.objects.filter(id_evaluacion__id_coordinacion__isActive = True, id_evaluacion__id_coordinacion__id_asignatura = asignatura.id).count()
    info.append(nCambiosFecha)

    ## n Solicitudes
    info.append(Solicitud_Revision.objects.filter(id_evaluacion__id_coordinacion__isActive = True, id_estudiante__id_planEstudio__id_carrera__id_departamento__id_subdirector__id_usuario = idAutoridad).count())
    ## n Solicitudes P
    info.append(Solicitud_Revision.objects.filter(id_evaluacion__id_coordinacion__isActive = True, id_estudiante__id_planEstudio__id_carrera__id_departamento__id_subdirector__id_usuario = idAutoridad, estado = 'P').count())
    ## n solicitudes A
    info.append(Solicitud_Revision.objects.filter(id_evaluacion__id_coordinacion__isActive = True, id_estudiante__id_planEstudio__id_carrera__id_departamento__id_subdirector__id_usuario = idAutoridad, estado = 'A').count())
    ## n Solicitudes R
    info.append(Solicitud_Revision.objects.filter(id_evaluacion__id_coordinacion__isActive = True, id_estudiante__id_planEstudio__id_carrera__id_departamento__id_subdirector__id_usuario = idAutoridad, estado = 'R').count())

    ## Retorno
    # ## n cambios notas en semestre
    # ## n cambios notas a azules
    #  n cambios notas a rojos
    # ##n cambios en ponderaciones
    # #n cambio fechas
    # n Solicitudes
    # n Solicitudes P
    # n Solicitudes A
    # n Solicitudes R
    
    return Response(info)
    
## Cambio fecha para el jefe de carrera dash
@api_view(['GET'])
def getCambioFechaDashboardJefeCarrera(request, idJefeCarrera = None):    
    
    idsAsignatura = Asignaturas_PlanEstudio.objects.filter(id_planEstudio__id_carrera__id_jefeCarrera__id_usuario = idJefeCarrera).distinct('id_asignatura').values_list('id_asignatura', flat= True)
    cambios = []
    asignaturas = []
    for id in idsAsignatura:
        cantidad = Cambio_Fecha.objects.filter(id_evaluacion__id_coordinacion__id_asignatura__id = id).count()
        if cantidad != 0:
            nombre = Asignatura.objects.filter(id = id).values_list('nombre',flat= True)
            asignaturas.append(nombre[0])
            cambios.append(cantidad)
    return Response([cambios,asignaturas])

## Atrasos segun asignatura para el jefe de carrera dash
@api_view(['GET'])
def getAtrasosDashboardJefeCarrera(request, idJefeCarrera = None):    
    
    idsAsignatura = Asignaturas_PlanEstudio.objects.filter(id_planEstudio__id_carrera__id_jefeCarrera__id_usuario = idJefeCarrera).distinct('id_asignatura').values_list('id_asignatura', flat= True)
    atrasos = []
    asignaturas = []
    for id in idsAsignatura:
        ## Fecha entrega < Fecha de hoy
        cantidad = Evaluacion.objects.filter(id_coordinacion__id_asignatura__id = id, estado = 'P', fechaEntrega__lt=datetime.date.today()).count()
        if cantidad != 0:
            nombre = Asignatura.objects.filter(id = id).values_list('nombre',flat= True)
            asignaturas.append(nombre[0])
            atrasos.append(cantidad)
    return Response([atrasos,asignaturas])

## Atrasos segun coordinaciones del coordinador dash
@api_view(['GET'])                                                                                                                                                                                          
def getAtrasosDashboardCoordinador(request, idCoordinador = None):    
    
    idsCoordinaciones = Coordinacion_Seccion.objects.filter(id_asignatura__id_coordinador__id_usuario__id = idCoordinador).distinct('id').values_list('id', flat= True)
    atrasos = []    
    secciones = []
    for id in idsCoordinaciones:
        ## Fecha entrega < Fecha de hoy
        cantidad = Evaluacion.objects.filter(id_coordinacion__id = id, estado = 'P', fechaEntrega__lt=datetime.date.today()).count()
        if cantidad != 0:
            seccion = Coordinacion_Seccion.objects.filter(id = id).values_list('seccion','coordinacion')

            
            secciones.append([str(seccion[0][1])+"-"+str(seccion[0][0])])
            atrasos.append(cantidad)
    return Response([atrasos,secciones])

## cambio de fecha segun coordinaciones del coordinador dash
@api_view(['GET'])                                                                                                                                                                                          
def getCambioNotasDashboardCoordinador(request, idCoordinador = None):    
    
    idsCoordinaciones = Coordinacion_Seccion.objects.filter(id_asignatura__id_coordinador__id_usuario__id = idCoordinador).distinct('id').values_list('id', flat= True)
    cambios = []    
    secciones = []
    for id in idsCoordinaciones:
        ## Cambios de fecha de esa coordinacion
        cantidad = Cambio_nota.objects.filter(id_calificacion__id_evaluacion__id_coordinacion__id = id).count()
        if cantidad != 0:
            seccion = Coordinacion_Seccion.objects.filter(id = id).values_list('seccion','coordinacion')
            secciones.append([str(seccion[0][1])+"-"+str(seccion[0][0])])
            cambios.append(cantidad)
    return Response([cambios,secciones])